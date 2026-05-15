from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


TEMPLATE_SIZE = (256, 96)


@dataclass(frozen=True)
class ProcessedVeinImage:
    source_path: Path
    original: np.ndarray
    roi: np.ndarray
    enhanced: np.ndarray
    vein_response: np.ndarray
    vein_mask: np.ndarray
    template: np.ndarray
    bbox: tuple[int, int, int, int]


@dataclass(frozen=True)
class MatchResult:
    person_id: str
    score: float
    cosine_score: float
    dice_score: float
    is_match: bool


def load_image(path: str | Path) -> np.ndarray:
    image_path = Path(path)
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image could not be read: {image_path}")
    return image


def _largest_contour_bbox(binary: np.ndarray) -> tuple[int, int, int, int] | None:
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    height, width = binary.shape[:2]
    min_area = height * width * 0.05
    candidates = [contour for contour in contours if cv2.contourArea(contour) >= min_area]
    if not candidates:
        candidates = contours

    contour = max(candidates, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(contour)
    return x, y, w, h


def crop_finger_roi(image: np.ndarray, padding_ratio: float = 0.06) -> tuple[np.ndarray, tuple[int, int, int, int]]:
    """Find a likely finger/palm region and crop it.

    This is intentionally conservative. It works best when the finger is on a
    dark background or inside a shaded NIR box. If segmentation fails, it falls
    back to a centered crop so the rest of the pipeline can still run.
    """

    height, width = image.shape[:2]
    blurred = cv2.GaussianBlur(image, (7, 7), 0)
    normalized = cv2.normalize(blurred, None, 0, 255, cv2.NORM_MINMAX)

    _, bright_mask = cv2.threshold(normalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, dark_mask = cv2.threshold(normalized, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    bright_bbox = _largest_contour_bbox(bright_mask)
    dark_bbox = _largest_contour_bbox(dark_mask)
    bbox = bright_bbox or dark_bbox

    if bbox is None:
        crop_w = int(width * 0.82)
        crop_h = int(height * 0.72)
        x = max((width - crop_w) // 2, 0)
        y = max((height - crop_h) // 2, 0)
        bbox = (x, y, crop_w, crop_h)

    x, y, w, h = bbox
    pad_x = int(w * padding_ratio)
    pad_y = int(h * padding_ratio)
    x0 = max(x - pad_x, 0)
    y0 = max(y - pad_y, 0)
    x1 = min(x + w + pad_x, width)
    y1 = min(y + h + pad_y, height)

    roi = image[y0:y1, x0:x1]
    if roi.size == 0:
        raise ValueError("ROI crop is empty. Check the input image.")

    return roi, (x0, y0, x1 - x0, y1 - y0)


def enhance_contrast(roi: np.ndarray) -> np.ndarray:
    resized = cv2.resize(roi, TEMPLATE_SIZE, interpolation=cv2.INTER_AREA)
    denoised = cv2.fastNlMeansDenoising(resized, h=8)
    clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)
    return cv2.GaussianBlur(enhanced, (3, 3), 0)


def extract_veins(enhanced: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Extract dark vessel-like lines from an enhanced NIR image."""

    kernels = [
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)),
    ]

    responses = [cv2.morphologyEx(enhanced, cv2.MORPH_BLACKHAT, kernel) for kernel in kernels]
    response = np.maximum.reduce(responses)
    response = cv2.GaussianBlur(response, (3, 3), 0)
    response = cv2.normalize(response, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    _, mask = cv2.threshold(response, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    return response, mask


def build_template(vein_response: np.ndarray, vein_mask: np.ndarray) -> np.ndarray:
    response = vein_response.astype(np.float32) / 255.0
    mask = (vein_mask.astype(np.float32) / 255.0) * 0.35
    template = np.clip(response + mask, 0.0, 1.0)
    template = cv2.resize(template, TEMPLATE_SIZE, interpolation=cv2.INTER_AREA)
    mean = float(template.mean())
    std = float(template.std())
    if std < 1e-6:
        return template - mean
    return (template - mean) / std


def process_vein_image(path: str | Path) -> ProcessedVeinImage:
    source_path = Path(path)
    original = load_image(source_path)
    roi, bbox = crop_finger_roi(original)
    enhanced = enhance_contrast(roi)
    vein_response, vein_mask = extract_veins(enhanced)
    template = build_template(vein_response, vein_mask)
    return ProcessedVeinImage(
        source_path=source_path,
        original=original,
        roi=roi,
        enhanced=enhanced,
        vein_response=vein_response,
        vein_mask=vein_mask,
        template=template,
        bbox=bbox,
    )


def enroll_template(image_paths: list[str | Path]) -> np.ndarray:
    if not image_paths:
        raise ValueError("At least one enrollment image is required.")

    templates = [process_vein_image(path).template for path in image_paths]
    average_template = np.mean(np.stack(templates, axis=0), axis=0)
    mean = float(average_template.mean())
    std = float(average_template.std())
    if std < 1e-6:
        return average_template - mean
    return (average_template - mean) / std


def compare_templates(candidate: np.ndarray, enrolled: np.ndarray) -> tuple[float, float, float]:
    candidate_flat = candidate.reshape(-1).astype(np.float32)
    enrolled_flat = enrolled.reshape(-1).astype(np.float32)

    denom = float(np.linalg.norm(candidate_flat) * np.linalg.norm(enrolled_flat))
    cosine = 0.0 if denom < 1e-9 else float(np.dot(candidate_flat, enrolled_flat) / denom)
    cosine_score = float(np.clip((cosine + 1.0) / 2.0, 0.0, 1.0))

    candidate_binary = candidate > np.percentile(candidate, 70)
    enrolled_binary = enrolled > np.percentile(enrolled, 70)
    intersection = np.logical_and(candidate_binary, enrolled_binary).sum()
    dice_denominator = candidate_binary.sum() + enrolled_binary.sum()
    dice_score = 0.0 if dice_denominator == 0 else float((2.0 * intersection) / dice_denominator)

    score = 0.72 * cosine_score + 0.28 * dice_score
    return float(score), cosine_score, dice_score


def save_outputs(processed: ProcessedVeinImage, output_dir: str | Path) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    cv2.imwrite(str(output_path / "01_original.png"), processed.original)
    cv2.imwrite(str(output_path / "02_roi.png"), processed.roi)
    cv2.imwrite(str(output_path / "03_enhanced.png"), processed.enhanced)
    cv2.imwrite(str(output_path / "04_vein_response.png"), processed.vein_response)
    cv2.imwrite(str(output_path / "05_vein_mask.png"), processed.vein_mask)

    template_vis = cv2.normalize(processed.template, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite(str(output_path / "06_template.png"), template_vis)


def save_template(person_id: str, template: np.ndarray, db_dir: str | Path) -> Path:
    db_path = Path(db_dir)
    db_path.mkdir(parents=True, exist_ok=True)
    output_path = db_path / f"{person_id}.npz"
    np.savez_compressed(output_path, person_id=person_id, template=template.astype(np.float32))
    return output_path


def load_template(path: str | Path) -> tuple[str, np.ndarray]:
    data = np.load(Path(path), allow_pickle=False)
    return str(data["person_id"]), data["template"].astype(np.float32)


def find_best_match(
    candidate_template: np.ndarray,
    db_dir: str | Path,
    threshold: float = 0.62,
) -> MatchResult | None:
    db_path = Path(db_dir)
    template_files = sorted(db_path.glob("*.npz"))
    if not template_files:
        return None

    best: MatchResult | None = None
    for template_path in template_files:
        person_id, enrolled_template = load_template(template_path)
        score, cosine_score, dice_score = compare_templates(candidate_template, enrolled_template)
        result = MatchResult(
            person_id=person_id,
            score=score,
            cosine_score=cosine_score,
            dice_score=dice_score,
            is_match=score >= threshold,
        )
        if best is None or result.score > best.score:
            best = result

    return best


from pathlib import Path
from random import Random

import cv2
import numpy as np
import typer
from rich import print


def _draw_branching_veins(canvas: np.ndarray, rng: Random, person_seed: int) -> None:
    height, width = canvas.shape[:2]
    center_y = height // 2 + rng.randint(-16, 16)
    amplitude = rng.randint(10, 28)
    period = rng.uniform(22.0, 54.0)
    phase = rng.uniform(0.0, 2.0 * np.pi)
    base_points = []
    x = int(width * 0.12)
    while x < int(width * 0.9):
        y = center_y + int(amplitude * np.sin((x + person_seed) / period + phase)) + rng.randint(-5, 5)
        base_points.append((x, y))
        x += rng.randint(22, 35)

    cv2.polylines(canvas, [np.array(base_points, dtype=np.int32)], False, color=48, thickness=3)

    branch_stride = rng.choice([2, 3])
    branch_bias = rng.choice([-1, 1])
    for idx, point in enumerate(base_points[2:-2], start=2):
        if idx % branch_stride == 0:
            direction = -1 if rng.random() < 0.5 else 1
            length = rng.randint(28, 55)
            end = (point[0] + branch_bias * rng.randint(18, 45), point[1] + direction * length)
            mid = ((point[0] + end[0]) // 2, point[1] + direction * rng.randint(10, 24))
            cv2.polylines(canvas, [np.array([point, mid, end], dtype=np.int32)], False, color=42, thickness=2)

    for _ in range(rng.randint(6, 11)):
        start = (rng.randint(int(width * 0.15), int(width * 0.85)), rng.randint(int(height * 0.35), int(height * 0.65)))
        end = (start[0] + rng.randint(-35, 35), start[1] + rng.randint(-20, 20))
        cv2.line(canvas, start, end, color=rng.randint(50, 72), thickness=1)


def _create_sample(person_id: int, sample_id: int, width: int = 420, height: int = 160) -> np.ndarray:
    sample_rng = Random(person_id * 10_000 + sample_id)
    person_rng = Random(person_id * 91_337)
    image = np.full((height, width), 18, dtype=np.uint8)

    finger = np.full_like(image, 0)
    x_margin = 24 + sample_rng.randint(-3, 3)
    y_margin = 26 + sample_rng.randint(-4, 4)
    cv2.rectangle(finger, (x_margin, y_margin), (width - x_margin, height - y_margin), 210, thickness=-1)
    cv2.ellipse(finger, (x_margin, height // 2), (26, height // 2 - y_margin), 0, 90, 270, 210, -1)
    cv2.ellipse(finger, (width - x_margin, height // 2), (26, height // 2 - y_margin), 0, -90, 90, 210, -1)

    veins = finger.copy()
    _draw_branching_veins(veins, person_rng, person_id * 137)
    image = np.maximum(image, veins)

    gradient = np.linspace(12, -8, width, dtype=np.float32)
    image = np.clip(image.astype(np.float32) + gradient[None, :], 0, 255).astype(np.uint8)
    image = cv2.GaussianBlur(image, (5, 5), 0)

    noise = np.random.default_rng(person_id * 50_000 + sample_id).normal(0, 5.5, image.shape)
    image = np.clip(image.astype(np.float32) + noise, 0, 255).astype(np.uint8)

    angle = sample_rng.uniform(-1.5, 1.5)
    matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1.0 + sample_rng.uniform(-0.015, 0.015))
    return cv2.warpAffine(image, matrix, (width, height), flags=cv2.INTER_LINEAR, borderValue=18)


def main(
    output: Path = typer.Option(Path("data/raw/synthetic"), "--output", "-o"),
    people: int = typer.Option(5, "--people"),
    samples: int = typer.Option(6, "--samples"),
) -> None:
    output.mkdir(parents=True, exist_ok=True)

    for person_idx in range(1, people + 1):
        person_dir = output / f"person_{person_idx:03d}"
        person_dir.mkdir(parents=True, exist_ok=True)
        for sample_idx in range(1, samples + 1):
            image = _create_sample(person_idx, sample_idx)
            cv2.imwrite(str(person_dir / f"sample_{sample_idx:02d}.png"), image)

    print(f"[green]Synthetic dataset created:[/green] {output}")
    print(f"[green]People:[/green] {people}  [green]Samples each:[/green] {samples}")


if __name__ == "__main__":
    typer.run(main)

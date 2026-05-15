from __future__ import annotations

import csv
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from statistics import mean, median

import numpy as np
import typer
from rich import print

from nexivo_vein_mvp.pipeline import compare_templates, process_vein_image


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


@dataclass(frozen=True)
class Sample:
    person_id: str
    image_path: Path
    template: np.ndarray


def _person_dirs(dataset: Path) -> list[Path]:
    return sorted(path for path in dataset.iterdir() if path.is_dir())


def _images(person_dir: Path) -> list[Path]:
    return sorted(path for path in person_dir.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS)


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0

    sorted_values = sorted(values)
    if len(sorted_values) == 1:
        return sorted_values[0]

    position = (len(sorted_values) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = position - lower
    return sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight


def _summary(values: list[float]) -> dict[str, float | int]:
    if not values:
        return {"count": 0, "min": 0.0, "p05": 0.0, "median": 0.0, "mean": 0.0, "p95": 0.0, "max": 0.0}

    return {
        "count": len(values),
        "min": min(values),
        "p05": _percentile(values, 0.05),
        "median": median(values),
        "mean": mean(values),
        "p95": _percentile(values, 0.95),
        "max": max(values),
    }


def _thresholds(step: float) -> list[float]:
    if step <= 0.0 or step > 1.0:
        raise typer.BadParameter("--threshold-step must be in the range (0, 1].")

    count = int(round(1.0 / step))
    thresholds = [round(index * step, 6) for index in range(count + 1)]
    if thresholds[-1] != 1.0:
        thresholds.append(1.0)
    return thresholds


def _format_summary(name: str, values: dict[str, float | int]) -> str:
    return (
        f"| {name} | {values['count']} | {values['min']:.5f} | {values['p05']:.5f} | "
        f"{values['median']:.5f} | {values['mean']:.5f} | {values['p95']:.5f} | {values['max']:.5f} |"
    )


def main(
    dataset: Path = typer.Argument(..., help="Folder with one subfolder per person."),
    scores_csv: Path = typer.Option(Path("reports/score_distribution.csv"), "--scores-csv"),
    report_md: Path = typer.Option(Path("reports/score_distribution.md"), "--report-md"),
    threshold_step: float = typer.Option(0.01, "--threshold-step"),
) -> None:
    people = _person_dirs(dataset)
    if not people:
        raise typer.BadParameter(f"No person folders found in {dataset}")

    samples: list[Sample] = []
    for person_dir in people:
        image_paths = _images(person_dir)
        if len(image_paths) < 2:
            print(f"[yellow]Skipping {person_dir.name}: at least 2 images are required.[/yellow]")
            continue

        for image_path in image_paths:
            processed = process_vein_image(image_path)
            samples.append(Sample(person_id=person_dir.name, image_path=image_path, template=processed.template))

    if len(samples) < 2:
        raise typer.BadParameter("At least two images are required for score analysis.")

    rows: list[dict[str, str | float | bool]] = []
    same_scores: list[float] = []
    different_scores: list[float] = []

    for left, right in combinations(samples, 2):
        score, cosine_score, dice_score = compare_templates(left.template, right.template)
        is_same_person = left.person_id == right.person_id
        if is_same_person:
            same_scores.append(score)
        else:
            different_scores.append(score)

        rows.append(
            {
                "left_person_id": left.person_id,
                "left_image": str(left.image_path),
                "right_person_id": right.person_id,
                "right_image": str(right.image_path),
                "pair_type": "same" if is_same_person else "different",
                "score": round(score, 5),
                "cosine_score": round(cosine_score, 5),
                "dice_score": round(dice_score, 5),
            }
        )

    scores_csv.parent.mkdir(parents=True, exist_ok=True)
    with scores_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "left_person_id",
                "left_image",
                "right_person_id",
                "right_image",
                "pair_type",
                "score",
                "cosine_score",
                "dice_score",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    threshold_rows = []
    for threshold in _thresholds(threshold_step):
        false_rejects = sum(1 for score in same_scores if score < threshold)
        false_accepts = sum(1 for score in different_scores if score >= threshold)
        frr = false_rejects / len(same_scores) if same_scores else 0.0
        far = false_accepts / len(different_scores) if different_scores else 0.0
        threshold_rows.append(
            {
                "threshold": threshold,
                "far": far,
                "frr": frr,
                "false_accepts": false_accepts,
                "false_rejects": false_rejects,
                "objective": far + frr,
                "eer_gap": abs(far - frr),
            }
        )

    best = min(threshold_rows, key=lambda row: (row["objective"], row["eer_gap"], -row["threshold"]))
    default_threshold = min(threshold_rows, key=lambda row: abs(row["threshold"] - 0.62))
    same_summary = _summary(same_scores)
    different_summary = _summary(different_scores)

    report_md.parent.mkdir(parents=True, exist_ok=True)
    report_md.write_text(
        "\n".join(
            [
                "# Score Distribution Analysis",
                "",
                f"Dataset: `{dataset}`",
                f"Images analyzed: {len(samples)}",
                f"Same-person pairs: {len(same_scores)}",
                f"Different-person pairs: {len(different_scores)}",
                "",
                "## Score Summary",
                "",
                "| Pair type | Count | Min | P05 | Median | Mean | P95 | Max |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
                _format_summary("Same person", same_summary),
                _format_summary("Different person", different_summary),
                "",
                "## Threshold Sweep",
                "",
                f"Best threshold by minimum FAR+FRR: `{best['threshold']:.2f}`",
                f"At best threshold: FAR `{best['far']:.4f}` ({best['false_accepts']}/{len(different_scores)}), "
                f"FRR `{best['frr']:.4f}` ({best['false_rejects']}/{len(same_scores)})",
                f"At current default 0.62: FAR `{default_threshold['far']:.4f}` "
                f"({default_threshold['false_accepts']}/{len(different_scores)}), "
                f"FRR `{default_threshold['frr']:.4f}` ({default_threshold['false_rejects']}/{len(same_scores)})",
                "",
                "## Notes",
                "",
                "- This is a synthetic pre-hardware sanity check, not a biometric validation claim.",
                "- The same/different distributions should be rerun when real NIR samples arrive.",
                f"- Raw pair scores are in `{scores_csv}`.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"[green]Images analyzed:[/green] {len(samples)}")
    print(f"[green]Same-person pairs:[/green] {len(same_scores)}")
    print(f"[green]Different-person pairs:[/green] {len(different_scores)}")
    print(f"[green]Best threshold:[/green] {best['threshold']:.2f}")
    print(f"[green]Scores CSV:[/green] {scores_csv}")
    print(f"[green]Report:[/green] {report_md}")


if __name__ == "__main__":
    typer.run(main)

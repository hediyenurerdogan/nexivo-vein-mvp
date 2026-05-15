from pathlib import Path

import csv
import shutil

import typer
from rich import print

from nexivo_vein_mvp.pipeline import enroll_template, find_best_match, process_vein_image, save_template


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


def _person_dirs(dataset: Path) -> list[Path]:
    return sorted(path for path in dataset.iterdir() if path.is_dir())


def _images(person_dir: Path) -> list[Path]:
    return sorted(path for path in person_dir.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS)


def main(
    dataset: Path = typer.Argument(..., help="Folder with one subfolder per person."),
    db: Path = typer.Option(Path("data/templates"), "--db"),
    report: Path = typer.Option(Path("reports/evaluation.csv"), "--report"),
    threshold: float = typer.Option(0.62, "--threshold", "-t"),
    reset_db: bool = typer.Option(True, "--reset-db/--keep-db"),
) -> None:
    people = _person_dirs(dataset)
    if not people:
        raise typer.BadParameter(f"No person folders found in {dataset}")

    if reset_db and db.exists():
        shutil.rmtree(db)
    db.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str | float | bool]] = []
    for person_dir in people:
        image_paths = _images(person_dir)
        if len(image_paths) < 2:
            print(f"[yellow]Skipping {person_dir.name}: at least 2 images are required.[/yellow]")
            continue

        enrollment_images = image_paths[:-1]
        probe_image = image_paths[-1]
        template = enroll_template(enrollment_images)
        save_template(person_dir.name, template, db)

        probe = process_vein_image(probe_image)
        best = find_best_match(probe.template, db, threshold=threshold)
        if best is None:
            continue

        is_correct_identity = best.person_id == person_dir.name
        rows.append(
            {
                "expected_person_id": person_dir.name,
                "probe_image": str(probe_image),
                "best_person_id": best.person_id,
                "score": round(best.score, 5),
                "cosine_score": round(best.cosine_score, 5),
                "dice_score": round(best.dice_score, 5),
                "threshold": threshold,
                "accepted": best.is_match,
                "correct_identity": is_correct_identity,
            }
        )

    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "expected_person_id",
                "probe_image",
                "best_person_id",
                "score",
                "cosine_score",
                "dice_score",
                "threshold",
                "accepted",
                "correct_identity",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    correct = sum(1 for row in rows if row["accepted"] and row["correct_identity"])
    total = len(rows)
    print(f"[green]Evaluated:[/green] {total} probes")
    print(f"[green]Correct accepted identities:[/green] {correct}/{total}")
    print(f"[green]Report:[/green] {report}")


if __name__ == "__main__":
    typer.run(main)


from pathlib import Path

import typer
from rich import print

from nexivo_vein_mvp.pipeline import find_best_match, process_vein_image


def main(
    image: Path = typer.Argument(..., help="Candidate image path."),
    db: Path = typer.Option(Path("data/templates"), "--db"),
    threshold: float = typer.Option(0.62, "--threshold", "-t"),
) -> None:
    candidate = process_vein_image(image)
    best = find_best_match(candidate.template, db, threshold=threshold)
    if best is None:
        print("[red]No enrolled templates found.[/red]")
        raise typer.Exit(code=1)

    status = "MATCH" if best.is_match else "NO MATCH"
    color = "green" if best.is_match else "yellow"
    print(f"[{color}]{status}[/{color}] person_id={best.person_id}")
    print(f"score={best.score:.4f} cosine={best.cosine_score:.4f} dice={best.dice_score:.4f}")


if __name__ == "__main__":
    typer.run(main)


from pathlib import Path

import typer
from rich import print

from nexivo_vein_mvp.pipeline import process_vein_image, save_outputs


def main(
    image: Path = typer.Argument(..., help="Input finger/palm vein image path."),
    output: Path = typer.Option(Path("data/processed/sample"), "--output", "-o"),
) -> None:
    processed = process_vein_image(image)
    save_outputs(processed, output)
    print(f"[green]Processed:[/green] {image}")
    print(f"[green]ROI bbox:[/green] {processed.bbox}")
    print(f"[green]Outputs:[/green] {output}")


if __name__ == "__main__":
    typer.run(main)


from pathlib import Path

import typer
from rich import print

from nexivo_vein_mvp.pipeline import enroll_template, save_template


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


def _collect_images(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(item for item in path.iterdir() if item.suffix.lower() in IMAGE_EXTENSIONS)


def main(
    person_id: str = typer.Option(..., "--person-id", "-p"),
    images: Path = typer.Option(..., "--images", "-i", help="Image file or folder."),
    db: Path = typer.Option(Path("data/templates"), "--db"),
) -> None:
    image_paths = _collect_images(images)
    if not image_paths:
        raise typer.BadParameter(f"No images found in {images}")

    template = enroll_template(image_paths)
    output_path = save_template(person_id, template, db)
    print(f"[green]Enrolled:[/green] {person_id}")
    print(f"[green]Images:[/green] {len(image_paths)}")
    print(f"[green]Template:[/green] {output_path}")


if __name__ == "__main__":
    typer.run(main)


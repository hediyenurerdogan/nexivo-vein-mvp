from __future__ import annotations

import re
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path

import typer
from rich import print


IMAGE_EXTENSIONS = {".bmp", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def _person_id_from_path(path: str) -> str:
    parts = Path(path).parts
    for index, part in enumerate(parts):
        if part.lower() == "captured images" and index + 1 < len(parts):
            candidate = parts[index + 1]
            if candidate.isdigit():
                return f"person_{int(candidate):03d}"

    for part in reversed(parts):
        match = re.search(r"(\d{3,})", part)
        if match:
            return f"person_{int(match.group(1)):03d}"
    return "person_unknown"


def _finger_id_from_path(path: str) -> str:
    parts = Path(path).parts
    for index, part in enumerate(parts):
        if part.lower() == "captured images" and index + 2 < len(parts):
            return parts[index + 2].lower().replace(" ", "_")

    lower = path.lower()
    for token in ["left", "right", "index", "middle", "ring", "thumb"]:
        if token in lower:
            return token

    matches = re.findall(r"\d+", Path(path).stem)
    if len(matches) >= 2:
        return f"finger_{int(matches[-2]):02d}"
    return "finger_00"


def _iter_images(zip_path: Path) -> list[zipfile.ZipInfo]:
    with zipfile.ZipFile(zip_path) as archive:
        return [
            info
            for info in archive.infolist()
            if not info.is_dir() and Path(info.filename).suffix.lower() in IMAGE_EXTENSIONS
        ]


def main(
    zip_path: Path = typer.Argument(..., help="Path to MMCBNU_6000.zip."),
    output: Path = typer.Option(Path("data/raw/mmcbnu_subset"), "--output", "-o"),
    people: int = typer.Option(8, "--people"),
    samples: int = typer.Option(8, "--samples"),
    source_folder: str = typer.Option("Captured images", "--source-folder"),
    preferred_finger: str = typer.Option("l_fore", "--preferred-finger"),
) -> None:
    if not zip_path.exists():
        raise typer.BadParameter(f"Zip file does not exist: {zip_path}")

    images = _iter_images(zip_path)
    if not images:
        raise typer.BadParameter(f"No image files found in: {zip_path}")

    grouped: dict[tuple[str, str], list[zipfile.ZipInfo]] = defaultdict(list)
    for info in images:
        if source_folder.lower() not in info.filename.lower():
            continue
        person_id = _person_id_from_path(info.filename)
        finger_id = _finger_id_from_path(info.filename)
        grouped[(person_id, finger_id)].append(info)

    by_person: dict[str, list[tuple[str, list[zipfile.ZipInfo]]]] = defaultdict(list)
    for (person_id, finger_id), items in sorted(grouped.items()):
        if len(items) >= samples:
            by_person[person_id].append((finger_id, items))

    selected_groups = []
    for person_id, candidates in sorted(by_person.items()):
        preferred = [candidate for candidate in candidates if candidate[0] == preferred_finger]
        finger_id, items = (preferred or candidates)[0]
        selected_groups.append((person_id, finger_id, sorted(items, key=lambda item: item.filename)))
        if len(selected_groups) >= people:
            break

    if len(selected_groups) < people:
        print(f"[yellow]Only {len(selected_groups)} groups have at least {samples} samples.[/yellow]")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as archive:
        for index, (person_id, finger_id, items) in enumerate(selected_groups, start=1):
            target_dir = output / f"{person_id}_{finger_id}"
            target_dir.mkdir(parents=True, exist_ok=True)
            for sample_index, info in enumerate(items[:samples], start=1):
                suffix = Path(info.filename).suffix.lower()
                target = target_dir / f"sample_{sample_index:02d}{suffix}"
                with archive.open(info) as source, target.open("wb") as destination:
                    shutil.copyfileobj(source, destination)
            print(f"[green]Prepared:[/green] {target_dir} ({samples} samples)")

    print(f"[green]Subset output:[/green] {output}")
    print(f"[green]Groups prepared:[/green] {len(selected_groups)}")


if __name__ == "__main__":
    typer.run(main)

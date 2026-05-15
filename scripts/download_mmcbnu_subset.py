from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen


DATASET_ROWS_URL = (
    "https://datasets-server.huggingface.co/rows"
    "?dataset=luyu0311%2FMMCBNU_6000&config=default&split=train"
)
FINGER_LABELS = ["L_Fore", "L_Middle", "L_Ring", "R_Fore", "R_Middle", "R_Ring"]
ROWS_PER_PERSON = 60
SAMPLES_PER_FINGER = 10


def _read_json(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "nexivo-vein-mvp/0.1"})
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def _download(url: str, output_path: Path) -> None:
    request = Request(url, headers={"User-Agent": "nexivo-vein-mvp/0.1"})
    with urlopen(request, timeout=60) as response:
        output_path.write_bytes(response.read())


def _row_to_target(row_idx: int, output: Path) -> Path:
    person_idx = row_idx // ROWS_PER_PERSON + 1
    within_person = row_idx % ROWS_PER_PERSON
    finger_idx = within_person // SAMPLES_PER_FINGER
    sample_idx = within_person % SAMPLES_PER_FINGER + 1
    finger = FINGER_LABELS[finger_idx]
    return output / f"person_{person_idx:03d}_{finger}" / f"sample_{sample_idx:02d}.jpg"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download a small MMCBNU_6000 subset from Hugging Face into the repo folder format."
    )
    parser.add_argument("--people", type=int, default=5, help="Number of subject blocks to download.")
    parser.add_argument("--output", type=Path, default=Path("data/raw/open_dataset_mmcbnu_5p"))
    parser.add_argument("--offset", type=int, default=0, help="Starting row offset; keep 0 for first subjects.")
    args = parser.parse_args()

    total_rows = args.people * ROWS_PER_PERSON
    rows_url = f"{DATASET_ROWS_URL}&offset={args.offset}&length={total_rows}"
    data = _read_json(rows_url)
    rows = data.get("rows", [])
    if len(rows) != total_rows:
        raise RuntimeError(f"Expected {total_rows} rows, got {len(rows)} from Hugging Face dataset-server.")

    args.output.mkdir(parents=True, exist_ok=True)
    for item in rows:
        row_idx = int(item["row_idx"])
        target = _row_to_target(row_idx, args.output)
        target.parent.mkdir(parents=True, exist_ok=True)

        image = item["row"]["image"]
        label = int(item["row"]["label"])
        expected_label = (row_idx % ROWS_PER_PERSON) // SAMPLES_PER_FINGER
        if label != expected_label:
            print(f"warning: row {row_idx} has label {label}, expected {expected_label}")

        if target.exists():
            print(f"skip {target}")
            continue
        _download(image["src"], target)
        print(f"downloaded {target}")

    print(f"Done: {args.output}")


if __name__ == "__main__":
    main()

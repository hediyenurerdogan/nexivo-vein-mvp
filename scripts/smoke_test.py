from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(command: list[str]) -> None:
    print(f"\n$ {' '.join(command)}")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    synthetic_dir = ROOT / "data" / "raw" / "synthetic_smoke"
    processed_dir = ROOT / "data" / "processed" / "smoke_sample"
    template_dir = ROOT / "data" / "templates_smoke"
    report_path = ROOT / "reports" / "smoke_evaluation.csv"

    for path in [synthetic_dir, processed_dir, template_dir]:
        if path.exists():
            shutil.rmtree(path)
    if report_path.exists():
        report_path.unlink()

    run([PYTHON, "scripts/generate_synthetic_dataset.py", "--output", str(synthetic_dir), "--people", "5", "--samples", "6"])
    run([PYTHON, "scripts/process_image.py", str(synthetic_dir / "person_001" / "sample_01.png"), "--output", str(processed_dir)])
    run([PYTHON, "scripts/enroll.py", "--person-id", "person_001", "--images", str(synthetic_dir / "person_001"), "--db", str(template_dir)])
    run([PYTHON, "scripts/verify.py", str(synthetic_dir / "person_001" / "sample_06.png"), "--db", str(template_dir)])
    run([PYTHON, "scripts/evaluate_folder_dataset.py", str(synthetic_dir), "--db", str(template_dir), "--report", str(report_path)])

    print("\nSmoke test completed.")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()

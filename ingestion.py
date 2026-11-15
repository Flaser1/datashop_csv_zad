

import csv
from pathlib import Path

def read_csv(path: Path, expected_columns: list[str]) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file, delimiter=";", strict=True)
        if reader.fieldnames != expected_columns:
            raise ValueError(f"Unexpected CSV header {reader.fieldnames!r}")

        rows = []
        for record_number, row in enumerate(reader, start=1):
            if None in row or any([value is None for value in row.values()]):
                raise ValueError(f"Wrong number of cells at record {record_number}")
            rows.append(row)

    return rows

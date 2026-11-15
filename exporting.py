

import csv
from pathlib import Path


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def export_orders(output_dir: Path, clean: list[dict], rejected: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "clean_orders.csv",
        clean,
        ["order_id", "customer_name", "status", "amount", "country", "note"],
    )
    write_csv(
        output_dir / "rejected_orders.csv",
        rejected,
        ["source_file", "record_number", "raw_order_id", "error_type", "reason"],
    )

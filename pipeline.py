

from pathlib import Path
from ingestion import read_csv
from transformations import transform_orders
from exporting import export_orders


def run_pipeline(input_path: Path, output_dir: Path, expected_columns: list[str]) -> dict:
    raw_orders = read_csv(input_path, expected_columns)
    clean_orders, rejected_orders = transform_orders(raw_orders, input_path.name)
    export_orders(output_dir, clean_orders, rejected_orders)
    return {
        "source_file": input_path.name,
        "input_rows_count": len(raw_orders),
        "clean_orders": clean_orders,
        "rejected_orders": rejected_orders,
    }


import os
import csv
import pandas as pd


def find_project_root(marker_file: str = "README.md") -> str:
    """
    Find the root directory of the project by looking for a marker file.

    """
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while current_dir != os.path.dirname(current_dir):
        if marker_file in os.listdir(current_dir):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    raise FileNotFoundError(
        f"Marker file '{marker_file}' not found in any parent directories."
    )


ROOT_DIR = find_project_root()


def save_and_append_to_csv(df: pd.DataFrame, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not os.path.exists(output_path):
        df.to_csv(output_path, index=False, mode="w", header=True)
    else:
        df.to_csv(
            output_path,
            index=False,
            mode="a",
            header=False,
            quoting=csv.QUOTE_ALL,
        )

    print(f"Data saved to {output_path}")

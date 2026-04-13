"""Minimal dataset inspection API usage example."""

from __future__ import annotations

from market_data_core.access import inspect_dataset, list_datasets


if __name__ == "__main__":
    root = ".data/market_data"
    print("datasets:", list_datasets(data_root=root))

    # Replace with a real dataset id discovered from list_datasets output.
    # profile = inspect_dataset("cn_equity_1d_raw", data_root=root)
    # print(profile)

    print("Use inspect_dataset(dataset_id, data_root=...) with an existing manifest-backed dataset id.")

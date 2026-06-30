"""
Configuration Loader

Responsibilities:
-----------------
1. Load environment configuration.
2. Load table configuration JSON files.
"""

from __future__ import annotations

import json
import importlib.util
from pathlib import Path
from typing import Dict, List


# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_DIR = PROJECT_ROOT / "config"

TABLE_CONFIG_DIR = PROJECT_ROOT / "table_configs"


# ==========================================================
# Environment Loader
# ==========================================================

def load_environment(environment: str = "dev"):
    """
    Load environment configuration from config/<environment>.py
    """

    config_file = CONFIG_DIR / f"{environment}.py"

    if not config_file.exists():
        raise FileNotFoundError(
            f"Environment config not found: {config_file}"
        )

    spec = importlib.util.spec_from_file_location(
        environment,
        config_file
    )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module


# ==========================================================
# Single Table Configuration
# ==========================================================

def load_table_config(table_name: str) -> Dict:

    config_file = TABLE_CONFIG_DIR / f"{table_name}.json"

    if not config_file.exists():
        raise FileNotFoundError(
            f"Table configuration not found: {config_file}"
        )

    with open(config_file, "r", encoding="utf-8") as file:
        return json.load(file)


# ==========================================================
# All Table Configurations
# ==========================================================

def load_all_table_configs() -> List[Dict]:

    tables = []

    if not TABLE_CONFIG_DIR.exists():
        return tables

    for json_file in sorted(TABLE_CONFIG_DIR.glob("*.json")):

        with open(json_file, "r", encoding="utf-8") as file:
            tables.append(json.load(file))

    return tables


# ==========================================================
# Enabled Tables
# ==========================================================

def load_enabled_tables() -> List[Dict]:

    return [
        table
        for table in load_all_table_configs()
        if table.get("enabled", True)
    ]


# ==========================================================
# Table Names
# ==========================================================

def get_table_names() -> List[str]:

    return [
        table["table_name"]
        for table in load_enabled_tables()
    ]


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    env = load_environment()

    print(f"Environment : {env.ENV}")
    print(f"Bucket      : {env.DATA_LAKE_BUCKET}")

    print("\nConfigured Tables")

    for table in get_table_names():
        print(table)
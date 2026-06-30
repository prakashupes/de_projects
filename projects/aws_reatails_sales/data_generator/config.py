from pathlib import Path

# ===========================
# Data Generation Settings
# ===========================

START_DATE = "2026-06-01"
NUMBER_OF_DAYS = 30
ROWS_PER_DAY = 10000

# Output Folder
BASE_DIR = Path(__file__).parent
OUTPUT_FOLDER = BASE_DIR / "sample_data"

# Random Seed (for reproducibility)
RANDOM_SEED = 42
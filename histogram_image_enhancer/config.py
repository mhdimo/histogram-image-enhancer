from pathlib import Path

PACKAGE_DIR = Path(__file__).parent
RESULTS_DIR = PACKAGE_DIR.parent / "results"
LOG_FILE = PACKAGE_DIR / "logs" / "enhancer.log"

# Create necessary directories upon import
RESULTS_DIR.mkdir(exist_ok=True)
LOG_FILE.parent.mkdir(exist_ok=True)

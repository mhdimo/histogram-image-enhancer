import logging
from pathlib import Path
import cv2
import numpy as np

def setup_logger(name: str, log_file: Path, level: int = logging.INFO) -> logging.Logger:
    """
    Configures a logger with file output.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def load_image(path: Path) -> np.ndarray:
    """
    Loads an image from disk, validating its existence and format.
    """
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File does not exist: {path}")
    img = cv2.imread(str(path))
    if img is None:
        raise ValueError(f"Could not read image (unsupported format or corrupt file): {path}")
    return img

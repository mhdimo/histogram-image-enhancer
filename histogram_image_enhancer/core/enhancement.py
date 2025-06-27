# histogram_image_enhancer/core/enhancement.py

from typing import List, Tuple, Optional

import cv2
import numpy as np

from ..config import LOG_FILE
from .utils import setup_logger

logger = setup_logger(__name__, LOG_FILE)


def equalize_histogram(
    img: np.ndarray,
    channels: List[int] = None
) -> np.ndarray:
    """
    Performs global histogram equalization on all specified channels (or all channels if channels=None).
    """
    if img.ndim == 3:
        chans = channels or [0, 1, 2]
        out = img.copy()
        for c in chans:
            out[:, :, c] = cv2.equalizeHist(img[:, :, c])
    else:
        out = cv2.equalizeHist(img)
    logger.info("Global histogram equalization on channels %s", channels)
    return out


def clahe_enhancement(
    img: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: Tuple[int, int] = (8, 8),
    channels: List[int] = None
) -> np.ndarray:
    """
    Applies CLAHE (Contrast Limited Adaptive Histogram Equalization).
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    if img.ndim == 3:
        chans = channels or [0, 1, 2]
        out = img.copy()
        for c in chans:
            out[:, :, c] = clahe.apply(img[:, :, c])
    else:
        out = clahe.apply(img)
    logger.info(
        "CLAHE applied: clip_limit=%s, tile_grid_size=%s",
        clip_limit, tile_grid_size
    )
    return out


def gamma_correction(
    img: np.ndarray,
    gamma: float = 1.0,
    channels: List[int] = None
) -> np.ndarray:
    """
    Applies gamma correction.
    """
    inv_gamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255
        for i in range(256)
    ], dtype="uint8")

    if img.ndim == 3:
        chans = channels or [0, 1, 2]
        out = img.copy()
        for c in chans:
            out[:, :, c] = cv2.LUT(img[:, :, c], table)
    else:
        out = cv2.LUT(img, table)

    logger.info("Gamma correction applied: gamma=%s", gamma)
    return out


def adjust_contrast(
    img: np.ndarray,
    alpha: float = 1.0,
    beta: float = 0
) -> np.ndarray:
    """
    Applies linear contrast adjustment: output = alpha * img + beta.
    """
    out = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    logger.info("Contrast adjustment applied: alpha=%s, beta=%s", alpha, beta)
    return out


def match_histogram(
    img: np.ndarray,
    reference: np.ndarray
) -> np.ndarray:
    """
    Matches the histogram of img to that of reference.
    """
    if img.ndim != reference.ndim:
        raise ValueError("Source and reference must have the same number of channels")

    out = img.copy()

    # Internal function for one channel
    def _match_channel(src_chan, ref_chan):
        # histograms
        src_hist, _ = np.histogram(src_chan, bins=256, range=(0, 255))
        ref_hist, _ = np.histogram(ref_chan, bins=256, range=(0, 255))
        # normalized CDFs
        src_cdf = np.cumsum(src_hist).astype(np.float64)
        src_cdf /= src_cdf[-1]
        ref_cdf = np.cumsum(ref_hist).astype(np.float64)
        ref_cdf /= ref_cdf[-1]
        # lookup
        lookup = np.zeros(256, dtype=np.uint8)
        for i in range(256):
            j = np.searchsorted(ref_cdf, src_cdf[i], side="left")
            lookup[i] = np.uint8(j)
        # apply
        return lookup[src_chan]

    if img.ndim == 2:
        out = _match_channel(img.flatten(), reference.flatten()).reshape(img.shape)
    else:
        for c in range(img.shape[2]):
            out[:, :, c] = _match_channel(img[:, :, c], reference[:, :, c])

    logger.info("Histogram matching applied")
    return out


def process_image(
    img: np.ndarray,
    method: str = "equalize",
    clip_limit: float = 2.0,
    tile_size: Tuple[int, int] = (8, 8),
    gamma: float = 1.0,
    alpha: float = 1.0,
    beta: float = 0,
    reference: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    Dispatches the specified enhancement method.

    Args:
        img: BGR image as a np.ndarray.
        method: 'equalize', 'clahe', 'gamma', 'contrast' or 'match'.
        clip_limit: for CLAHE.
        tile_size: for CLAHE (width, height).
        gamma: for gamma correction.
        alpha: for linear contrast.
        beta: for linear brightness.
        reference: reference image for histogram matching.

    Returns:
        Processed image.
    """
    if method == "equalize":
        return equalize_histogram(img)
    elif method == "clahe":
        return clahe_enhancement(
            img,
            clip_limit=clip_limit,
            tile_grid_size=tile_size
        )
    elif method == "gamma":
        return gamma_correction(img, gamma=gamma)
    elif method == "contrast":
        return adjust_contrast(img, alpha=alpha, beta=beta)
    elif method == "match":
        if reference is None:
            raise ValueError("Reference image required for histogram matching")
        return match_histogram(img, reference)
    else:
        raise ValueError(f"Unknown method: {method}")

import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

def log_operation(log_file, operation, parameters=None):
    """Log operation to file."""
    with open(log_file, 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {operation}"
        if parameters:
            log_entry += f" - Parametri: {parameters}"
        f.write(log_entry + "\n")

def show_histogram(img, title='Histogram', filename=None):
    """Display image histogram."""
    if len(img.shape) == 3:  # Color image
        colors = ('b', 'g', 'r')
        plt.figure(figsize=(10, 6))
        for i, col in enumerate(colors):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(hist, color=col)
    else:  # Grayscale image
        plt.figure(figsize=(10, 6))
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        plt.plot(hist, color='gray')
    
    plt.title(title)
    plt.xlabel('Pixel intensity')
    plt.ylabel('Pixel count')
    plt.xlim([0, 256])
    
    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

def equalize_histogram(img, channels=None, log_file='image_processing.log'):
    """Equalize image histogram."""
    if len(img.shape) == 3:  # Color image
        if channels is None:
            channels = [0, 1, 2]  # Default: all channels
        
        result = img.copy()
        for ch in channels:
            result[:, :, ch] = cv2.equalizeHist(img[:, :, ch])
        
        log_operation(log_file, 'Histogram equalization', {'channels': channels})
        return result
    else:  # Grayscale image
        log_operation(log_file, 'Histogram equalization')
        return cv2.equalizeHist(img)

def clahe_enhancement(img, clip_limit=2.0, tile_grid_size=(8, 8), channels=None, log_file='image_processing.log'):
    """Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)."""
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    
    if len(img.shape) == 3:  # Color image
        if channels is None:
            channels = [0, 1, 2]  # Default: all channels
        
        result = img.copy()
        for ch in channels:
            result[:, :, ch] = clahe.apply(img[:, :, ch])
        
        log_operation(log_file, 'CLAHE enhancement', {'clip_limit': clip_limit, 'tile_grid_size': tile_grid_size, 'channels': channels})
        return result
    else:  # Grayscale image
        log_operation(log_file, 'CLAHE enhancement', {'clip_limit': clip_limit, 'tile_grid_size': tile_grid_size})
        return clahe.apply(img)

def gamma_correction(img, gamma=1.0, channels=None, log_file='image_processing.log'):
    """Apply gamma correction to image."""
    lookup_table = np.zeros((1, 256), dtype=np.uint8)
    for i in range(256):
        lookup_table[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    
    if len(img.shape) == 3:  # Color image
        if channels is None:
            channels = [0, 1, 2]  # Default: all channels
        
        result = img.copy()
        for ch in channels:
            result[:, :, ch] = cv2.LUT(img[:, :, ch], lookup_table)
        
        log_operation(log_file, 'Gamma correction', {'gamma': gamma, 'channels': channels})
        return result
    else:  # Grayscale image
        log_operation(log_file, 'Gamma correction', {'gamma': gamma})
        return cv2.LUT(img, lookup_table)

def process_image(img, method='equalize', clip_limit=2.0, tile_size=(8,8), gamma=1.0, log_file='image_processing.log'):
    """
    Process image using specified enhancement method.
    
    Args:
        img: Input image (BGR format)
        method: Enhancement method ('equalize', 'clahe', 'gamma')
        clip_limit: CLAHE clip limit (default: 2.0)
        tile_size: CLAHE tile size (default: 8x8)
        gamma: Gamma correction value (default: 1.0)
        log_file: Path to log file (default: 'image_processing.log')
    
    Returns:
        Processed image
    """
    if method == 'equalize':
        return equalize_histogram(img, log_file=log_file)
    elif method == 'clahe':
        return clahe_enhancement(img, clip_limit, tile_size, log_file=log_file)
    elif method == 'gamma':
        return gamma_correction(img, gamma, log_file=log_file)
    else:
        raise ValueError(f"Unknown method: {method}")
from pathlib import Path
import matplotlib.pyplot as plt
import cv2
import numpy as np

def save_comparison(
    original: np.ndarray,
    processed: np.ndarray,
    out_path: Path,
    titles: tuple = ("Original", "Processed")
) -> None:
    """
    Generates a 2×2 figure with the original image, the processed image, and their histograms,
    and saves it to out_path.
    """
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # Display images
    for ax, img, title in zip(axs[0], (original, processed), titles):
        cmap = None if img.ndim == 3 else "gray"
        disp = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if img.ndim == 3 else img
        ax.imshow(disp, cmap=cmap)
        ax.set_title(title)
        ax.axis("off")

    # Generic function for histograms
    def plot_histogram(ax, img):
        channels = range(img.shape[2]) if img.ndim == 3 else [0]
        colors = ("b", "g", "r") if img.ndim == 3 else ("k",)
        for channel, col in zip(channels, colors):
            hist = cv2.calcHist([img], [channel], None, [256], [0, 256])
            # Normalize histogram to prevent spikes and show proper distribution
            hist = hist.flatten() / hist.sum()
            # Use proper x-axis values (0-255) instead of indices
            x_values = np.arange(256)
            ax.plot(x_values, hist, color=col, alpha=0.7)
        ax.set_xlim(0, 255)
        ax.set_ylabel('Normalized Frequency')
        ax.set_xlabel('Pixel Intensity')

    plot_histogram(axs[1, 0], original)
    axs[1, 0].set_title("Original Histogram")
    plot_histogram(axs[1, 1], processed)
    axs[1, 1].set_title("Processed Histogram")

    plt.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)

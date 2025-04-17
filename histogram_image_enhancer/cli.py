import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pick
import logging
import os
from datetime import datetime
from .process_image import process_image, show_histogram

def create_comparison(original, processed, title1="Original", title2="Processed"):
    """Create comparison image with histograms."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Image display
    if len(original.shape) == 3:
        axes[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
        axes[0, 1].imshow(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
    else:
        axes[0, 0].imshow(original, cmap='gray')
        axes[0, 1].imshow(processed, cmap='gray')
    
    axes[0, 0].set_title(title1)
    axes[0, 1].set_title(title2)
    axes[0, 0].axis('off')
    axes[0, 1].axis('off')
    
    # Histograms
    if len(original.shape) == 3:  # Color image
        colors = ('b', 'g', 'r')
        for i, col in enumerate(colors):
            hist_original = cv2.calcHist([original], [i], None, [256], [0, 256])
            hist_processed = cv2.calcHist([processed], [i], None, [256], [0, 256])
            axes[1, 0].plot(hist_original, color=col)
            axes[1, 1].plot(hist_processed, color=col)
    else:  # Grayscale
        hist_original = cv2.calcHist([original], [0], None, [256], [0, 256])
        hist_processed = cv2.calcHist([processed], [0], None, [256], [0, 256])
        axes[1, 0].plot(hist_original, color='black')
        axes[1, 1].plot(hist_processed, color='black')
    
    axes[1, 0].set_title(f"Histogram {title1}")
    axes[1, 1].set_title(f"Histogram {title2}")
    axes[1, 0].set_xlim([0, 256])
    axes[1, 1].set_xlim([0, 256])
    
    plt.tight_layout()
    return fig

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='histogram_enhancer.log',
        filemode='a'
    )
    return logging.getLogger('histogram_enhancer')

def get_user_input(logger, input_file):
    # Validate input file exists and is readable
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    if not os.path.isfile(input_file):
        raise ValueError(f"Path is not a file: {input_file}")
    
    # Normalize path for Windows and check image format
    input_file = os.path.normpath(input_file)
    try:
        img = cv2.imread(input_file)
        if img is None:
            raise ValueError(f"Could not read image {input_file}. Supported formats: JPG, PNG, BMP, etc.")
    except Exception as e:
        raise ValueError(f"Error reading image: {str(e)}")
    
    # Select method
    method_options = ['equalize', 'clahe', 'gamma']
    method_title = 'Select enhancement method:'
    method, _ = pick.pick(method_options, method_title)
    logger.info(f'User selected method: {method}')
    
    # Get parameters based on method
    params = {}
    if method == 'clahe':
        clip_limit = float(input('Enter CLAHE clip limit (default 2.0): ') or 2.0)
        tile_size = input('Enter CLAHE tile size as "width height" (default 8 8): ') or "8 8"
        tile_size = list(map(int, tile_size.split()))
        params.update({'clip_limit': clip_limit, 'tile_size': tile_size})
        logger.info(f'User set CLAHE parameters: {params}')
    elif method == 'gamma':
        gamma = float(input('Enter gamma value (default 1.0): ') or 1.0)
        params.update({'gamma': gamma})
        logger.info(f'User set gamma parameter: {params}')
    
    return input_file, 'output.jpg', method, params

def main():
    logger = setup_logging()
    logger.info('Histogram Enhancer started')
    
    # Create results directory if it doesn't exist
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    parser = argparse.ArgumentParser(description='Histogram image enhancer')
    parser.add_argument('input_file', help='Path to input image file')
    args = parser.parse_args()
    
    try:
        input_file, output_file, method, params = get_user_input(logger, args.input_file)
        output_file = os.path.join(results_dir, output_file)
    except Exception as e:
        logger.error(f"Error getting user input: {e}")
        print(f"Error: {e}")
        return 1
    
    # Read input image
    img = cv2.imread(input_file)
    if img is None:
        logger.error(f"Could not read image {input_file}")
        print(f"Error: Could not read image {input_file}")
        return 1
    
    # Process image
    result = process_image(img, method=method, 
                          clip_limit=params.get('clip_limit', 2.0), 
                          tile_size=params.get('tile_size', [8, 8]),
                          gamma=params.get('gamma', 1.0))
    
    # Save output
    cv2.imwrite(output_file, result)
    logger.info(f"Successfully processed image saved to {output_file}")
    print(f"Successfully processed image saved to {output_file}")
    
    # Show and save comparison
    comparison_fig = create_comparison(img, result)
    comparison_path = os.path.join(results_dir, 'output_comparison.png')
    comparison_fig.savefig(comparison_path)
    plt.close(comparison_fig)
    logger.info(f"Saved comparison image to {comparison_path}")
    
    logger.info('Histogram Enhancer completed successfully')
    
    return 0

if __name__ == "__main__":
    main()
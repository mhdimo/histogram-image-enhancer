import unittest
import cv2
import numpy as np
import os

from histogram_image_enhancer import process_image

class TestImageProcessing(unittest.TestCase):
    def setUp(self):
        # Create a simple test image
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.test_image[25:75, 25:75] = 128
        self.output_path = "test_output.jpg"
    
    def tearDown(self):
        # Clean up output file if it exists
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
    
    def test_histogram_equalization(self):
        """Test basic histogram equalization."""
        result = process_image(self.test_image, method="equalize")
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_clahe(self):
        """Test CLAHE processing."""
        result = process_image(self.test_image, method="clahe", clip_limit=2.0, tile_size=(8,8))
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_gamma_correction(self):
        """Test gamma correction."""
        result = process_image(self.test_image, method="gamma", gamma=0.5)
        self.assertEqual(result.shape, self.test_image.shape)

if __name__ == "__main__":
    unittest.main()
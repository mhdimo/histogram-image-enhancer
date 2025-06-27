import numpy as np
import pytest

from histogram_image_enhancer.core.enhancement import process_image

@pytest.fixture
def test_image():
    # 100x100 with a gray square (value 128)
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[25:75, 25:75] = 128
    return img

def test_equalize(test_image):
    result = process_image(test_image, method="equalize")
    assert result.shape == test_image.shape

def test_clahe(test_image):
    result = process_image(test_image, method="clahe",
                           clip_limit=2.0, tile_size=(8, 8))
    assert result.shape == test_image.shape

def test_gamma(test_image):
    result = process_image(test_image, method="gamma", gamma=0.5)
    assert result.shape == test_image.shape

def test_contrast(test_image):
    result = process_image(test_image, method="contrast",
                           alpha=2.0, beta=10)
    assert result.shape == test_image.shape

def test_match_identity(test_image):
    # With the same reference image, it should return an identical image
    result = process_image(test_image, method="match", reference=test_image)
    assert result.shape == test_image.shape
    assert np.array_equal(result, test_image)

import pytest
import numpy as np
import cv2
from src.ocr.processor import ImagePreprocessor
import os

def test_contrast_enhancement():
    # Create a dummy image
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    enhanced = ImagePreprocessor.enhance_contrast(img)
    assert enhanced.shape == (100, 100)
    assert enhanced.dtype == np.uint8

def test_denoise():
    img = np.zeros((100, 100), dtype=np.uint8)
    denoised = ImagePreprocessor.denoise(img)
    assert denoised.shape == (100, 100)

def test_preprocessing_pipeline(tmp_path):
    img_path = tmp_path / "test.jpg"
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite(str(img_path), img)
    
    processed = ImagePreprocessor.process(str(img_path))
    assert processed is not None
    assert len(processed.shape) == 2 # Grayscale

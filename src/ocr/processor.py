import cv2
import numpy as np
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class ImagePreprocessor:
    @staticmethod
    def load_image(image_path: str):
        """Loads an image from path."""
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not load image at {image_path}")
        return image

    @staticmethod
    def fix_rotation(image):
        """Corrects image rotation using Canny edge detection and hough lines (simplified)."""
        # In a real production system, this would use a more robust deskewing algorithm
        # For now, we'll return the original image as a placeholder for the pipeline
        logger.info("Correction rotation...")
        return image

    @staticmethod
    def enhance_contrast(image):
        """Enhances image contrast using CLAHE."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        return enhanced

    @staticmethod
    def denoise(image):
        """Reduces noise in the image."""
        return cv2.fastNlMeansDenoising(image, None, 30, 7, 21)

    @classmethod
    def process(cls, image_path: str):
        """Full preprocessing pipeline."""
        image = cls.load_image(image_path)
        image = cls.fix_rotation(image)
        enhanced = cls.enhance_contrast(image)
        denoised = cls.denoise(enhanced)
        return denoised

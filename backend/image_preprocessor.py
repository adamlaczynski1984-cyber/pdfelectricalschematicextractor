import cv2
import numpy as np
from PIL import Image


class ImagePreprocessor:
    def __init__(self, dpi: int = 200):
        self.dpi = dpi

    def preprocess(self, image: Image.Image) -> Image.Image:
        cv_image = self._pil_to_cv(image)

        cv_image = self._grayscale(cv_image)
        cv_image = self._denoise(cv_image)
        cv_image = self._threshold(cv_image)
        cv_image = self._sharpen(cv_image)
        cv_image = self._deskew(cv_image)

        return self._cv_to_pil(cv_image)

    def _pil_to_cv(self, image: Image.Image) -> np.ndarray:
        rgb_image = np.array(image)
        return cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

    def _cv_to_pil(self, cv_image: np.ndarray) -> Image.Image:
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_image)

    def _grayscale(self, image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def _denoise(self, image: np.ndarray) -> np.ndarray:
        return cv2.fastNlMeansDenoising(
            image,
            h=10,
            templateWindowSize=7,
            searchWindowSize=21,
        )

    def _threshold(self, image: np.ndarray) -> np.ndarray:
        return cv2.adaptiveThreshold(
            image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=11,
            C=2,
        )

    def _sharpen(self, image: np.ndarray) -> np.ndarray:
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0],
        ], dtype=np.float32)

        return cv2.filter2D(image, -1, kernel)

    def _deskew(self, image: np.ndarray) -> np.ndarray:
        coords = np.column_stack(np.where(image > 0))

        if len(coords) == 0:
            return image

        angle = cv2.minAreaRect(coords)[2]

        if angle < -45:
            angle = 90 + angle

        if angle > 10 or angle < -10:
            h, w = image.shape
            center = (w // 2, h // 2)
            matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            image = cv2.warpAffine(
                image,
                matrix,
                (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE,
            )

        return image

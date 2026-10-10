from typing import List, Dict, Any

import pytesseract
from pdf2image import convert_from_path

from .image_preprocessor import ImagePreprocessor


class PDFProcessor:
    def __init__(self, dpi: int = 200):
        self.dpi = dpi
        self.preprocessor = ImagePreprocessor(dpi=dpi)

    def process_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        pages: List[Dict[str, Any]] = []

        try:
            images = convert_from_path(pdf_path, dpi=self.dpi)
        except Exception as exc:
            raise RuntimeError(f"Nie można przekonwertować PDF do obrazów: {exc}") from exc

        for page_number, image in enumerate(images, start=1):
            processed_image = self.preprocessor.preprocess(image)

            text = pytesseract.image_to_string(
                processed_image,
                config="--psm 6 --oem 3",
            )

            pages.append({
                "page_number": page_number,
                "text": text,
                "image": processed_image,
            })

        return pages

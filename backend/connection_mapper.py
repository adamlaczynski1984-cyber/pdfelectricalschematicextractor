import re
from typing import Any, Dict, List

from .page_processor import MultiPageConnectionProcessor


class ConnectionMapper:
    def __init__(self):
        self.processor = MultiPageConnectionProcessor()

    def extract_connections(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return self.processor.build_connections(pages)

    def build_device_summary(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        device_map: Dict[str, Dict[str, Any]] = {}

        for page in pages:
            text = page.get("text", "")
            for token in re.findall(r"\b([A-Z]{1,6}[0-9]{0,4}[A-Z0-9]{0,4})\b", text):
                if not self._is_probable_device(token):
                    continue

                device = token.strip()
                if device not in device_map:
                    device_map[device] = {
                        "device": device,
                        "pages": set(),
                        "terminals": set(),
                    }

                device_map[device]["pages"].add(page["page_number"])

                for _, terminal in re.findall(r"([A-Z0-9]+)\s*(?:[:.-]|\s)\s*([0-9]{1,3}[A-Z0-9]{0,3})", text):
                    if terminal:
                        device_map[device]["terminals"].add(terminal)

        result = []
        for device, data in device_map.items():
            result.append({
                "device": device,
                "pages": sorted(data["pages"]),
                "terminals": sorted(data["terminals"]),
            })

        return sorted(result, key=lambda item: item["device"])

    def _is_probable_device(self, value: str) -> bool:
        if len(value) < 2:
            return False
        if value.isdigit():
            return False
        return bool(re.fullmatch(r"[A-Z]{1,6}[0-9]{0,4}[A-Z0-9]{0,4}", value))

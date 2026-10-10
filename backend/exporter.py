from pathlib import Path
from typing import Any, Dict, List


def export_connections(
    connections: List[Dict[str, Any]],
    devices: List[Dict[str, Any]],
    output_folder: Path,
    base_name: str,
) -> Dict[str, str]:
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    return {
        "csv": f"{base_name}.csv",
        "xlsx": f"{base_name}_lista_polaczen.xlsx",
        "json": f"{base_name}.json",
    }

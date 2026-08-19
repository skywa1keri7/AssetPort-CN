from dataclasses import dataclass, asdict
import json 
from pathlib import Path

SUPPORTED_LANGUAGES = {"zh_CN", "en_US"}

@dataclass

class ImporterSettings():
    parent_material_opaque : str ="/Game/Python/Materials/M_Master_Opaque"
    parent_material_masked : str ="/Game/Python/Materials/M_Master_Masked"
    parent_material_translucent : str = "/Game/Python/Materials/M_Master_Translucent"
    auto_create_mi : bool = True
    auto_assign_to_mesh : bool = True
    replace_existing : bool = False
    organize_asset : bool = True
    language : str = "zh_CN"

def config_loader():
    settings = ImporterSettings()
    config_file = Path(__file__).parent.parent / "importer_config.json"

    if not config_file.exists():
        save_config(settings)
        return settings

    try:
        with open(config_file, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return settings

    known_fields = asdict(settings)
    known_fields.update({key: value for key, value in data.items() if key in known_fields})
    if known_fields["language"] not in SUPPORTED_LANGUAGES:
        known_fields["language"] = settings.language
    return ImporterSettings(**known_fields)


def save_config(settings: ImporterSettings):
    config_file = Path(__file__).parent.parent / "importer_config.json"
    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(asdict(settings), file, ensure_ascii=False, indent=4)

from dataclasses import dataclass, asdict
import json 
from pathlib import Path

SUPPORTED_LANGUAGES = {"zh_CN", "en_US"}

@dataclass

class ImporterSettings():
    parent_material_opaque : str ="/Game/Python/Materials/M_Master_Opaque"
    parent_material_masked : str ="/Game/Python/Materials/M_Master_Masked"
    parent_material_translucent : str = "/Game/Python/Materials/M_Master_Translucent"
    parent_material_decal : str = "/Game/Python/Materials/M_Master_Decal"
    auto_create_mi : bool = True
    auto_create_material_fallback : bool = True
    auto_configure_textures : bool = True
    auto_assign_to_mesh : bool = True
    replace_existing : bool = False
    organize_asset : bool = True
    language : str = "zh_CN"
    opacity_mask_clip_value : float = 0.333
    auto_import_lods : bool = True

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
    try:
        known_fields["opacity_mask_clip_value"] = max(
            0.0, min(1.0, float(known_fields["opacity_mask_clip_value"]))
        )
    except (TypeError, ValueError):
        known_fields["opacity_mask_clip_value"] = settings.opacity_mask_clip_value
    return ImporterSettings(**known_fields)


def save_config(settings: ImporterSettings):
    config_file = Path(__file__).parent.parent / "importer_config.json"
    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(asdict(settings), file, ensure_ascii=False, indent=4)

"""Create and remove one temporary material to verify UE graph editing APIs."""

import sys
import uuid
from pathlib import Path
from types import SimpleNamespace

import unreal


repository_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repository_root))
for module_name in tuple(sys.modules):
    if module_name == "asset_port" or module_name.startswith("asset_port."):
        del sys.modules[module_name]

from asset_port.config import ImporterSettings  # noqa: E402
from asset_port.materials import _configure_generated_material  # noqa: E402
from asset_port.models import TextureSlot  # noqa: E402


asset_name = f"M_AssetPortCN_Smoke_{uuid.uuid4().hex[:8]}"
package_path = "/Game/__AssetPortCN_Smoke"
asset_path = f"{package_path}/{asset_name}"
material = None

try:
    material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name=asset_name,
        package_path=package_path,
        asset_class=unreal.Material,
        factory=unreal.MaterialFactoryNew(),
    )
    if material is None:
        raise RuntimeError("Could not create temporary smoke-test material")

    texture_path = "/Game/Python/Materials/T_Default_White_VT"
    if not unreal.EditorAssetLibrary.load_asset(texture_path):
        raise RuntimeError(f"Required smoke-test texture is missing: {texture_path}")

    textures = [
        SimpleNamespace(
            ue_path=texture_path,
            texture_slot=TextureSlot.BASE_COLOUR,
            has_alpha=False,
        ),
        SimpleNamespace(
            ue_path=texture_path,
            texture_slot=TextureSlot.OPACITY_MASK,
            has_alpha=False,
        ),
    ]
    _configure_generated_material(material, textures, "Masked", ImporterSettings())
    unreal.log("AssetPort-CN generated-material graph smoke test passed.")
finally:
    if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        unreal.EditorAssetLibrary.delete_asset(asset_path)

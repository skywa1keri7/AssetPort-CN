"""Run with UnrealEditor-Cmd to verify the package inside Unreal Python."""

import sys
from pathlib import Path

import unreal


repository_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repository_root))
for module_name in tuple(sys.modules):
    if module_name == "asset_port" or module_name.startswith("asset_port."):
        del sys.modules[module_name]

from asset_port.localization import category_options, tr  # noqa: E402
from asset_port import materials  # noqa: E402,F401
from asset_port.ui_localization import localize_main_widget  # noqa: E402,F401


assert tr("app.name")
assert len(category_options()) == 5
assert hasattr(unreal.MaterialEditingLibrary, "create_material_expression")
assert hasattr(unreal.MaterialEditingLibrary, "connect_material_property")
assert hasattr(unreal.MaterialEditingLibrary, "recompile_material")
assert hasattr(unreal.MaterialProperty, "MP_OPACITY_MASK")
assert hasattr(unreal.TextureCompressionSettings, "TC_MASKS")

required_assets = (
    "/Game/Python/Widgets/EUW_AssetPort",
    "/Game/Python/Widgets/EUW_AssetPort_Preview",
    "/Game/Python/Widgets/EUW_TransparencySetup",
)
missing_assets = [path for path in required_assets if not unreal.load_asset(path)]
if missing_assets:
    raise RuntimeError(f"AssetPort-CN missing required assets: {missing_assets}")

unreal.log("AssetPort-CN Unreal smoke test passed.")

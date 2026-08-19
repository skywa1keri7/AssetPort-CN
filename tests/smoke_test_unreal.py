"""Run with UnrealEditor-Cmd to verify the package inside Unreal Python."""

import sys
from pathlib import Path

import unreal


repository_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repository_root))

from asset_port.localization import category_options, tr  # noqa: E402
from asset_port.ui_localization import localize_main_widget  # noqa: E402,F401


assert tr("app.name")
assert len(category_options()) == 5

required_assets = (
    "/Game/Python/Widgets/EUW_AssetPort",
    "/Game/Python/Widgets/EUW_AssetPort_Preview",
    "/Game/Python/Widgets/EUW_TransparencySetup",
)
missing_assets = [path for path in required_assets if not unreal.load_asset(path)]
if missing_assets:
    raise RuntimeError(f"AssetPort-CN missing required assets: {missing_assets}")

unreal.log("AssetPort-CN Unreal smoke test passed.")


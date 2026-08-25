"""Exercise the importer path against the bundled bilingual master."""

from types import SimpleNamespace

import unreal

from asset_port.material_parameters import bilingual_parameter_name
from asset_port.materials import _create_material_instance
from asset_port.models import TextureSlot


parent = unreal.EditorAssetLibrary.load_asset("/Game/Python/Materials/M_Master_Opaque")
assert parent is not None
texture_path = "/Engine/EngineResources/DefaultTexture"
texture = SimpleNamespace(
    texture_slot=TextureSlot.BASE_COLOUR,
    ue_path=texture_path,
    has_alpha=False,
)
config = SimpleNamespace(replace_existing=False)

instance, _, assigned = _create_material_instance(
    "MI_BilingualBinding",
    "/Game/AssetPortSmoke",
    [texture],
    "Opaque",
    parent,
    config,
)
assert instance is not None
parameter_name = bilingual_parameter_name("BaseColour")
assert assigned == {parameter_name: texture_path}, assigned
assert (
    unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(
        instance, parameter_name
    )
    == unreal.EditorAssetLibrary.load_asset(texture_path)
)
unreal.log("AssetPort-CN bilingual material binding smoke test passed.")

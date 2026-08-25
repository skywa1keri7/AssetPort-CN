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

decal_parent = unreal.EditorAssetLibrary.load_asset(
    "/Game/Python/Materials/M_Master_Decal"
)
assert decal_parent is not None
decal_instance_path = "/Game/AssetPortSmoke/MI_BilingualDecalOpacityBinding"
if unreal.EditorAssetLibrary.does_asset_exist(decal_instance_path):
    unreal.EditorAssetLibrary.delete_asset(decal_instance_path)

opacity_texture = SimpleNamespace(
    texture_slot=TextureSlot.OPACITY,
    ue_path=texture_path,
    has_alpha=False,
)
decal_instance, _, decal_assigned = _create_material_instance(
    "MI_BilingualDecalOpacityBinding",
    "/Game/AssetPortSmoke",
    [opacity_texture],
    "Decal",
    decal_parent,
    config,
)
assert decal_instance is not None
opacity_mask_parameter = bilingual_parameter_name("OpacityMask")
assert decal_assigned == {opacity_mask_parameter: texture_path}, decal_assigned
assert (
    unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(
        decal_instance, opacity_mask_parameter
    )
    == unreal.EditorAssetLibrary.load_asset(texture_path)
)
assert unreal.EditorAssetLibrary.delete_asset(decal_instance_path)
unreal.log("AssetPort-CN Decal opacity binding smoke test passed.")

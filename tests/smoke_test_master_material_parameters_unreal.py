"""Verify bundled bilingual identifiers and legacy alias resolution."""

import unreal

from asset_port.material_parameters import bilingual_parameter_name


material_paths = (
    "/Game/Python/Materials/M_Master_Opaque",
    "/Game/Python/Materials/M_Master_Masked",
    "/Game/Python/Materials/M_Master_Translucent",
    "/Game/Python/Materials/M_Master_Decal",
)
required_textures = {
    bilingual_parameter_name(name) for name in ("BaseColour", "Normal", "Roughness")
}
required_switches = {bilingual_parameter_name(name) for name in ("UseORM", "UseVT")}
editing = unreal.MaterialEditingLibrary

for path in material_paths:
    material = unreal.EditorAssetLibrary.load_asset(path)
    assert material is not None, f"Missing master material: {path}"

    texture_names = {str(name) for name in editing.get_texture_parameter_names(material)}
    switch_names = {str(name) for name in editing.get_static_switch_parameter_names(material)}
    assert required_textures.issubset(texture_names), (path, texture_names)
    assert required_switches.issubset(switch_names), (path, switch_names)

unreal.log("AssetPort-CN master-material parameter compatibility smoke test passed.")

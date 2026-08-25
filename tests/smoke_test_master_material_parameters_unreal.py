"""Verify that bilingual master-material edits preserve binding identifiers."""

import unreal


material_paths = (
    "/Game/Python/Materials/M_Master_Opaque",
    "/Game/Python/Materials/M_Master_Masked",
    "/Game/Python/Materials/M_Master_Translucent",
    "/Game/Python/Materials/M_Master_Decal",
)
required_textures = {"BaseColour", "Normal", "Roughness"}
required_switches = {"UseORM", "UseVT"}
editing = unreal.MaterialEditingLibrary

for path in material_paths:
    material = unreal.EditorAssetLibrary.load_asset(path)
    assert material is not None, f"Missing master material: {path}"

    texture_names = {str(name) for name in editing.get_texture_parameter_names(material)}
    switch_names = {str(name) for name in editing.get_static_switch_parameter_names(material)}
    assert required_textures.issubset(texture_names), (path, texture_names)
    assert required_switches.issubset(switch_names), (path, switch_names)

unreal.log("AssetPort-CN master-material parameter compatibility smoke test passed.")

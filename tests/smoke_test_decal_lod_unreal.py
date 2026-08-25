import unreal

from asset_port.config import config_loader
from asset_port.localization import blend_options, blend_to_internal
from asset_port.materials import _configure_generated_material


config = config_loader()
assert config.auto_import_lods is True
assert config.parent_material_decal == "/Game/Python/Materials/M_Master_Decal"

internal_modes = [blend_to_internal(value) for value in blend_options()]
assert internal_modes == ["Masked", "Translucent", "Decal", "Opaque"]

fbx = unreal.FbxImportUI()
fbx.static_mesh_import_data.import_mesh_lods = True
assert bool(fbx.static_mesh_import_data.import_mesh_lods) is True

subsystem_class = getattr(unreal, "StaticMeshEditorSubsystem", None)
assert subsystem_class is not None
subsystem = unreal.get_editor_subsystem(subsystem_class)
legacy = getattr(unreal, "EditorStaticMeshLibrary", None)
unreal.log(
    f"ASSET_PORT_LOD_SUBSYSTEM: {[name for name in dir(subsystem) if 'lod' in name.lower()]}"
)
unreal.log(
    f"ASSET_PORT_LOD_LEGACY: {[name for name in dir(legacy) if 'lod' in name.lower()]}"
)
assert (
    subsystem is not None and hasattr(subsystem, "import_lod")
) or (legacy is not None and hasattr(legacy, "import_lod"))

decal_master = unreal.EditorAssetLibrary.load_asset(config.parent_material_decal)
assert decal_master is not None
assert decal_master.get_editor_property("material_domain") == unreal.MaterialDomain.MD_DEFERRED_DECAL

test_root = "/Game/AssetPortCNTests"
test_path = f"{test_root}/M_DecalFallback_Smoke"
if unreal.EditorAssetLibrary.does_asset_exist(test_path):
    unreal.EditorAssetLibrary.delete_asset(test_path)
material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
    "M_DecalFallback_Smoke",
    test_root,
    unreal.Material,
    unreal.MaterialFactoryNew(),
)
assert material is not None
_configure_generated_material(material, [], "Decal", config)
assert material.get_editor_property("material_domain") == unreal.MaterialDomain.MD_DEFERRED_DECAL
assert material.get_editor_property("blend_mode") == unreal.BlendMode.BLEND_TRANSLUCENT
assert unreal.EditorAssetLibrary.delete_asset(test_path)

unreal.log("AssetPort-CN Decal and LOD smoke test passed.")

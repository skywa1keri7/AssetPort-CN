import unreal
from asset_port.models import DetectedAsset, AssetType, TextureSlot
from asset_port.material_rules import texture_profile

def get_mesh_setting(asset: DetectedAsset):
    
    fbx = unreal.FbxImportUI()
    
    fbx.import_materials = False
    fbx.import_textures = False
    
    if asset.asset_type == AssetType.STATIC_MESH :
        fbx.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
        # Imports LOD groups embedded in a single FBX. Separately exported
        # ``_LOD1`` files are attached after the base mesh import.
        static_mesh = fbx.static_mesh_import_data
        try:
            static_mesh.import_mesh_lods = True
        except Exception:
            pass
        static_mesh.combine_meshes = True
        static_mesh.generate_lightmap_u_vs = True
        
    elif asset.asset_type == AssetType.SKELETAL_MESH:
      fbx.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH  
      skeletal_mesh = fbx.skeletal_mesh_import_data
      skeletal_mesh.import_content_type =  unreal.FBXImportContentType.FBXICT_GEOMETRY
      
    else:
        fbx.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH


    return fbx



def texture_settings(texture_asset, slot: TextureSlot):
    profile = texture_profile(slot)
    if profile is None:
        return False

    compression_name, srgb = profile
    compression_values = {
        "default": unreal.TextureCompressionSettings.TC_DEFAULT,
        "normal": unreal.TextureCompressionSettings.TC_NORMALMAP,
        "masks": unreal.TextureCompressionSettings.TC_MASKS,
        "alpha": unreal.TextureCompressionSettings.TC_ALPHA,
    }
    texture_asset.set_editor_property("srgb", srgb)
    texture_asset.set_editor_property("compression_settings", compression_values[compression_name])
    return True

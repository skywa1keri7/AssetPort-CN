import unreal

from asset_port.config import ImporterSettings
from asset_port.material_rules import automatic_blend_mode, material_connections
from asset_port.models import AssetGroup, AtlasGroup, MaterialBuildResult, TextureSlot


MATERIAL_PROPERTIES = {
    "base_color": "MP_BASE_COLOR",
    "normal": "MP_NORMAL",
    "roughness": "MP_ROUGHNESS",
    "metallic": "MP_METALLIC",
    "ambient_occlusion": "MP_AMBIENT_OCCLUSION",
    "specular": "MP_SPECULAR",
    "emissive_color": "MP_EMISSIVE_COLOR",
    "opacity": "MP_OPACITY",
    "opacity_mask": "MP_OPACITY_MASK",
}


def _blend_mode_for(mi_name, textures, decisions):
    if decisions and mi_name in decisions:
        return decisions[mi_name]
    return automatic_blend_mode(textures)


def _master_path(blend_mode, config):
    if blend_mode == "Masked":
        return config.parent_material_masked
    if blend_mode == "Translucent":
        return config.parent_material_translucent
    if blend_mode == "Decal":
        return config.parent_material_decal
    return config.parent_material_opaque


def _is_skeletal_mesh(mesh_object):
    skeletal_mesh_class = getattr(unreal, "SkeletalMesh", None)
    return skeletal_mesh_class is not None and isinstance(mesh_object, skeletal_mesh_class)


def _assign_material_at_index(mesh_object, index, material):
    """Assign a material without relying on StaticMesh-only APIs."""
    if not _is_skeletal_mesh(mesh_object):
        mesh_object.set_material(index, material)
        return True

    skeletal_materials = mesh_object.get_editor_property("materials")
    if index >= len(skeletal_materials):
        return False

    current = skeletal_materials[index]
    replacement = unreal.SkeletalMaterial()
    # Preserve slot metadata when rebuilding the struct. UE returns skeletal
    # material entries by value, so mutating the old entry is not reliable.
    for property_name in (
        "material_slot_name",
        "imported_material_slot_name",
        "uv_channel_data",
        "enable_shadow_casting",
        "recompute_tangent",
    ):
        try:
            replacement.set_editor_property(
                property_name, current.get_editor_property(property_name)
            )
        except Exception:
            pass
    replacement.set_editor_property("material_interface", material)
    skeletal_materials[index] = replacement
    mesh_object.set_editor_property("materials", skeletal_materials)
    return True


def _assign_material(mesh_object, material, group, slot_name, config, blend_mode="Opaque"):
    # Deferred decal materials belong on Decal Actors/Components, not in a
    # Static Mesh material slot.
    if blend_mode == "Decal" or not mesh_object or not config.auto_assign_to_mesh:
        return False

    if group.is_multi_material:
        material_slots = mesh_object.get_editor_property(
            "materials" if _is_skeletal_mesh(mesh_object) else "static_materials"
        )
        for index, mat_slot in enumerate(material_slots):
            mesh_slot = str(mat_slot.get_editor_property("material_slot_name"))
            if slot_name.lower() in mesh_slot.lower() or mesh_slot.lower() in slot_name.lower():
                if not _assign_material_at_index(mesh_object, index, material):
                    return False
                unreal.log(
                    f"AssetPort: Assigned {material.get_name()} to slot [{index}] '{slot_name}'"
                )
                unreal.EditorAssetLibrary.save_loaded_asset(mesh_object)
                return True
        return False

    if not _assign_material_at_index(mesh_object, 0, material):
        return False
    unreal.EditorAssetLibrary.save_loaded_asset(mesh_object)
    return True


def _set_sampler_type(expression, texture, slot):
    is_virtual = bool(texture.get_editor_property("virtual_texture_streaming"))
    if slot == TextureSlot.NORMAL:
        enum_name = "SAMPLERTYPE_VIRTUAL_NORMAL" if is_virtual else "SAMPLERTYPE_NORMAL"
    elif slot in (
        TextureSlot.ROUGHNESS,
        TextureSlot.METALLIC,
        TextureSlot.AO,
        TextureSlot.CAVITY,
        TextureSlot.SPECULAR,
        TextureSlot.GLOSS,
        TextureSlot.ORM,
        TextureSlot.RMA,
        TextureSlot.HEIGHT,
        TextureSlot.OPACITY,
        TextureSlot.OPACITY_MASK,
    ):
        enum_name = "SAMPLERTYPE_VIRTUAL_MASKS" if is_virtual else "SAMPLERTYPE_MASKS"
    else:
        enum_name = "SAMPLERTYPE_VIRTUAL_COLOR" if is_virtual else "SAMPLERTYPE_COLOR"

    sampler_type = getattr(unreal.MaterialSamplerType, enum_name, None)
    if sampler_type is not None:
        expression.set_editor_property("sampler_type", sampler_type)


def _connect_property(expression, output_name, property_name):
    unreal_property = getattr(unreal.MaterialProperty, MATERIAL_PROPERTIES[property_name])
    return unreal.MaterialEditingLibrary.connect_material_property(
        expression, output_name, unreal_property
    )


def _configure_generated_material(material, textures, blend_mode, config):
    blend_values = {
        "Opaque": unreal.BlendMode.BLEND_OPAQUE,
        "Masked": unreal.BlendMode.BLEND_MASKED,
        "Translucent": unreal.BlendMode.BLEND_TRANSLUCENT,
        "Decal": unreal.BlendMode.BLEND_TRANSLUCENT,
    }
    material.set_editor_property(
        "blend_mode", blend_values.get(blend_mode, unreal.BlendMode.BLEND_OPAQUE)
    )
    if blend_mode == "Decal":
        decal_domain = getattr(unreal.MaterialDomain, "MD_DEFERRED_DECAL", None)
        if decal_domain is not None:
            material.set_editor_property("material_domain", decal_domain)
    if blend_mode == "Masked":
        material.set_editor_property("opacity_mask_clip_value", config.opacity_mask_clip_value)

    # Explicit single-channel maps win over packed maps if both are present.
    priority = {
        TextureSlot.CAVITY: 5,
        TextureSlot.GLOSS: 5,
        TextureSlot.ORM: 10,
        TextureSlot.RMA: 10,
    }
    ordered_textures = sorted(textures, key=lambda item: priority.get(item.texture_slot, 0))
    connected_inputs = set()
    expressions = {}

    for index, texture in enumerate(ordered_textures):
        if not texture.ue_path:
            continue
        texture_object = unreal.EditorAssetLibrary.load_asset(texture.ue_path)
        if texture_object is None:
            continue

        expression = unreal.MaterialEditingLibrary.create_material_expression(
            material, unreal.MaterialExpressionTextureSample, -700, index * 220 - 350
        )
        expression.set_editor_property("texture", texture_object)
        _set_sampler_type(expression, texture_object, texture.texture_slot)
        expressions[texture.texture_slot] = expression

        for output_name, property_name in material_connections(texture.texture_slot):
            if property_name in connected_inputs:
                continue
            _connect_property(expression, output_name, property_name)
            connected_inputs.add(property_name)

    # If transparency was selected for a BaseColor with alpha and there is no
    # dedicated opacity texture, use the BaseColor alpha channel.
    base_color = next(
        (texture for texture in ordered_textures if texture.texture_slot == TextureSlot.BASE_COLOUR),
        None,
    )
    base_expression = expressions.get(TextureSlot.BASE_COLOUR)
    if base_color and base_color.has_alpha and base_expression:
        if blend_mode == "Masked" and "opacity_mask" not in connected_inputs:
            _connect_property(base_expression, "A", "opacity_mask")
        elif blend_mode in ("Translucent", "Decal") and "opacity" not in connected_inputs:
            _connect_property(base_expression, "A", "opacity")

    layout = getattr(unreal.MaterialEditingLibrary, "layout_material_expressions", None)
    if layout:
        layout(material)
    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_loaded_asset(material)


def _create_fallback_material(asset_name, package_path, textures, blend_mode, config):
    material_name = asset_name.replace("MI_", "M_", 1) + "_Auto"
    material_path = f"{package_path}/{material_name}"

    if unreal.EditorAssetLibrary.does_asset_exist(material_path):
        if not config.replace_existing:
            return unreal.EditorAssetLibrary.load_asset(material_path), material_path
        unreal.EditorAssetLibrary.delete_asset(material_path)

    factory = unreal.MaterialFactoryNew()
    material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name=material_name,
        package_path=package_path,
        asset_class=unreal.Material,
        factory=factory,
    )
    if material:
        _configure_generated_material(material, textures, blend_mode, config)
    return material, material_path


def _create_material_instance(mi_name, mi_package, textures, blend_mode, parent_material, config):
    mi_path = f"{mi_package}/{mi_name}"
    mi = None
    if unreal.EditorAssetLibrary.does_asset_exist(mi_path):
        if not config.replace_existing:
            mi = unreal.EditorAssetLibrary.load_asset(mi_path)
        else:
            unreal.EditorAssetLibrary.delete_asset(mi_path)

    if mi is None:
        factory = unreal.MaterialInstanceConstantFactoryNew()
        mi = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            asset_name=mi_name,
            package_path=mi_package,
            asset_class=unreal.MaterialInstanceConstant,
            factory=factory,
        )
    if mi is None:
        return None, mi_path, {}

    mi.set_editor_property("parent", parent_material)
    if blend_mode in ("Masked", "Translucent", "Decal"):
        base_color = next(
            (texture for texture in textures if texture.texture_slot == TextureSlot.BASE_COLOUR),
            None,
        )
        unreal.MaterialEditingLibrary.set_material_instance_static_switch_parameter_value(
            mi, "UseBaseColourAlpha", value=bool(base_color and base_color.has_alpha)
        )

    loaded_textures = []
    has_vt = False
    for texture in textures:
        if not texture.ue_path:
            continue
        texture_object = unreal.EditorAssetLibrary.load_asset(texture.ue_path)
        if texture_object:
            loaded_textures.append((texture, texture_object))
            has_vt = has_vt or bool(texture_object.get_editor_property("virtual_texture_streaming"))

    unreal.MaterialEditingLibrary.set_material_instance_static_switch_parameter_value(
        mi, "UseVT", value=has_vt
    )

    assigned = {}
    for texture, texture_object in loaded_textures:
        if has_vt and not texture_object.get_editor_property("virtual_texture_streaming"):
            texture_object.set_editor_property("virtual_texture_streaming", True)
            unreal.EditorAssetLibrary.save_loaded_asset(texture_object)

        param_name = texture.texture_slot.value
        if has_vt:
            param_name = f"{param_name}_VT"
        unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
            mi, param_name, texture_object
        )
        if texture.texture_slot == TextureSlot.ORM:
            unreal.MaterialEditingLibrary.set_material_instance_static_switch_parameter_value(
                mi, "UseORM", value=True
            )
        assigned[param_name] = texture.ue_path

    unreal.EditorAssetLibrary.save_loaded_asset(mi)
    return mi, mi_path, assigned


def create_material_instance(group: AssetGroup, config: ImporterSettings, decisions=None):
    """Create an MI, or a connected regular material when its master is missing."""

    report = MaterialBuildResult(base_name=group.base_name)
    if not group.folder_path:
        report.errors.append(f"Could not resolve destination folder for {group.base_name}")
        return report

    mesh_object = unreal.EditorAssetLibrary.load_asset(group.mesh.ue_path) if group.mesh else None
    slots_to_process = group.material_slots if group.is_multi_material else {"": group.texture_list}

    for slot_name, textures in slots_to_process.items():
        if not textures:
            continue
        if group.is_multi_material:
            mi_name = f"MI_{group.base_name}_{slot_name}"
            package_path = f"{group.folder_path}/Materials"
        else:
            mi_name = f"MI_{group.base_name}"
            package_path = group.folder_path

        blend_mode = _blend_mode_for(mi_name, textures, decisions)
        master_path = _master_path(blend_mode, config)
        parent_material = unreal.EditorAssetLibrary.load_asset(master_path)

        if parent_material:
            material, asset_path, assigned = _create_material_instance(
                mi_name, package_path, textures, blend_mode, parent_material, config
            )
            report.mi_path = asset_path
            report.texture_assigned.update(assigned)
        elif config.auto_create_material_fallback:
            material, asset_path = _create_fallback_material(
                mi_name, package_path, textures, blend_mode, config
            )
            report.material_path = asset_path
            report.used_fallback_material = True
            report.texture_assigned.update(
                {
                    texture.texture_slot.value: texture.ue_path
                    for texture in textures
                    if texture.ue_path and material_connections(texture.texture_slot)
                }
            )
            unreal.log_warning(
                f"AssetPort: Master material missing ({master_path}); generated {asset_path}"
            )
        else:
            report.errors.append(f"Master material not found: {master_path}")
            continue

        if material is None:
            report.errors.append(f"Could not create material asset for {group.base_name}")
            continue

        if _assign_material(mesh_object, material, group, slot_name, config, blend_mode):
            report.mesh_linked = group.mesh.base_name
        report.success = True

    return report


def create_atlas_material_instance(
    group_atlas: AtlasGroup, config: ImporterSettings, decisions=None
):
    """Build one shared material for every mesh in an atlas/modular kit."""

    report = MaterialBuildResult(base_name=group_atlas.kit_name)
    if not group_atlas.folder_path:
        report.errors.append(
            f"Could not resolve destination folder for {group_atlas.kit_name}"
        )
        return report

    textures = group_atlas.texture_list
    mi_name = f"MI_{group_atlas.kit_name}"
    package_path = group_atlas.folder_path
    blend_mode = _blend_mode_for(mi_name, textures, decisions)
    master_path = _master_path(blend_mode, config)
    parent_material = unreal.EditorAssetLibrary.load_asset(master_path)

    if parent_material:
        material, asset_path, assigned = _create_material_instance(
            mi_name, package_path, textures, blend_mode, parent_material, config
        )
        report.mi_path = asset_path
        report.texture_assigned.update(assigned)
    elif config.auto_create_material_fallback:
        material, asset_path = _create_fallback_material(
            mi_name, package_path, textures, blend_mode, config
        )
        report.material_path = asset_path
        report.used_fallback_material = True
        report.texture_assigned.update(
            {
                texture.texture_slot.value: texture.ue_path
                for texture in textures
                if texture.ue_path and material_connections(texture.texture_slot)
            }
        )
        unreal.log_warning(
            f"AssetPort: Master material missing ({master_path}); generated {asset_path}"
        )
    else:
        report.errors.append(f"Master material not found: {master_path}")
        return report

    if material is None:
        report.errors.append(
            f"Could not create material asset for {group_atlas.kit_name}"
        )
        return report

    linked = False
    if config.auto_assign_to_mesh and blend_mode != "Decal":
        for mesh in group_atlas.mesh_list:
            mesh_object = unreal.EditorAssetLibrary.load_asset(mesh.ue_path) if mesh else None
            if mesh_object is None:
                continue
            if not _assign_material_at_index(mesh_object, 0, material):
                continue
            unreal.EditorAssetLibrary.save_loaded_asset(mesh_object)
            linked = True

    if linked:
        report.mesh_linked = group_atlas.kit_name
    report.success = True
    return report

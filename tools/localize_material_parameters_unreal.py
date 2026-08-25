"""Rename bundled master parameters and migrate dependent material instances.

Run this script through UnrealEditor-Cmd (or UE's Python console) with the
project closed in the regular editor.  It is idempotent: already-bilingual
parameters are left unchanged.
"""

import importlib.util
from pathlib import Path

import unreal

repository_root = Path(__file__).resolve().parents[1]
parameter_module_path = repository_root / "asset_port" / "material_parameters.py"
parameter_spec = importlib.util.spec_from_file_location(
    "asset_port_cn_migration_parameter_names", parameter_module_path
)
if parameter_spec is None or parameter_spec.loader is None:
    raise RuntimeError(f"Could not load parameter names from {parameter_module_path}")
parameter_module = importlib.util.module_from_spec(parameter_spec)
parameter_spec.loader.exec_module(parameter_module)
PARAMETER_LABELS = parameter_module.PARAMETER_LABELS


MASTER_PATHS = (
    "/Game/Python/Materials/M_Master_Opaque",
    "/Game/Python/Materials/M_Master_Masked",
    "/Game/Python/Materials/M_Master_Translucent",
    "/Game/Python/Materials/M_Master_Decal",
)
OVERRIDE_PROPERTIES = (
    "texture_parameter_values",
    "scalar_parameter_values",
    "vector_parameter_values",
)
STATIC_SWITCHES = ("UseBaseColourAlpha", "UseORM", "UseVT")
editing = unreal.MaterialEditingLibrary


def asset_path(asset):
    return asset.get_path_name().split(".", 1)[0]


def bundled_master_for(instance):
    parent = instance.get_editor_property("parent")
    visited = set()
    while parent is not None and asset_path(parent) not in visited:
        path = asset_path(parent)
        if path in MASTER_PATHS:
            return parent
        visited.add(path)
        if not isinstance(parent, unreal.MaterialInstance):
            return None
        parent = parent.get_editor_property("parent")
    return None


def dependent_instances():
    instances = []
    for path in unreal.EditorAssetLibrary.list_assets(
        "/Game", recursive=True, include_folder=False
    ):
        asset = unreal.EditorAssetLibrary.load_asset(path)
        if isinstance(asset, unreal.MaterialInstanceConstant) and bundled_master_for(asset):
            instances.append(asset)
    return instances


def capture_static_switch_values(instances):
    captured = {}
    root_switches = {}
    for path in MASTER_PATHS:
        master = unreal.EditorAssetLibrary.load_asset(path)
        if master:
            root_switches[path] = {
                str(name) for name in editing.get_static_switch_parameter_names(master)
            }

    for instance in instances:
        master = bundled_master_for(instance)
        available = root_switches.get(asset_path(master), set())
        values = {}
        for legacy_name in STATIC_SWITCHES:
            if legacy_name in available:
                value = editing.get_material_instance_static_switch_parameter_value(
                    instance, legacy_name
                )
                # AssetPort only writes UseORM when an ORM map is present.  A
                # false value is therefore normally inherited from the master;
                # avoid turning that inheritance into a new explicit override.
                if legacy_name == "UseORM" and not value:
                    continue
                values[legacy_name] = value
        captured[instance.get_path_name()] = values
    return captured


def rename_override_array(instance, property_name):
    values = list(instance.get_editor_property(property_name))
    changed = 0
    for index, entry in enumerate(values):
        info = entry.get_editor_property("parameter_info")
        legacy_name = str(info.get_editor_property("name"))
        bilingual_name = PARAMETER_LABELS.get(legacy_name)
        if not bilingual_name:
            continue
        info.set_editor_property("name", bilingual_name)
        entry.set_editor_property("parameter_info", info)
        values[index] = entry
        changed += 1
    if changed:
        instance.set_editor_property(property_name, values)
    return changed


def rename_master_expressions(master):
    prefix = master.get_path_name() + ":"
    changed = 0
    for expression in unreal.ObjectIterator(unreal.MaterialExpression):
        if not expression.get_path_name().startswith(prefix):
            continue
        try:
            legacy_name = str(expression.get_editor_property("parameter_name"))
        except Exception:
            continue
        bilingual_name = PARAMETER_LABELS.get(legacy_name)
        if not bilingual_name:
            continue
        expression.set_editor_property("parameter_name", bilingual_name)
        changed += 1
    if changed:
        editing.recompile_material(master)
        unreal.EditorAssetLibrary.save_loaded_asset(master)
    return changed


def migrate():
    masters = [unreal.EditorAssetLibrary.load_asset(path) for path in MASTER_PATHS]
    missing = [path for path, master in zip(MASTER_PATHS, masters) if master is None]
    if missing:
        raise RuntimeError("Missing bundled master materials: " + ", ".join(missing))

    instances = dependent_instances()
    switch_values = capture_static_switch_values(instances)

    expression_count = sum(rename_master_expressions(master) for master in masters)
    override_count = 0
    switch_count = 0
    for instance in instances:
        for property_name in OVERRIDE_PROPERTIES:
            override_count += rename_override_array(instance, property_name)
        for legacy_name, value in switch_values[instance.get_path_name()].items():
            editing.set_material_instance_static_switch_parameter_value(
                instance, PARAMETER_LABELS[legacy_name], value=value
            )
            switch_count += 1
        unreal.EditorAssetLibrary.save_loaded_asset(instance)

    unreal.log(
        "AssetPort-CN bilingual parameter migration complete: "
        f"{expression_count} expressions, {override_count} overrides, "
        f"{switch_count} switches across {len(instances)} material instances."
    )


if __name__ == "__main__":
    migrate()

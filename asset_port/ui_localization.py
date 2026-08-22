"""Runtime localization helpers for the bundled Editor Utility Widgets."""

import unreal

from asset_port.localization import (
    BLEND_KEYS,
    category_options,
    category_to_internal,
    blend_options,
    blend_to_internal,
    tr,
)


TEXT_REPLACEMENTS = {
    "Asset Port": "main.title",
    "Browse": "main.browse",
    "Cancel": "common.cancel",
    "Category :": "main.category",
    "Category:": "main.category",
    "Folder :": "main.folder",
    "Folder:": "main.folder",
    "Import": "main.import",
    "Preview": "main.preview",
    "Asset Port - Preview": "preview.title",
    "Confirm Import": "preview.confirm",
    "Conform Import": "preview.confirm",
    "Failed / Warnings": "preview.failed",
    "Asset Port - Transparency Setup": "transparency.title",
    "Select the desired Blend Mode for detected transparent assets:": "transparency.help",
}

NAMED_TEXT_WIDGETS = {
    "Browse_Text": "main.browse",
    "Category_Text": "main.category",
    "FOlder_Text": "main.folder",
}


def _find_widget(root_widget, name):
    try:
        widget = root_widget.find_child_widget_by_name(unreal.Name(name))
        if widget:
            return widget
    except Exception:
        pass
    try:
        widget = root_widget.get_widget_from_name(unreal.Name(name))
        if widget:
            return widget
    except Exception:
        pass
    try:
        return root_widget.get_editor_property(name)
    except Exception:
        return None


def _all_widgets(root_widget):
    widgets = []
    try:
        tree = root_widget.get_editor_property("widget_tree")
        widgets.extend(tree.get_all_widgets())
    except Exception:
        pass

    for name in NAMED_TEXT_WIDGETS:
        widget = _find_widget(root_widget, name)
        if widget and widget not in widgets:
            widgets.append(widget)
    return widgets


def _text_to_string(value):
    try:
        return unreal.TextLibrary.conv_text_to_string(value).strip()
    except Exception:
        return str(value).strip()


def _set_widget_text(widget, text):
    try:
        widget.set_text(unreal.Text(text))
        return True
    except Exception:
        return False


def _set_descendant_text(widget, key):
    try:
        current = _text_to_string(widget.get_text())
        if current in (tr(key, "en_US"), tr(key, "zh_CN")):
            return _set_widget_text(widget, tr(key))
    except Exception:
        pass

    children = []
    try:
        children.extend(widget.get_child_at(index) for index in range(widget.get_children_count()))
    except Exception:
        try:
            content = widget.get_content()
            if content:
                children.append(content)
        except Exception:
            pass

    return any(_set_descendant_text(child, key) for child in children if child)


def _set_named_text(root_widget, name, key):
    widget = _find_widget(root_widget, name)
    if widget:
        if not _set_widget_text(widget, tr(key)):
            _set_descendant_text(widget, key)


def _set_button_text(root_widget, button_name, key):
    button = _find_widget(root_widget, button_name)
    if not button:
        return
    child = None
    for accessor in ("get_content", "get_child_at"):
        try:
            child = getattr(button, accessor)(0) if accessor == "get_child_at" else getattr(button, accessor)()
            if child:
                break
        except Exception:
            continue
    if child:
        _set_widget_text(child, tr(key))


def _localize_text_widgets(root_widget):
    for widget in _all_widgets(root_widget):
        try:
            current = _text_to_string(widget.get_text())
        except Exception:
            continue
        key = TEXT_REPLACEMENTS.get(current)
        if key:
            _set_widget_text(widget, tr(key))

    for name, key in NAMED_TEXT_WIDGETS.items():
        widget = _find_widget(root_widget, name)
        if widget:
            _set_widget_text(widget, tr(key))


def _replace_combo_options(combo, display_options, selected_internal, to_internal):
    if not combo:
        return
    try:
        combo.clear_options()
        for option in display_options:
            combo.add_option(option)
        selected_display = next(
            (option for option in display_options if to_internal(option) == selected_internal),
            display_options[0],
        )
        combo.set_selected_option(selected_display)
    except Exception as error:
        unreal.log_warning(f"AssetPort-CN: Could not localize combo box: {error}")


def localize_main_widget(widget):
    _localize_text_widgets(widget)
    _set_named_text(widget, "Asset_Port", "main.title")
    _set_button_text(widget, "Browse_Button", "main.browse")
    _set_button_text(widget, "Import_Button", "main.import")
    _set_button_text(widget, "Preview_Button", "main.preview")
    _set_button_text(widget, "Cancel_Button", "common.cancel")

    folder_field = _find_widget(widget, "Folder_Path_Field")
    if folder_field:
        try:
            folder_field.set_hint_text(unreal.Text(tr("main.folder_hint")))
        except Exception:
            pass

    category_combo = _find_widget(widget, "Category_Dropdown")
    current = None
    if category_combo:
        try:
            current = category_to_internal(category_combo.get_selected_option())
        except Exception:
            pass
    _replace_combo_options(
        category_combo,
        category_options(),
        current,
        category_to_internal,
    )


def localize_preview_widget(widget):
    _localize_text_widgets(widget)
    _set_named_text(widget, "Asset_Port", "preview.title")
    _set_button_text(widget, "Confirm_Import", "preview.confirm")
    _set_button_text(widget, "Conform_Import", "preview.confirm")
    _set_button_text(widget, "Cancel_preview", "common.cancel")


def localize_transparency_widget(widget):
    _localize_text_widgets(widget)
    _set_named_text(widget, "Asset_Port", "transparency.title")
    _set_button_text(widget, "Confirm_Button", "common.confirm")
    _set_button_text(widget, "Cancel_Button", "common.cancel")
    scroll_box = _find_widget(widget, "Transparency_ScrollBox")
    if not scroll_box:
        return

    try:
        rows = [scroll_box.get_child_at(index) for index in range(scroll_box.get_children_count())]
    except Exception:
        return

    for row in rows:
        combo = _find_widget(row, "ComboBox_BlendMode")
        if not combo:
            continue
        try:
            current = blend_to_internal(combo.get_selected_option())
        except Exception:
            current = "Opaque"
        _replace_combo_options(combo, blend_options(), current, blend_to_internal)

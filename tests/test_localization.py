import sys
import types
import unittest


class FakeText(str):
    pass


fake_unreal = types.SimpleNamespace(
    Name=str,
    Text=FakeText,
    TextLibrary=types.SimpleNamespace(conv_text_to_string=str),
    log_warning=lambda _message: None,
)
sys.modules.setdefault("unreal", fake_unreal)

from asset_port.localization import (  # noqa: E402
    blend_options,
    blend_to_internal,
    category_options,
    category_to_internal,
    localize_message,
)
from asset_port.ui_localization import localize_main_widget  # noqa: E402


class FakeTextWidget:
    def __init__(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = str(text)


class FakeButton:
    def __init__(self, text):
        self.content = FakeTextWidget(text)

    def get_content(self):
        return self.content


class FakeCombo:
    def __init__(self, selected):
        self.options = []
        self.selected = selected

    def get_selected_option(self):
        return self.selected

    def clear_options(self):
        self.options.clear()

    def add_option(self, option):
        self.options.append(option)

    def set_selected_option(self, option):
        self.selected = option


class FakeField:
    def set_hint_text(self, text):
        self.hint = str(text)


class FakeTree:
    def __init__(self, widgets):
        self.widgets = widgets

    def get_all_widgets(self):
        return self.widgets


class FakeRoot:
    def __init__(self):
        self.widgets = {
            "Asset_Port": FakeTextWidget("Asset Port"),
            "Browse_Text": FakeTextWidget("Browse"),
            "Category_Text": FakeTextWidget("Category :"),
            "FOlder_Text": FakeTextWidget("Folder :"),
            "Browse_Button": FakeButton("Browse"),
            "Import_Button": FakeButton("Import"),
            "Preview_Button": FakeButton("Preview"),
            "Cancel_Button": FakeButton("Cancel"),
            "Folder_Path_Field": FakeField(),
            "Category_Dropdown": FakeCombo("Environment"),
        }
        self.tree = FakeTree(list(self.widgets.values()))

    def get_widget_from_name(self, name):
        return self.widgets.get(str(name))

    def get_editor_property(self, name):
        if name == "widget_tree":
            return self.tree
        raise AttributeError(name)


class LocalizationTests(unittest.TestCase):
    def test_category_round_trip(self):
        expected = [None, "Environment", "Weapons", "Props", "Characters"]
        self.assertEqual([category_to_internal(value, "zh_CN") for value in category_options("zh_CN")], expected)
        self.assertEqual([category_to_internal(value, "en_US") for value in category_options("en_US")], expected)

    def test_blend_round_trip(self):
        expected = ["Masked", "Translucent", "Decal", "Opaque"]
        self.assertEqual([blend_to_internal(value, "zh_CN") for value in blend_options("zh_CN")], expected)
        self.assertEqual([blend_to_internal(value, "en_US") for value in blend_options("en_US")], expected)

    def test_chinese_warning(self):
        self.assertEqual(localize_message("group Chair Normal map is missing", "zh_CN"), "资源组 Chair 缺少法线纹理")

    def test_main_widget_localization(self):
        root = FakeRoot()
        localize_main_widget(root)
        self.assertEqual(root.widgets["Asset_Port"].text, "AssetPort 资源导入")
        self.assertEqual(root.widgets["Import_Button"].content.text, "立即导入")
        self.assertEqual(root.widgets["Category_Dropdown"].selected, "环境")
        self.assertEqual(category_to_internal(root.widgets["Category_Dropdown"].selected), "Environment")


if __name__ == "__main__":
    unittest.main()

"""Small runtime localization layer for AssetPort-CN.

Internal identifiers remain English. Only user-facing strings are translated.
"""

import re

from asset_port.config import config_loader


TRANSLATIONS = {
    "en_US": {
        "app.name": "AssetPort",
        "menu.tooltip": "Import a folder using the AssetPort automated pipeline",
        "folder.dialog_title": "Select Import Folder",
        "dialog.select_directory.title": "Select Directory",
        "dialog.select_directory.body": "Please select a valid import directory before launching the preview.",
        "main.title": "Asset Port",
        "main.browse": "Browse",
        "main.cancel": "Cancel",
        "main.import": "Import",
        "main.preview": "Preview",
        "main.category": "Category:",
        "main.folder": "Folder:",
        "main.folder_hint": "Select Folder",
        "preview.title": "Asset Port - Preview",
        "preview.confirm": "Confirm Import",
        "preview.failed": "Failed / Warnings",
        "transparency.title": "Asset Port - Transparency Setup",
        "transparency.help": "Select the desired Blend Mode for detected transparent assets:",
        "common.confirm": "Confirm Import",
        "common.cancel": "Cancel",
        "category.auto": "Auto-Detect",
        "category.environment": "Environment",
        "category.weapons": "Weapons",
        "category.props": "Props",
        "category.characters": "Characters",
        "blend.opaque": "Opaque",
        "blend.masked": "Masked",
        "blend.translucent": "Translucent",
        "report.scanned": "Scanned",
        "report.imported": "Imported",
        "report.mi_created": "Materials Created",
        "report.mi_linked": "Materials Linked",
        "report.warning": "Warning",
        "report.error": "Error",
        "progress.processing": "Processing imported assets...",
        "progress.texture": "Configuring textures: {name}",
    },
    "zh_CN": {
        "app.name": "AssetPort 资源导入",
        "menu.tooltip": "使用 AssetPort 自动化流程批量导入文件夹资源",
        "folder.dialog_title": "选择要导入的文件夹",
        "dialog.select_directory.title": "请选择目录",
        "dialog.select_directory.body": "启动导入预览前，请先选择有效的资源目录。",
        "main.title": "AssetPort 资源导入",
        "main.browse": "浏览",
        "main.cancel": "取消",
        "main.import": "立即导入",
        "main.preview": "导入预览",
        "main.category": "资源分类：",
        "main.folder": "源文件夹：",
        "main.folder_hint": "请选择资源文件夹",
        "preview.title": "AssetPort - 导入预览",
        "preview.confirm": "确认导入",
        "preview.failed": "失败与警告",
        "transparency.title": "AssetPort - 透明材质设置",
        "transparency.help": "请为检测到的透明材质选择混合模式：",
        "common.confirm": "确认导入",
        "common.cancel": "取消",
        "category.auto": "自动检测",
        "category.environment": "环境",
        "category.weapons": "武器",
        "category.props": "道具",
        "category.characters": "角色",
        "blend.opaque": "不透明",
        "blend.masked": "遮罩",
        "blend.translucent": "半透明",
        "report.scanned": "扫描数量",
        "report.imported": "成功导入",
        "report.mi_created": "创建材质",
        "report.mi_linked": "关联材质",
        "report.warning": "警告",
        "report.error": "错误",
        "progress.processing": "正在处理导入的资源……",
        "progress.texture": "正在配置纹理：{name}",
    },
}


CATEGORY_KEYS = {
    "Auto-Detect": "category.auto",
    "None": "category.auto",
    "Environment": "category.environment",
    "Weapon": "category.weapons",
    "Weapons": "category.weapons",
    "Props": "category.props",
    "Character": "category.characters",
    "Characters": "category.characters",
    "Charactor": "category.characters",
}

CATEGORY_INTERNAL = {
    "category.auto": None,
    "category.environment": "Environment",
    "category.weapons": "Weapons",
    "category.props": "Props",
    "category.characters": "Characters",
}

BLEND_KEYS = {
    "Opaque": "blend.opaque",
    "Masked": "blend.masked",
    "Translucent": "blend.translucent",
}

STATIC_MESSAGE_TRANSLATIONS = {
    "file is empty or corrupted": "文件为空或已损坏",
    "Mesh size is bigger than 500 MB": "模型文件大于 500 MB",
    "Texture Size is bigger than 100 MB": "纹理文件大于 100 MB",
    "File Format not supported": "不支持此文件格式",
    "Asset doesn't have Prefix": "资源名称缺少类型前缀",
}


def get_language():
    return config_loader().language


def tr(key, language=None, **values):
    language = language or get_language()
    table = TRANSLATIONS.get(language, TRANSLATIONS["en_US"])
    text = table.get(key, TRANSLATIONS["en_US"].get(key, key))
    return text.format(**values) if values else text


def category_options(language=None):
    return [
        tr("category.auto", language),
        tr("category.environment", language),
        tr("category.weapons", language),
        tr("category.props", language),
        tr("category.characters", language),
    ]


def category_to_internal(display_value, language=None):
    if display_value in CATEGORY_KEYS:
        return CATEGORY_INTERNAL[CATEGORY_KEYS[display_value]]
    for key, internal in CATEGORY_INTERNAL.items():
        if display_value == tr(key, language):
            return internal
    return display_value or None


def blend_to_internal(display_value, language=None):
    if display_value in BLEND_KEYS:
        return display_value
    for internal, key in BLEND_KEYS.items():
        if display_value == tr(key, language):
            return internal
    return "Opaque"


def blend_options(language=None):
    return [tr(BLEND_KEYS[value], language) for value in ("Masked", "Translucent", "Opaque")]


def localize_message(message, language=None):
    language = language or get_language()
    if language != "zh_CN":
        return message
    if message in STATIC_MESSAGE_TRANSLATIONS:
        return STATIC_MESSAGE_TRANSLATIONS[message]

    patterns = (
        (r"^group (.+) has no mesh but textures$", r"资源组 \1 只有纹理，没有模型"),
        (r"^group (.+) base colour map is missing$", r"资源组 \1 缺少基础颜色纹理"),
        (r"^group (.+) Normal map is missing$", r"资源组 \1 缺少法线纹理"),
        (r"^group (.+) Roughness or ORM map is missing\s*$", r"资源组 \1 缺少粗糙度或 ORM 纹理"),
    )
    for pattern, replacement in patterns:
        if re.match(pattern, message):
            return re.sub(pattern, replacement, message)
    return message

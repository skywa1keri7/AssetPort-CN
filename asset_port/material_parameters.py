"""Artist-facing bilingual names for bundled master-material parameters.

The dictionary keys are the legacy identifiers used by Asset-Port and by
existing custom master materials.  Keep those keys stable: the importer uses
them as compatibility aliases when a project has not adopted the bilingual
bundled masters.
"""


PARAMETER_LABELS = {
    # Texture parameters
    "BaseColour": "基础色 / BaseColour",
    "BaseColour_VT": "基础色虚拟纹理 / BaseColour_VT",
    "Normal": "法线 / Normal",
    "Normal_VT": "法线虚拟纹理 / Normal_VT",
    "Roughness": "粗糙度 / Roughness",
    "Roughness_VT": "粗糙度虚拟纹理 / Roughness_VT",
    "Metallic": "金属度 / Metallic",
    "Metallic_VT": "金属度虚拟纹理 / Metallic_VT",
    "AmbientOcclusion": "环境光遮蔽 / AmbientOcclusion",
    "AmbientOcclusion_VT": "环境光遮蔽虚拟纹理 / AmbientOcclusion_VT",
    "Emissive": "自发光 / Emissive",
    "Emissive_VT": "自发光虚拟纹理 / Emissive_VT",
    "Height": "高度 / Height",
    "Height_VT": "高度虚拟纹理 / Height_VT",
    "ORM": "ORM通道打包 / ORM",
    "ORM_VT": "ORM虚拟纹理 / ORM_VT",
    "OpacityMask": "不透明度遮罩 / OpacityMask",
    "OpacityMask_VT": "不透明度遮罩虚拟纹理 / OpacityMask_VT",
    # Scalar parameters (including corrected artist-facing spellings).
    "AoStrength": "环境光遮蔽强度 / AO Strength",
    "BaseSpeculer": "基础高光 / Base Specular",
    "Contrast": "对比度 / Contrast",
    "EmissiveStrength": "自发光强度 / Emissive Strength",
    "HeightStrength": "高度强度 / Height Strength",
    "MaxRoughness.": "最大粗糙度 / Max Roughness",
    "MetallicIntensity": "金属度强度 / Metallic Intensity",
    "MinRoughness.": "最小粗糙度 / Min Roughness",
    "NormalStrength": "法线强度 / Normal Strength",
    "OpacityAmount": "不透明度 / Opacity Amount",
    "ORM_AoStrength": "ORM环境光遮蔽强度 / ORM AO Strength",
    "ORM_MetalStrength": "ORM金属度强度 / ORM Metallic Strength",
    "ORM_RoughnessStrength": "ORM粗糙度强度 / ORM Roughness Strength",
    "Saturation": "饱和度 / Saturation",
    "brightness": "亮度 / Brightness",
    # Vector parameters
    "Advance UV Control": "高级UV控制 / Advanced UV Control",
    "TInt": "色调 / Tint",
    # Static switches
    "UseBaseColourAlpha": "使用基础色Alpha / Use BaseColour Alpha",
    "UseORM": "使用ORM / Use ORM",
    "UseVT": "使用虚拟纹理 / Use VT",
}


def bilingual_parameter_name(legacy_name):
    """Return the bundled bilingual label for a legacy parameter name."""

    return PARAMETER_LABELS.get(str(legacy_name), str(legacy_name))


def resolve_parameter_name(legacy_name, available_names):
    """Resolve a parameter on either a bilingual or legacy English master.

    Unknown/custom masters retain the historical behavior: if neither alias
    is advertised, return the legacy name and let Unreal handle the miss.
    """

    legacy_name = str(legacy_name)
    available = {str(name) for name in available_names}
    bilingual = bilingual_parameter_name(legacy_name)
    if bilingual in available:
        return bilingual
    if legacy_name in available:
        return legacy_name
    return legacy_name

"""Pure material/texture rules shared by the Unreal-facing pipeline.

Keeping these decisions outside Unreal makes filename and graph behaviour easy to
test without launching the editor.
"""

from asset_port.models import TextureSlot


TEXTURE_PROFILES = {
    TextureSlot.BASE_COLOUR: ("default", True),
    TextureSlot.EMISSIVE: ("default", True),
    TextureSlot.NORMAL: ("normal", False),
    TextureSlot.ROUGHNESS: ("masks", False),
    TextureSlot.METALLIC: ("masks", False),
    TextureSlot.AO: ("masks", False),
    TextureSlot.CAVITY: ("masks", False),
    TextureSlot.SPECULAR: ("masks", False),
    TextureSlot.GLOSS: ("masks", False),
    TextureSlot.TRANSLUCENCY: ("default", True),
    TextureSlot.ORM: ("masks", False),
    TextureSlot.RMA: ("masks", False),
    TextureSlot.HEIGHT: ("masks", False),
    TextureSlot.OPACITY_MASK: ("masks", False),
    TextureSlot.OPACITY: ("alpha", False),
}


MATERIAL_CONNECTIONS = {
    TextureSlot.BASE_COLOUR: (("RGB", "base_color"),),
    TextureSlot.NORMAL: (("RGB", "normal"),),
    TextureSlot.ROUGHNESS: (("R", "roughness"),),
    TextureSlot.METALLIC: (("R", "metallic"),),
    TextureSlot.AO: (("R", "ambient_occlusion"),),
    TextureSlot.CAVITY: (("R", "ambient_occlusion"),),
    TextureSlot.SPECULAR: (("R", "specular"),),
    TextureSlot.EMISSIVE: (("RGB", "emissive_color"),),
    TextureSlot.OPACITY: (("R", "opacity"),),
    TextureSlot.OPACITY_MASK: (("R", "opacity_mask"),),
    TextureSlot.ORM: (
        ("R", "ambient_occlusion"),
        ("G", "roughness"),
        ("B", "metallic"),
    ),
    TextureSlot.RMA: (
        ("R", "roughness"),
        ("G", "metallic"),
        ("B", "ambient_occlusion"),
    ),
}


def texture_profile(slot):
    """Return ``(compression profile, sRGB)`` or ``None`` for unknown slots."""

    return TEXTURE_PROFILES.get(slot)


def material_connections(slot):
    """Return texture-output/material-input pairs for a generated material."""

    return MATERIAL_CONNECTIONS.get(slot, ())


def automatic_blend_mode(textures):
    """Choose a conservative blend mode from explicit texture semantics."""

    slots = {texture.texture_slot for texture in textures}
    if TextureSlot.OPACITY_MASK in slots:
        return "Masked"
    if TextureSlot.OPACITY in slots:
        return "Translucent"
    return "Opaque"

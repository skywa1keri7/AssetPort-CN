import unittest
from types import SimpleNamespace

from asset_port.detector import AssetDetector
from asset_port.material_rules import (
    automatic_blend_mode,
    material_connections,
    texture_profile,
)
from asset_port.models import TextureSlot


class MaterialRuleTests(unittest.TestCase):
    def test_mask_profiles_disable_srgb(self):
        for slot in (
            TextureSlot.ROUGHNESS,
            TextureSlot.METALLIC,
            TextureSlot.AO,
            TextureSlot.ORM,
            TextureSlot.RMA,
            TextureSlot.OPACITY_MASK,
        ):
            self.assertEqual(texture_profile(slot), ("masks", False))

    def test_colour_and_normal_profiles(self):
        self.assertEqual(texture_profile(TextureSlot.BASE_COLOUR), ("default", True))
        self.assertEqual(texture_profile(TextureSlot.NORMAL), ("normal", False))

    def test_explicit_mask_has_priority(self):
        textures = [
            SimpleNamespace(texture_slot=TextureSlot.OPACITY),
            SimpleNamespace(texture_slot=TextureSlot.OPACITY_MASK),
        ]
        self.assertEqual(automatic_blend_mode(textures), "Masked")
        self.assertEqual(
            automatic_blend_mode([SimpleNamespace(texture_slot=TextureSlot.OPACITY)]),
            "Translucent",
        )

    def test_packed_map_channels(self):
        self.assertEqual(
            material_connections(TextureSlot.ORM),
            (
                ("R", "ambient_occlusion"),
                ("G", "roughness"),
                ("B", "metallic"),
            ),
        )
        self.assertEqual(
            material_connections(TextureSlot.RMA),
            (
                ("R", "roughness"),
                ("G", "metallic"),
                ("B", "ambient_occlusion"),
            ),
        )

    def test_rma_suffix_detection(self):
        asset = AssetDetector().detect_file("T_Chair_RMA.png")
        self.assertEqual(asset.base_name, "Chair")
        self.assertEqual(asset.texture_slot, TextureSlot.RMA)


if __name__ == "__main__":
    unittest.main()

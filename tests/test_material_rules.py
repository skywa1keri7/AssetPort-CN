import unittest
from types import SimpleNamespace

from asset_port.detector import AssetDetector
from asset_port.material_rules import (
    automatic_blend_mode,
    material_connections,
    texture_profile,
)
from asset_port.models import AssetType, DetectedAsset, TextureSlot


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

    def test_prefixless_marketplace_texture_detection(self):
        asset = AssetDetector().detect_file("phhibtp2_2K_Albedo.jpg")
        self.assertEqual(asset.asset_type, AssetType.TEXTURE)
        self.assertEqual(asset.base_name, "phhibtp2")
        self.assertEqual(asset.texture_slot, TextureSlot.BASE_COLOUR)
        self.assertIsNone(asset.material_slot_name)

    def test_prefixless_fbx_defaults_to_static_mesh(self):
        asset = AssetDetector().detect_file("phhibtp2.fbx")
        self.assertEqual(asset.asset_type, AssetType.STATIC_MESH)
        self.assertEqual(asset.base_name, "phhibtp2")

    def test_marketplace_auxiliary_maps_are_unique_and_configurable(self):
        detector = AssetDetector()
        expected = {
            "Cavity": TextureSlot.CAVITY,
            "Gloss": TextureSlot.GLOSS,
            "Specular": TextureSlot.SPECULAR,
            "Bump": TextureSlot.HEIGHT,
            "Metalness": TextureSlot.METALLIC,
        }
        for suffix, slot in expected.items():
            asset = detector.detect_file(f"chair_2K_{suffix}.jpg")
            self.assertEqual(asset.base_name, "chair")
            self.assertEqual(asset.texture_slot, slot)
            self.assertEqual(texture_profile(slot)[0], "masks")

    def test_unknown_files_do_not_create_empty_groups(self):
        unknown = DetectedAsset(
            filename="notes.txt",
            source_path="notes.txt",
            prefix="",
            base_name="notes",
            suffix="",
            asset_type=AssetType.UNKNOWN,
            texture_slot=None,
            extension=".txt",
        )
        self.assertEqual(AssetDetector().group_assets([unknown]), [])


if __name__ == "__main__":
    unittest.main()

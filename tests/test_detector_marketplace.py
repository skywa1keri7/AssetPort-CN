import unittest

from asset_port.detector import AssetDetector
from asset_port.models import AssetType, TextureSlot


class MarketplaceFilenameTests(unittest.TestCase):
    def setUp(self):
        self.detector = AssetDetector()

    def test_prefixless_texture_uses_extension_and_ignores_resolution_token(self):
        asset = self.detector.detect_file("RockCliff_2K_BaseColor.png")

        self.assertEqual(asset.asset_type, AssetType.TEXTURE)
        self.assertEqual(asset.base_name, "RockCliff")
        self.assertIsNone(asset.material_slot_name)
        self.assertEqual(asset.texture_slot, TextureSlot.BASE_COLOUR)

    def test_prefixless_fbx_defaults_to_static_mesh(self):
        asset = self.detector.detect_file("RockCliff.fbx")

        self.assertEqual(asset.asset_type, AssetType.STATIC_MESH)
        self.assertEqual(asset.base_name, "RockCliff")

    def test_prefixless_atlas_fbx_gets_static_mesh_asset_name(self):
        asset = self.detector.detect_file("Rock01-RockKit.fbx")

        self.assertEqual(asset.asset_type, AssetType.STATIC_MESH)
        self.assertEqual(asset.kit_name, "RockKit")
        self.assertEqual(asset.ue_asset_name, "SM_Rock01")

    def test_atlas_group_keeps_shared_texture_set(self):
        assets = [
            self.detector.detect_file("SM_env_Rock01-RockKit.fbx"),
            self.detector.detect_file("SM_env_Rock02-RockKit.fbx"),
            self.detector.detect_file("T_env_RockKit_D.png"),
            self.detector.detect_file("T_env_RockKit_N.png"),
        ]

        atlas_groups, remaining = self.detector.group_atlas_assets(assets)

        self.assertEqual(remaining, [])
        self.assertEqual(len(atlas_groups), 1)
        self.assertEqual(atlas_groups[0].kit_name, "RockKit")
        self.assertEqual(atlas_groups[0].mesh_count, 2)
        self.assertEqual(len(atlas_groups[0].texture_list), 2)

    def test_additional_marketplace_suffixes(self):
        expected = {
            "Metalness": TextureSlot.METALLIC,
            "Cavity": TextureSlot.CAVITY,
            "Specular": TextureSlot.SPECULAR,
            "Gloss": TextureSlot.GLOSS,
            "Translucency": TextureSlot.TRANSLUCENCY,
            "Bump": TextureSlot.HEIGHT,
            "RMA": TextureSlot.RMA,
        }

        for suffix, slot in expected.items():
            with self.subTest(suffix=suffix):
                asset = self.detector.detect_file(f"RockCliff_{suffix}.png")
                self.assertEqual(asset.asset_type, AssetType.TEXTURE)
                self.assertEqual(asset.texture_slot, slot)

    def test_unknown_files_do_not_create_empty_groups(self):
        unknown = self.detector.detect_file("notes.txt")

        self.assertEqual(unknown.asset_type, AssetType.UNKNOWN)
        self.assertEqual(self.detector.group_assets([unknown]), [])


if __name__ == "__main__":
    unittest.main()

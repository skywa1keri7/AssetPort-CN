import unittest

from asset_port.detector import AssetDetector


class CategoryInheritanceTests(unittest.TestCase):
    def setUp(self):
        self.detector = AssetDetector()

    def test_group_category_propagates_to_prefixless_textures_and_lods(self):
        assets = [
            self.detector.detect_file("SM_env_Chest_LOD0.fbx"),
            self.detector.detect_file("SM_Chest_LOD1.fbx"),
            self.detector.detect_file("T_Chest_BaseColor.png"),
            self.detector.detect_file("T_Chest_Normal.png"),
        ]

        group = self.detector.group_assets(assets)[0]

        self.assertEqual(group.category, "Environment")
        self.assertEqual(group.mesh.category, "Environment")
        self.assertTrue(all(item.category == "Environment" for item in group.texture_list))
        self.assertTrue(all(item.category == "Environment" for item in group.lod_meshes))

    def test_atlas_category_consensus_includes_lods(self):
        assets = [
            self.detector.detect_file("SM_Rock01-RockKit_LOD0.fbx"),
            self.detector.detect_file("SM_prop_Rock01-RockKit_LOD1.fbx"),
            self.detector.detect_file("SM_Rock02-RockKit_LOD0.fbx"),
            self.detector.detect_file("T_RockKit_D.png"),
        ]

        atlas = self.detector.group_atlas_assets(assets)[0][0]

        self.assertEqual(atlas.category, "Props")
        all_lods = [lod for lods in atlas.lod_meshes.values() for lod in lods]
        self.assertTrue(all(item.category == "Props" for item in atlas.mesh_list))
        self.assertTrue(all(item.category == "Props" for item in atlas.texture_list))
        self.assertTrue(all(item.category == "Props" for item in all_lods))

    def test_vehicle_and_effect_categories(self):
        self.assertEqual(
            self.detector.detect_file("SM_veh_Car.fbx").category, "Vehicles"
        )
        self.assertEqual(
            self.detector.detect_file("T_fx_Smoke_D.png").category, "Effects"
        )


if __name__ == "__main__":
    unittest.main()

import unittest

from asset_port.material_parameters import (
    bilingual_parameter_name,
    resolve_parameter_name,
)


class MaterialParameterNameTests(unittest.TestCase):
    def test_bundled_master_prefers_bilingual_name(self):
        self.assertEqual(
            resolve_parameter_name("Normal", {"法线 / Normal", "粗糙度 / Roughness"}),
            "法线 / Normal",
        )

    def test_custom_legacy_master_remains_supported(self):
        self.assertEqual(resolve_parameter_name("UseORM", {"UseORM", "UseVT"}), "UseORM")

    def test_unknown_master_keeps_historical_fallback(self):
        self.assertEqual(resolve_parameter_name("BaseColour", set()), "BaseColour")

    def test_opacity_falls_back_to_bundled_opacity_mask(self):
        self.assertEqual(
            resolve_parameter_name(
                "Opacity",
                {"不透明度遮罩 / OpacityMask"},
                ("OpacityMask",),
            ),
            "不透明度遮罩 / OpacityMask",
        )

    def test_custom_opacity_parameter_wins_over_fallback(self):
        self.assertEqual(
            resolve_parameter_name(
                "Opacity",
                {"Opacity", "不透明度遮罩 / OpacityMask"},
                ("OpacityMask",),
            ),
            "Opacity",
        )

    def test_corrected_artist_facing_spelling_keeps_legacy_alias(self):
        self.assertEqual(bilingual_parameter_name("BaseSpeculer"), "基础高光 / Base Specular")


if __name__ == "__main__":
    unittest.main()

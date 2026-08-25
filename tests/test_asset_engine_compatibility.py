import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ENGINE_RELEASE_PATTERN = re.compile(rb"Release-5\.(\d+)")


class AssetEngineCompatibilityTests(unittest.TestCase):
    def test_bundled_assets_do_not_require_newer_than_ue56(self):
        assets = sorted(REPOSITORY_ROOT.glob("Materials/*.uasset"))
        assets.extend(sorted(REPOSITORY_ROOT.glob("Widgets/*.uasset")))
        self.assertTrue(assets)

        incompatible = {}
        missing_markers = []
        for asset in assets:
            versions = {
                int(match)
                for match in ENGINE_RELEASE_PATTERN.findall(asset.read_bytes())
            }
            if not versions:
                missing_markers.append(asset.name)
                continue
            if max(versions) > 6:
                incompatible[asset.name] = sorted(versions)

        self.assertFalse(missing_markers, missing_markers)
        self.assertFalse(incompatible, incompatible)


if __name__ == "__main__":
    unittest.main()

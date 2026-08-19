# Changelog

## [0.2.1] - 2026-08-19

### Fixed

- Infer texture/static-mesh types from file extensions when `T_`/`SM_` prefixes are absent.
- Ignore `2K`/`4K` resolution tokens instead of treating them as material slots.
- Prevent unknown files from producing empty material groups with a `None` package path.
- Keep import tasks paired with their detected assets, including UDIM-skipped files.
- Reconfigure an existing imported texture when `replace_existing` is disabled.
- Avoid renaming every object from a multi-object FBX to the same destination.

### Added

- Detection and compression profiles for Cavity, Gloss, Specular, Bump and Metalness maps.

## [0.2.0] - 2026-08-19

### Added

- Generate a connected `M_*_Auto` material when the selected master material is missing.
- Automatic BaseColor, Normal, Roughness, Metallic, AO, Emissive, Opacity and OpacityMask graph connections.
- ORM (`R=AO, G=Roughness, B=Metallic`) and RMA (`R=Roughness, G=Metallic, B=AO`) packed-map support.
- Configurable texture setup, fallback material creation and opacity-mask clip value.

### Changed

- OpacityMask textures now use Masks compression with sRGB disabled.
- Explicit mask/opacity semantics select Masked/Translucent for generated materials.
- Automatic mesh assignment now respects `auto_assign_to_mesh`.

## [0.1.0] - 2026-08-19

### Added

- Simplified Chinese and English runtime localization layer.
- Localized toolbar, dialogs, progress messages, reports, and bundled Editor Utility Widgets.
- Safe conversion between localized category/blend-mode labels and original English internal values.
- `language` setting with `zh_CN` and `en_US` options.
- Configuration compatibility and basic JSON error handling.

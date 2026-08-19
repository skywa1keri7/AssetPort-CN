# Changelog

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

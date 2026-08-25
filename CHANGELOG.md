# Changelog

## Unreleased — 0.4.2-dev

- Fixed dedicated `_Opacity` textures not binding to the bundled Decal master's `OpacityMask` parameter while preserving custom masters that expose `Opacity` directly.

## [0.4.1] - 2026-08-25

- Added bilingual Chinese/English parameter-group headers to all four bundled master materials.
- Added bilingual Chinese/English labels for the individual texture, scalar, vector, and switch parameters.
- Added bilingual/legacy parameter alias resolution so older English custom master materials remain compatible.
- Added a safe migration path for existing material-instance overrides when bundled master parameters are renamed.
- Corrected the artist-facing `Metalic` and `Speculer` group-label spellings.

## [0.4.0] - 2026-08-25

- Incorporated upstream v1.5.2 category inheritance and Atlas category resolution.
- Added Vehicles/Effects categories and localized UI choices.
- Added `skm_`, `anim_`, `_alb`, and `_arm` naming aliases.
- Incorporated the upstream Skeletal Mesh import and multi-material assignment fixes.
- Added a localized Decal choice to the transparency workflow.
- Added a bundled Deferred Decal master material and safe fallback generation.
- Enabled embedded FBX LOD import and separate `_LOD0/_LOD1/...` Static Mesh files, including Atlas kits.
- Added bilingual guidance inside the bundled master-material graphs while preserving stable English parameter identifiers.
- Reworked README into complete Chinese and English sections.

## [0.3.0] - 2026-08-22

### Added

- Integrated upstream Asset-Port v1.5.0 Atlas / modular-kit grouping and routing.
- Apply automatic blend-mode selection and fallback material generation to shared Atlas materials.
- Assign a shared Atlas material to every mesh in the modular kit when automatic assignment is enabled.
- Localized Atlas counts in pipeline logs and import reports.
- Added focused tests for prefixless marketplace filenames and additional map suffixes.

### Changed

- Rebased the public CN edition onto a real GitHub fork of `Colosyn/Asset-Port`.
- Preserved v1.5.0 task pairing while retaining existing-texture reconfiguration and safe multi-object FBX naming.
- Restored upstream naming conventions and the bug-report template.

### Fixed

- Keep Atlas import tasks paired with their detected assets during texture configuration and reporting.
- Avoid renaming all objects produced by a multi-object FBX to the same destination.

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

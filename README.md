# AssetPort-CN

[中文](#中文说明) · [English](#english)

AssetPort-CN 是 [Colosyn/Asset-Port](https://github.com/Colosyn/Asset-Port) 原作者认可、由社区独立维护的 UE5 双语增强版。项目保留上游的英文内部标识和 MIT License，并面向美术生产流程增加自动材质、贴图设置、Atlas、Decal 与 LOD 支持。

AssetPort-CN is an independently maintained bilingual UE5 fork of [Colosyn/Asset-Port](https://github.com/Colosyn/Asset-Port), created with the upstream author's approval. It preserves the upstream English identifiers and MIT License while adding artist-oriented material, texture, Atlas, Decal, and LOD workflows.

> 当前版本 / Current version: `0.4.1 Beta`。本次更新由 AssetPort-CN 独立开发，专注于材质参数的中英双语显示与兼容迁移。This AssetPort-CN-specific release focuses on bilingual material parameters and compatible migration.

---

## 中文说明

### 主要功能

- 主导入窗口、预览窗口、透明材质窗口支持简体中文/英文运行时本地化。
- 主材质缺失时自动生成 `M_资源名_Auto`，连接常用 PBR 贴图。
- 自动识别并配置 BaseColor、Normal、Roughness、Metallic、AO、Emissive、Opacity、OpacityMask、ORM、RMA 等贴图。
- 根据用途自动设置纹理压缩和 sRGB；遮罩及通道打包纹理关闭 sRGB。
- 兼容没有 `T_`/`SM_` 前缀的 Marketplace/Fab 命名，并忽略 `2K`、`4K` 等分辨率标记。
- 支持 Atlas/模块化套件：多个静态网格共享一套贴图和材质。
- 同步 v1.5.2 的分类继承、载具/特效分类、骨骼网格导入与多材质修复。
- 识别 `skm_`、`anim_`、`_alb`、`_arm` 等 Fab/Marketplace 别名。
- 透明材质弹窗新增“贴花”选项，可创建 Deferred Decal 材质。
- 支持 FBX 内嵌 LOD，以及单独导出的 `_LOD0/_LOD1/...` 静态网格文件。
- 内置母材质图、材质实例参数组与具体参数名均采用“中文 / English”双语显示。

### Decal / 贴花材质

检测到透明贴图或 BaseColor Alpha 后，透明材质设置窗口现在提供“不透明”“遮罩”“半透明”和“贴花”。选择“贴花”后，工具优先使用：

```text
/Game/Python/Materials/M_Master_Decal
```

如果该母材质不存在且启用了兜底材质，工具会生成 Material Domain 为 `Deferred Decal` 的普通材质。贴花材质应放到 Decal Actor 或 Decal Component 上，因此工具不会把它自动挂进静态网格材质槽。

### LOD 导入

单个 FBX 内已有 LOD Group 时，导入器会启用 FBX LOD 导入。单独导出的静态网格可使用：

```text
SM_env_Rock_LOD0.fbx
SM_env_Rock_LOD1.fbx
SM_env_Rock_LOD2.fbx
T_env_Rock_D.png
T_env_Rock_N.png
```

也可以使用无后缀基础网格加 `_LOD1`、`_LOD2`。Atlas/模块化套件写成：

```text
SM_env_Rock01-RockKit_LOD0.fbx
SM_env_Rock01-RockKit_LOD1.fbx
SM_env_Rock02-RockKit_LOD0.fbx
SM_env_Rock02-RockKit_LOD1.fbx
T_env_RockKit_D.png
T_env_RockKit_ORM.png
```

独立 LOD 当前针对 Static Mesh。骨骼网格仍使用原有导入流程，遇到独立 LOD 文件时会警告而不会错误合并。

### 自动材质策略

工具优先使用配置的四种母材质创建材质实例：

```json
{
  "parent_material_opaque": "/Game/Python/Materials/M_Master_Opaque",
  "parent_material_masked": "/Game/Python/Materials/M_Master_Masked",
  "parent_material_translucent": "/Game/Python/Materials/M_Master_Translucent",
  "parent_material_decal": "/Game/Python/Materials/M_Master_Decal"
}
```

缺少相应母材质且 `auto_create_material_fallback` 为 `true` 时生成 `M_资源名_Auto`。单独的 Roughness、Metallic、AO 贴图优先于 ORM/RMA 中的对应通道。为带 Alpha 的 BaseColor 选择 Masked、Translucent 或 Decal 且没有单独透明贴图时，会使用 BaseColor Alpha。

材质实例中的参数组标题和具体参数名均采用“中文 / English”双语形式。导入器会自动识别新版双语参数，同时保留 `BaseColour`、`Normal`、`UseORM` 等旧英文别名，因此使用旧版英文参数的自定义母材质仍然兼容。升级已有工程时，应在关闭常规 UE Editor 后通过 UE Python 运行 [`tools/localize_material_parameters_unreal.py`](tools/localize_material_parameters_unreal.py) 一次，将既有材质实例中的参数覆盖安全迁移到双语名称；操作前仍建议备份工程。

### 配置

```json
{
  "auto_create_mi": true,
  "auto_create_material_fallback": true,
  "auto_configure_textures": true,
  "auto_assign_to_mesh": true,
  "auto_import_lods": true,
  "replace_existing": false,
  "language": "zh_CN",
  "opacity_mask_clip_value": 0.333
}
```

- `auto_import_lods`：导入 FBX 内嵌 LOD，并将独立 `_LOD#` 文件挂到基础 Static Mesh。
- `auto_assign_to_mesh`：自动给普通网格分配材质；Decal 始终不会分配给网格槽。
- `opacity_mask_clip_value`：Masked 材质裁剪阈值，限制在 0～1。
- `language`：支持 `zh_CN` 和 `en_US`。

### 安装

本项目沿用上游的 `Content/Python` 安装方式，不是标准 `.uplugin`。

1. 在 UE 项目中启用 `Python Editor Script Plugin` 和 `Editor Scripting Utilities`。
2. 将 `asset_port/`、`Materials/`、`Widgets/`、`importer_config.json`、`init_unreal.py` 复制到项目的 `Content/Python/`。
3. 重启 Unreal Editor。

不要把外层 `AssetPort-CN` 文件夹整体放入 `Content/Python`。

### 已知限制

- Widget 固定文字由 Python 在窗口生成后替换；上游修改控件名时需要同步本地化映射。
- 语言通过 JSON 切换，暂时没有窗口内语言开关。
- 安装路径仍固定为 `/Game/Python`。
- Height 贴图会设置为数据纹理，但不会自动连接位移。
- 独立文件 LOD 当前只支持 Static Mesh；FBX 内嵌 LOD 由 UE 导入器处理。

---

## English

### Highlights

- Runtime Simplified Chinese/English localization for the main, preview, and transparency windows.
- Connected `M_*_Auto` fallback materials when a configured master is missing.
- Automatic PBR mapping and texture settings for Base Color, Normal, Roughness, Metallic, AO, Emissive, Opacity, Opacity Mask, ORM, RMA, and related aliases.
- Prefixless Marketplace/Fab filenames with resolution tokens such as `2K` and `4K` ignored during grouping.
- Asset-group/Atlas category inheritance, Vehicles/Effects routing, and the v1.5.2 Skeletal Mesh fixes.
- `skm_`, `anim_`, `_alb`, and `_arm` Fab/Marketplace aliases.
- Atlas/modular-kit workflow with one shared material across multiple meshes.
- A `Decal` choice in the transparency dialog, backed by a Deferred Decal master material.
- Embedded FBX LOD import and separately exported `_LOD0/_LOD1/...` Static Mesh files.
- Bilingual Chinese/English graph legends, parameter groups, and individual parameter labels in all bundled master materials, with legacy English aliases retained for custom-master compatibility.

### Decal materials

The transparency dialog now offers `Opaque`, `Masked`, `Translucent`, and `Decal`. Decal uses `/Game/Python/Materials/M_Master_Decal`. If the master is missing and fallback generation is enabled, AssetPort-CN creates a material with the `Deferred Decal` domain. Decal materials belong on Decal Actors or Decal Components, so they are intentionally not assigned to Static Mesh material slots.

### LOD import

LOD groups embedded in one FBX are enabled through the FBX import settings. Separately exported Static Mesh LODs use `SM_env_Rock_LOD0.fbx`, `SM_env_Rock_LOD1.fbx`, and so on. An unsuffixed base mesh plus `_LOD1` and later files is also valid. Atlas meshes use the marker after the kit name, for example `SM_env_Rock01-RockKit_LOD1.fbx`.

Separate-file LOD attachment currently targets Static Mesh assets. Skeletal Mesh files remain on the original import path and produce a warning instead of being merged incorrectly.

### Material policy

AssetPort-CN first tries the configured Opaque, Masked, Translucent, or Decal master. If it is unavailable and fallback generation is enabled, it creates `M_<Asset>_Auto` and wires recognized PBR inputs. Dedicated Roughness, Metallic, and AO textures take priority over matching ORM/RMA channels. Base Color alpha is used for Masked, Translucent, or Decal when no dedicated opacity texture exists.

Material Instance group headers and individual parameters, plus the master-material graph legends, are bilingual. The importer resolves the new bilingual names first and falls back to legacy identifiers such as `BaseColour`, `Normal`, and `UseORM`, so existing English custom masters remain compatible. When upgrading an existing project, close the regular UE Editor and run [`tools/localize_material_parameters_unreal.py`](tools/localize_material_parameters_unreal.py) once through UE Python so stored Material Instance overrides follow the renamed bundled parameters; back up the project first.

### Configuration and installation

See `importer_config.json`. The new keys are `parent_material_decal` and `auto_import_lods`; `language` accepts `zh_CN` or `en_US`.

Enable `Python Editor Script Plugin` and `Editor Scripting Utilities`, then copy `asset_port/`, `Materials/`, `Widgets/`, `importer_config.json`, and `init_unreal.py` into the project's `Content/Python/` directory and restart Unreal Editor. Copy the repository contents, not the outer `AssetPort-CN` folder itself.

### Known limitations

- Widget text is relabelled at runtime; renamed upstream widgets require localization-map updates.
- Language selection currently lives in JSON rather than in the tool window.
- The content path remains `/Game/Python`.
- Height maps are configured as data textures but are not connected to displacement.
- Separate-file LOD attachment currently supports Static Mesh assets only.

---

## Upstream, authorship, and license / 上游、署名与许可证

- Upstream / 原项目: https://github.com/Colosyn/Asset-Port
- Original author / 原作者: Colosyn (Shahnawaz Hussain)
- License / 许可证: MIT License

The original copyright notice and MIT License are preserved in [LICENSE](LICENSE). See [NOTICE](NOTICE) for provenance and modification notes.

原始版权声明和 MIT License 全文保留在 [LICENSE](LICENSE)；来源与修改说明见 [NOTICE](NOTICE)。

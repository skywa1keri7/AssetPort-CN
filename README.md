# AssetPort-CN

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Unreal Engine Version](https://img.shields.io/badge/Unreal%20Engine-5.6%20%7C%205.7%20Verified-blue)](https://www.unrealengine.com/)
[![Language: Python](https://img.shields.io/badge/Language-Python-green)](https://www.python.org/)
[![UI: Simplified Chinese / English](https://img.shields.io/badge/UI-%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87%20%7C%20English-red)](#语言与运行环境)

[中文说明](#中文说明) · [English](#english) · [开发计划 / Roadmap](ROADMAP.md) · [更新记录 / Changelog](CHANGELOG.md)

AssetPort-CN 是 [Colosyn/Asset-Port](https://github.com/Colosyn/Asset-Port) 原作者认可、由社区独立维护的 UE5 双语增强版。项目保留上游的英文内部标识和 MIT License，并面向美术生产流程增加自动材质、贴图设置、Atlas、Decal 与 LOD 支持。

AssetPort-CN is an independently maintained bilingual UE5 fork of [Colosyn/Asset-Port](https://github.com/Colosyn/Asset-Port), created with the upstream author's approval. It preserves the upstream English identifiers and MIT License while adding artist-oriented material, texture, Atlas, Decal, and LOD workflows.

> 当前版本 / Current version: `0.4.3 Beta`。本次更新将四颗内置母材质重新保存为 UE5.6 兼容资产，同时保留 0.4.2 的贴花透明贴图绑定修复。This release rebuilds all four bundled masters as UE5.6-compatible assets while retaining the 0.4.2 Decal opacity-binding fix.

---

## 中文说明

### 语言与运行环境

| 项目 | 当前状态 |
| --- | --- |
| 界面语言 | 简体中文 `zh_CN`、英文 `en_US` |
| Unreal Engine | UE5.6、UE5.7 已验证；其他小版本建议先在测试工程验证 |
| 母材质资产版本 | 四颗内置母材质由 UE5.6 保存 |
| 操作系统 | Windows 11 已验证；其他桌面平台尚未完整测试 |
| Python | 使用 Unreal Editor 内置 Python，不需要另外安装系统 Python |
| 必需插件 | `Python Editor Script Plugin`、`Editor Scripting Utilities` |
| 安装形式 | 复制到项目的 `Content/Python/`；本项目不是 `.uplugin` |

运行时界面支持中英文切换，但内部类别名、配置键和兼容别名继续使用英文，方便与上游同步，也避免语言切换破坏既有工程。

### UE 版本兼容性

Unreal 的 `.uasset` 通常可以由新版本读取旧版本资产，但旧版本不能可靠读取新版本保存的资产。代码兼容并不等于二进制资产兼容。

- `v0.4.2` 的四颗母材质曾由 UE5.7 保存，因此 UE5.6 会将它们视为不可读取资产，表现为内容浏览器中“母材质消失”。
- `v0.4.3` 已将 `Opaque`、`Masked`、`Translucent`、`Decal` 四颗母材质全部使用 UE5.6 重新生成并保存。
- 四颗 UE5.6 母材质已在 UE5.7 完成向前兼容加载、双语参数、透明遮罩和 Deferred Decal 检查。
- 默认 VT 贴图和 Editor Utility Widgets 保持 UE5.3 资产版本，可由 UE5.6/5.7 向前读取。
- 自动测试会检查仓库内 `.uasset` 的引擎版本标记，阻止误提交需要 UE5.7 或更高版本的发行资产。
- 当前不宣称完整支持 UE5.3～5.5；计划中的“当前引擎自动生成母材质”将进一步减少二进制版本依赖，详见 [开发计划](ROADMAP.md)。

发布包的推荐范围是 UE5.6 和 UE5.7。更高 UE5 小版本预计可向前读取这些资产，但在列入“已验证”前仍应先用测试工程检查。

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

四颗内置母材质使用 UE5.6 重新保存，并已在 UE5.7 中完成向前兼容加载检查。当前已验证范围为 UE5.6 和 UE5.7；其他小版本应先在测试工程中验证。

### 开发计划

后续方向包括当前 UE 版本自动生成共享母材质、双面植物材质、自发光材质、布料/绒毛材质，以及更完整的版本兼容矩阵。规划不代表功能已经完成，具体范围与优先级见 [ROADMAP.md](ROADMAP.md)。

### 已知限制

- Widget 固定文字由 Python 在窗口生成后替换；上游修改控件名时需要同步本地化映射。
- 语言通过 JSON 切换，暂时没有窗口内语言开关。
- 安装路径仍固定为 `/Game/Python`。
- Height 贴图会设置为数据纹理，但不会自动连接位移。
- 独立文件 LOD 当前只支持 Static Mesh；FBX 内嵌 LOD 由 UE 导入器处理。

---

## English

### Languages and environment

| Item | Current status |
| --- | --- |
| UI languages | Simplified Chinese `zh_CN` and English `en_US` |
| Unreal Engine | Verified on UE5.6 and UE5.7; test other minor versions before production use |
| Master asset baseline | All four bundled master materials are saved with UE5.6 |
| Operating system | Verified on Windows 11; other desktop platforms are not fully tested |
| Python | Uses Unreal Editor's embedded Python; no separate system Python installation is required |
| Required plugins | `Python Editor Script Plugin` and `Editor Scripting Utilities` |
| Installation model | Copy into the project's `Content/Python/`; this is not a `.uplugin` package |

The runtime UI can switch languages, while internal category identifiers, configuration keys, and compatibility aliases remain in English for upstream interoperability and project stability.

### Unreal Engine compatibility

New Unreal versions can generally read assets saved by older versions, but older versions cannot reliably read newer `.uasset` files. Source-code compatibility does not guarantee binary-asset compatibility.

- The four masters in `v0.4.2` were accidentally saved by UE5.7, so UE5.6 treated them as unreadable and hid them from the Content Browser.
- `v0.4.3` rebuilds and saves the bundled Opaque, Masked, Translucent, and Decal masters with UE5.6.
- The rebuilt masters passed UE5.7 forward-loading checks, including bilingual parameters, opacity-mask inputs, and the Deferred Decal domain.
- Default VT textures and Editor Utility Widgets remain UE5.3 assets and forward-load in UE5.6/5.7.
- An automated test now checks engine markers in bundled `.uasset` files and rejects release assets that require UE5.7 or newer.
- Full UE5.3–5.5 support is not claimed. A future current-engine master-material generator is planned to reduce binary-version coupling; see the [roadmap](ROADMAP.md).

The recommended release range is UE5.6 and UE5.7. Newer UE5 minor releases are expected to forward-load these assets, but remain unverified until tested in a clean project.

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

The four bundled master materials are saved with UE5.6 and have passed forward-loading checks in UE5.7. The currently verified range is UE5.6 and UE5.7; validate any other minor version in a test project first.

### Roadmap

Planned directions include current-engine shared master generation, two-sided foliage, emissive, and cloth/fuzz material workflows, plus a broader engine compatibility matrix. Planned items are not completed features; see [ROADMAP.md](ROADMAP.md) for scope and priorities.

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

# AssetPort-CN

AssetPort-CN 是 [Colosyn/Asset-Port](https://github.com/Colosyn/Asset-Port) 的非官方中文增强版。它为 Unreal Engine 5 的批量资源导入流程增加简体中文/英文双语界面，同时保持原项目的英文内部标识与资源命名逻辑，避免本地化影响导入结果。

> 当前版本：`0.2.0`。建议先在测试工程中使用。

## 当前改动

- 工具栏按钮和提示支持简体中文、英文。
- 主导入窗口、预览窗口、透明材质窗口运行时本地化。
- 分类下拉框显示本地化文本，但内部仍使用原英文分类值。
- `Opaque`、`Masked`、`Translucent` 可显示为“不透明”“遮罩”“半透明”，材质逻辑仍接收原英文值。
- 文件夹选择、错误对话框、进度提示、预览警告和导入报告支持双语。
- 配置读取增加缺失字段、未知字段和损坏 JSON 的基本容错。
- 主材质缺失时自动生成 `M_资源名_Auto` 普通材质，并连接已识别贴图。
- 自动材质支持 BaseColor、Normal、Roughness、Metallic、AO、Emissive、Opacity、OpacityMask、ORM 和 RMA。
- 根据贴图用途自动配置压缩方式和 sRGB；遮罩与通道打包图使用 `Masks` 并关闭 sRGB。
- 明确识别到 OpacityMask 时自动使用 `Masked`，识别到 Opacity 时自动使用 `Translucent`。

## 自动材质策略

导入时仍优先使用 `parent_material_opaque`、`parent_material_masked` 和
`parent_material_translucent` 指定的主材质创建材质实例。只有当前混合模式所需的主材质不存在，且
`auto_create_material_fallback` 为 `true` 时，才会在资源目录生成普通材质：

```text
M_资源名_Auto
```

单独的 Roughness、Metallic、AO 贴图优先于 ORM/RMA 中相同的通道，避免输入重复连接。
如果用户为带 Alpha 的 BaseColor 选择了 Masked 或 Translucent，又没有单独的透明贴图，自动材质会使用 BaseColor Alpha。

常用配置：

```json
{
  "auto_create_mi": true,
  "auto_create_material_fallback": true,
  "auto_configure_textures": true,
  "auto_assign_to_mesh": true,
  "opacity_mask_clip_value": 0.333
}
```

- `auto_create_mi`：启用整个自动材质构建步骤（包括实例和兜底普通材质）。
- `auto_create_material_fallback`：缺少主材质时生成普通材质；关闭后会在报告中记录错误。
- `auto_configure_textures`：自动设置贴图压缩方式和 sRGB。
- `opacity_mask_clip_value`：Masked 材质的裁剪阈值，配置读取时限制在 0～1。

## 安装

本项目目前沿用上游的 Content/Python 安装方式，不是标准 `.uplugin` 插件。

1. 在 Unreal Engine 项目中启用：
   - Python Editor Script Plugin
   - Editor Scripting Utilities
2. 将本仓库以下内容复制到项目的 `Content/Python/`：
   - `asset_port/`
   - `Materials/`
   - `Widgets/`
   - `importer_config.json`
   - `init_unreal.py`
3. 重启 Unreal Editor。

不要把外层 `AssetPort-CN` 文件夹整体放进 `Content/Python`，应复制它里面的内容。

## 切换语言

编辑 `importer_config.json`：

```json
{
  "language": "zh_CN"
}
```

支持的值：

- `zh_CN`：简体中文
- `en_US`：英文

修改后关闭并重新打开 AssetPort 窗口。工具栏名称需要刷新菜单或重启编辑器后更新。

## 双语实现原则

界面只翻译显示文本，以下内部值保持英文：

- 分类路径：`Environment`、`Weapons`、`Props`、`Characters`
- 混合模式：`Opaque`、`Masked`、`Translucent`
- 资源前后缀及材质参数名
- Unreal 资源路径

这样中文界面不会改变原项目的路由、材质和命名行为。

## 已知限制

- Editor Utility Widget 的固定文字通过 Python 在窗口生成后替换；如果上游重命名控件，需要同步更新 `asset_port/ui_localization.py`。
- 当前语言通过 JSON 配置切换，窗口内语言选择器将在后续版本加入。
- 上游 Widget 资源位于 `/Game/Python/Widgets`，当前版本仍依赖该安装路径。
- 自动生成材质目前连接常用 PBR 输入；Height 只会配置为 Masks，不会擅自连接位移。

## 上游与许可证

本项目基于 AssetPort 修改：

- 原项目：https://github.com/Colosyn/Asset-Port
- 原作者：Colosyn（Shahnawaz Hussain）
- 原许可证：MIT License

原项目版权声明和 MIT 许可证全文保留在 [LICENSE](LICENSE) 中。

## 开发计划

- [x] Python 菜单、对话框和提示双语化
- [x] 主窗口、预览窗口、透明材质窗口运行时双语化
- [x] 分类与混合模式显示值/内部值分离
- [x] 缺少主材质时生成基础 PBR 材质
- [x] 按贴图用途自动设置压缩与 sRGB
- [ ] 在主窗口中增加语言切换控件
- [ ] 增加可视化设置面板
- [ ] 修复并测试 UDIM、EXR Alpha 和重复事件绑定问题
- [ ] 封装为标准 Unreal Engine 插件

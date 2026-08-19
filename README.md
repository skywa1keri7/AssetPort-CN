# AssetPort-CN

AssetPort-CN 是 [Colosyn/Asset-Port](https://github.com/Colosyn/Asset-Port) 的非官方中文增强版。它为 Unreal Engine 5 的批量资源导入流程增加简体中文/英文双语界面，同时保持原项目的英文内部标识与资源命名逻辑，避免本地化影响导入结果。

> 当前状态：双语 UI 第一阶段。建议先在测试工程中使用。

## 当前改动

- 工具栏按钮和提示支持简体中文、英文。
- 主导入窗口、预览窗口、透明材质窗口运行时本地化。
- 分类下拉框显示本地化文本，但内部仍使用原英文分类值。
- `Opaque`、`Masked`、`Translucent` 可显示为“不透明”“遮罩”“半透明”，材质逻辑仍接收原英文值。
- 文件夹选择、错误对话框、进度提示、预览警告和导入报告支持双语。
- 配置读取增加缺失字段、未知字段和损坏 JSON 的基本容错。

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
- [ ] 在主窗口中增加语言切换控件
- [ ] 增加可视化设置面板
- [ ] 修复并测试 UDIM、EXR Alpha 和重复事件绑定问题
- [ ] 封装为标准 Unreal Engine 插件


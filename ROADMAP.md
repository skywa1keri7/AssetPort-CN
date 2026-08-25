# AssetPort-CN Development Roadmap / 开发计划

[中文](#中文计划) · [English](#english-roadmap) · [返回 README / Back to README](README.md)

> 本路线图用于说明方向，不承诺具体发布日期。功能只有在实现、测试并写入 Changelog 后才视为正式支持。
>
> This roadmap communicates direction, not release dates. A feature is supported only after implementation, testing, and inclusion in the Changelog.

---

## 中文计划

### 近期：稳定性与版本兼容

- 建立 UE5.6、UE5.7、UE5.8 的基础兼容测试矩阵，分别记录“可加载”“可导入”“生产复测”状态。
- 在发行检查中持续限制二进制资产的最低引擎版本，避免新版本 `.uasset` 意外进入旧版本兼容包。
- 增加启动诊断：显示当前 UE 版本、配置语言、必需插件、母材质状态和缺失资产。
- 为旧发行版本提供更清楚的升级提示和兼容性说明。

### 中期：降低二进制母材质依赖

- 开发“当前引擎生成共享母材质”：首次运行时由 Python 在用户当前 UE 版本中创建 Opaque、Masked、Translucent 和 Decal 母材质。
- 保留混合兜底策略：内置母材质可用时直接使用；不可用时自动生成共享母材质；仍失败时再生成当前已有的 `M_*_Auto` 单材质。
- 为自动生成的母材质增加结构版本号、完整性检查和安全重建入口，不覆盖用户自行修改的材质。
- 研究减少默认 VT 贴图二进制依赖的方法，同时保留普通纹理和虚拟纹理工作流。

### 材质工作流设想

- **双面植物材质**：Two Sided、Two Sided Foliage、Subsurface Color、Opacity Mask、法线方向和风动接口；优先服务树叶、草、卡片植物。
- **自发光材质**：自发光贴图、颜色、强度、曝光补偿与 Bloom 友好参数；区分普通表面自发光和特效用途。
- **布料/绒毛材质**：先研究 Cloth/Fuzz Shading Model、Fuzz Color、强度和粗糙度参数；Chaos Cloth 资产导入属于另一条更大的工作流，不与材质预设混为一谈。
- **材质预设选择**：根据命名、贴图组合或用户选择，在标准 PBR、植物、自发光、布料和贴花之间选择合适模板。
- **高级表面**：继续评估 Height/Displacement、Detail Normal、Clear Coat 和各向异性材质的生产价值与版本差异。

### 工具与美术体验

- 在窗口中切换语言和常用导入设置，减少直接编辑 JSON。
- 为每次导入提供更直观的材质、贴图、LOD 和警告摘要。
- 增加“检查/重建 AssetPort-CN 母材质”和“打开问题资产”入口。
- 扩充 Marketplace/Fab 命名样本和美术同学的真实项目回归测试。

---

## English roadmap

### Near term: stability and engine compatibility

- Establish a UE5.6, UE5.7, and UE5.8 compatibility matrix that separately records asset loading, import smoke tests, and production retests.
- Keep release-time engine-marker checks so newer `.uasset` files cannot silently enter an older-compatible package.
- Add startup diagnostics for engine version, language, required plugins, master-material health, and missing assets.
- Improve upgrade warnings and compatibility notes for older releases.

### Mid term: reduce binary master-material coupling

- Build shared Opaque, Masked, Translucent, and Decal masters with Python in the user's current engine on first run.
- Use a layered fallback: bundled masters first, generated shared masters second, and the existing per-asset `M_*_Auto` material as the final fallback.
- Add a schema version, integrity checks, and a safe rebuild command for generated masters without overwriting user-customized materials.
- Investigate reducing binary default-VT-texture dependencies while retaining regular and virtual-texture workflows.

### Material workflow ideas

- **Two-sided foliage**: Two Sided, Two Sided Foliage, Subsurface Color, Opacity Mask, normal handling, and wind hooks for leaves, grass, and card vegetation.
- **Emissive**: emissive texture, color, intensity, exposure compensation, and Bloom-friendly controls for surfaces and effects.
- **Cloth/fuzz**: initially target the Cloth/Fuzz shading model and artist-facing fuzz color, strength, and roughness controls. Chaos Cloth asset import is a separate, larger workflow.
- **Material preset selection**: choose Standard PBR, Foliage, Emissive, Cloth, or Decal templates from naming, texture combinations, or an explicit artist choice.
- **Advanced surfaces**: continue evaluating Height/Displacement, Detail Normal, Clear Coat, and anisotropy against production value and engine-version differences.

### Tooling and artist experience

- Move language and common import settings into the tool window instead of requiring direct JSON edits.
- Provide clearer material, texture, LOD, and warning summaries for every import.
- Add “Validate/Rebuild AssetPort-CN Masters” and “Open Problem Asset” actions.
- Expand Marketplace/Fab filename fixtures and regression tests based on real artist projects.

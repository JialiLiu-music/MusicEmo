# 音乐情绪回归的少样本输出校准

[English](README.md) | **简体中文**

音乐情绪跨数据集少样本输出校准的论文稿件、配套图表与 CPU 演示代码。

## 阅读入口

- [英文论文正文](manuscript_en.md)
- [HTML 阅读版本](manuscript_en.html) — GitHub 显示源代码，可下载仓库后在本地打开阅读。
- [Word 可编辑版本](manuscript_en.docx)
- [图表及图注](figures/captions.md)
- [文献证据记录](working/literature_evidence.json)

## 研究概述

本研究使用冻结的 MERT 音乐表征和在 DEAM 上训练的情绪预测头，在 PMEmo 完整副歌数据上比较评分预算为 5 首或 10 首歌曲时的输出校准方法。

在预设的主要对比中，使用 10 首歌曲的评分、仅对唤醒度进行半强度偏移校正，在 334 个固定评价风险组代表上使唤醒度均方误差平均降低 13.50%。论文正文和附录记录了数据职责、完整对照、适应池稳定性以及结论适用范围。

仓库提供英文论文稿件。作者信息、目标期刊格式及正式投稿声明仍需补充。

## CPU 音乐情绪演示

网站源码位于 [`code/`](code/README.md)，采用前后端分离架构：前端为 React/TypeScript 中文界面，后端为在 CPU 上运行的 FastAPI 服务。

演示支持：

- 上传音频片段
- 整体效价与唤醒度双轴预测
- 使用 10 秒窗口、5 秒步长生成窗口级评分曲线
- 播放联动可视化
- JSON 和 CSV 导出

窗口级曲线来自静态模型，不应视为经过验证的逐秒情绪识别结果。默认不启用目标域校准。

启动方法、固定版本 MERT 模型下载及论文预测头校验说明见 [`code/README.md`](code/README.md)。

仓库不包含模型权重、试听音乐、虚拟环境或 `node_modules`。克隆代码后，仍需另行准备所需模型资产。

自动测试与真实 CPU 执行的范围见 [`code/VALIDATION.md`](code/VALIDATION.md) 和 [`code/TIMELINE_UPGRADE-20261012.md`](code/TIMELINE_UPGRADE-20261012.md)。将源码上传至本仓库不代表演示网站已部署到公网。

## 文件结构

- `manuscript_en.*`：Markdown、HTML 和 Word 格式的论文正文。
- `figures/`：6 幅图的 PNG、PDF 和 SVG 版本、图注及来源校验清单。
- `scripts/`：图表生成、正文结构检查和文档导出脚本。
- `working/`：证据地图、文献记录、章节蓝图及修订说明。

## 脚本与文档生成

在仓库根目录运行 `python scripts/audit_manuscript.py`，可检查正文结构与文件引用。

如需从 Markdown 更新 HTML 和 Word 版本，请先使用 Python 3.10 或以上版本运行 `python -m pip install -r scripts/requirements-documents.txt` 安装依赖，再运行 `python scripts/build_manuscript_outputs.py`。

HTML 使用原生 MathML 离线显示公式，适用于现代 Chrome、Edge 或 Firefox。Word 使用 Pandoc 将公式转换为可编辑的原生公式对象。Markdown 采用 GitHub 支持的 `$...$` 和 `$$...$$` 公式定界符。

运行 `python scripts/test_math_rendering.py`，可核验 10 个独立公式、行内公式及 Word 公式结构，并检查数学表达式相对于原始提交保持不变。

运行 `python scripts/test_reporting_integrity.py`，可检查贡献措辞修订前后的完整结果表、附录、参考文献和必要限制是否保持一致。

GitHub 源码页面只展示 HTML 代码，阅读 HTML 版本需要在本地打开。阅读 Markdown 正文时，请使用 GitHub 的渲染视图，而非 Raw 源码视图。

## 数据、模型与可复现性

图表生成依赖 `numpy`、`matplotlib` 以及原工作区 `进度/` 目录中的实验 JSON 文件。

完整原始实验产物、模型权重、音乐音频及本地安装依赖不包含在本仓库中。仓库中的 `figure_manifest.json` 保留来源路径与 SHA 记录，但不能据此声称已公开完整实验数据。

商业歌曲音频未随仓库发布。数据与模型来源请参见论文及参考文献。

# Markdown-to-PDF 📄✨

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Managed by: uv](https://img.shields.io/badge/Managed%20by-uv-purple)](https://github.com/astral-sh/uv)

**Markdown-to-PDF** 是专为高质量文档排版设计的轻量级、出版级 PDF 导出与渲染引擎。不仅针对中文排版、LaTeX 数学公式、代码高亮、表格及 GitHub Callout 警示框进行了深度调优，还原生集成了 **Antigravity** 智能体开发环境的 Artifact 实时预览交互能力。

---

## 🌟 核心特性 (Features)

- 🎨 **多款精美主题**:
  - **`modern`**: 科技现代蓝调，适合方案设计、技术文档与产品规划。
  - **`academic`**: 严谨学术风，经典衬线字体（Georgia / 宋体）与三线表（Booktabs）。
  - **`report`**: 商业研报风，商务墨绿基调、章节强调线与摘要卡片。
  - **`minimal`**: 黑白瑞士网格极简风，高对比纯净排版。
  - **`github`**: 开发者熟悉的经典 GitHub Markdown 风格。
- 📐 **LaTeX 数学公式完美渲染**: 通过 KaTeX 引擎原生渲染行内 `$E=mc^2$` 与行间多行复杂微积分、矩阵公式，矢量清晰。
- 📦 **GitHub 风格 Callout 警示框**: 完美解析 `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, `[!CAUTION]` 并渲染为精美卡片。
- 📑 **智能分页控制**: 彻底杜绝孤行标题（Orphan headings）、表格行跨页被腰斩等排版瑕疵。
- 🎯 **封面页与目录生成**: 一键生成结构化封面（Title, Subtitle, Abstract, Author, Date）与独立目录页。
- 🚀 **零繁琐依赖 (No GTK / Cairo DLLs)**: 自动调用 Windows 系统自带的 Google Chrome 或 Microsoft Edge 无头打印管道，毫秒级生成。
- 🤖 **Antigravity 原生 Artifact 同步**: 自动生成符合 Generative UI 规范的交互式预览组件，可在 Antigravity 侧边栏即时查看与打开。
- ⚡ **uv 原生支持**: 遵循现代 Python 标准，通过 `uv` 极速管理虚拟环境与依赖。

---

## 🚀 快速上手 (Quick Start)

### 1. 克隆仓库与安装

```bash
git clone https://github.com/haownz/markdown-to-pdf.git
cd markdown-to-pdf
```

安装依赖（使用 [uv](https://github.com/astral-sh/uv) 极速管理）：

```bash
uv sync
```

### 2. 命令行基础使用

转换 Markdown 文件为 PDF：

```bash
uv run python scripts/md_to_pdf.py -i examples/sample_report.md -o output.pdf
```

选择排版主题（如学术风 `academic` 或研报风 `report`）：

```bash
uv run python scripts/md_to_pdf.py -i report.md -o report.pdf --theme academic
```

生成包含封面页、目录与页眉页脚的完整技术白皮书：

```bash
uv run python scripts/md_to_pdf.py `
  -i technical_proposal.md `
  -o technical_proposal.pdf `
  --theme report `
  --title "2026 年度技术架构白皮书" `
  --subtitle "企业级高可用服务架构升级实践" `
  --author "haownz" `
  --cover `
  --toc
```

### 3. 从标准输入管道流式处理

```powershell
Get-Content README.md -Raw | uv run python scripts/md_to_pdf.py -i - -o readme.pdf
```

---

## 🛠️ 参数全景 (CLI Options)

| 参数 | 说明 | 默认值 | 示例 |
| :--- | :--- | :--- | :--- |
| `-i`, `--input` | 输入 Markdown 文件（或 `-` 读取 stdin） | *(必填)* | `-i doc.md` |
| `-o`, `--output` | 输出 PDF 文件路径 | `<name>.pdf` | `-o dist/doc.pdf` |
| `--theme` | 排版主题（`modern` / `academic` / `report` / `minimal` / `github`） | `modern` | `--theme report` |
| `--title` | 文档主标题（可覆盖 Frontmatter） | 首个 H1 / 文件名 | `--title "用户手册"` |
| `--subtitle` | 文档副标题 | 空 | `--subtitle "快速入门指南"` |
| `--author` | 作者署名 | `Antigravity` | `--author "haownz"` |
| `--date` | 生成日期 | 当前日期 | `--date "2026-10-11"` |
| `--cover` | 启用独立正规封面页 | 关闭 | `--cover` |
| `--toc` | 自动生成目录大纲 | 关闭 | `--toc` |
| `--page-size` | 页面纸张大小（`A4`, `Letter`） | `A4` | `--page-size A4` |
| `--orientation`| 页面方向（`portrait`, `landscape`） | `portrait` | `--orientation landscape` |
| `--no-header-footer` | 隐藏页眉与页脚 | 显示 | `--no-header-footer` |
| `--artifact-dir` | 同步生成 Antigravity Generative UI 预览 Artifact | 无 | `--artifact-dir "<path>"` |
| `--open` | 生成后自动打开系统默认 PDF 阅读器 | 关闭 | `--open` |
| `--json` | 输出机器可读 JSON 元数据 | 关闭 | `--json` |

---

## 📁 目录结构 (Repository Structure)

```text
markdown-to-pdf/
├── scripts/
│   ├── md_to_pdf.py         # 核心转换引擎与 CLI 入口
│   └── browser.py           # Headless Chromium / Edge 浏览器调度引擎
├── templates/
│   ├── document.html        # 打印排版 Jinja2 模板
│   ├── artifact_preview.html# Antigravity Generative UI 预览模板
│   └── styles/
│       ├── base.css         # 基础排版、@page 规范与防孤行规则
│       ├── modern.css       # 科技现代主题
│       ├── academic.css     # 学术论文主题
│       ├── report.css       # 商业研报主题
│       ├── minimal.css      # 极简黑白主题
│       └── github.css       # GitHub 经典主题
├── examples/
│   ├── sample_report.md     # 示范文档（含公式、表格、代码、警示框）
│   └── sample_output.pdf    # 示范输出 PDF
├── tests/
│   └── test_conversion.py   # 全主题自动化端到端测试套件
├── pyproject.toml           # uv 项目配置与依赖管理
├── SKILL.md                 # Antigravity Skill 规范描述文件
└── README.md
```

---

## 🧪 运行自动化测试

```bash
uv run python tests/test_conversion.py
```

测试套件将全量验证 5 种排版主题、KaTeX 公式渲染、代码高亮以及 Antigravity Artifact 的完整生成流程。

---

## 📄 开源许可证 (License)

本项目采用 [MIT License](LICENSE) 开源协议。

---
name: markdown-to-pdf
description: >-
  Convert formatted answers, Markdown documents, research reports, and technical guides into publication-quality PDFs with beautiful typesetting (typography, LaTeX math formulas, code syntax highlighting, tables, callout blocks, page numbers, and custom themes) and synchronize interactive artifacts for direct preview in Antigravity. Use whenever the user asks to export or format content as a PDF or generate printable documents.
---

# Markdown-to-PDF Professional Typesetting Skill

This skill converts formatted text, responses, and Markdown documents into publication-quality PDFs with optimized typography, clean pagination, and synchronized Antigravity artifacts.

> [!IMPORTANT]
> Always execute the converter using `uv` according to user rules:
> `uv run python E:\program\markdown-to-pdf\scripts\md_to_pdf.py ...`

---

## 1. Capabilities & Highlights

1. **Publication-Grade Typography**:
   - Optimized Chinese & English font stacks (`Microsoft YaHei`, `PingFang SC`, `Noto Sans SC`, `Segoe UI`, `Georgia`, `Cascadia Code`).
   - Smart page breaks preventing orphan headings (`break-after: avoid;`).
   - Clean table layouts preventing mid-row splits across pages (`break-inside: avoid;`).
2. **Mathematical Formulas**:
   - High-fidelity vector rendering for inline (`$E = mc^2$`) and block (`$$\int_{-\infty}^\infty e^{-x^2} dx = \sqrt{\pi}$$`) formulas via KaTeX.
3. **Rich Elements**:
   - GitHub-style alert callouts (`[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, `[!CAUTION]`).
   - Syntax highlighted code blocks via Pygments.
   - Optional Table of Contents (`--toc`) and formal Cover Page (`--cover`).
4. **Antigravity Artifact Synchronization**:
   - Generates interactive Generative UI HTML preview (`<name>_preview.html`) and summary report (`<name>_summary.md`) directly in Antigravity's artifact directory so the user can inspect the document immediately in the side pane.
5. **Zero Heavy C-Dependencies**:
   - Uses local Headless Chromium (`Google Chrome` or `Microsoft Edge`) already installed on Windows. No GTK+ or Cairo DLL issues.

---

## 2. Standard CLI Usage

### Basic Conversion
```powershell
uv run python E:\program\markdown-to-pdf\scripts\md_to_pdf.py `
  --input "path\to\document.md" `
  --output "path\to\output.pdf" `
  --theme "modern"
```

### Full Report with Cover Page, TOC, and Antigravity Artifacts
```powershell
uv run python E:\program\markdown-to-pdf\scripts\md_to_pdf.py `
  --input "path\to\document.md" `
  --output "path\to\output.pdf" `
  --theme "report" `
  --title "系统架构与技术选型白皮书" `
  --author "haownz" `
  --cover `
  --toc `
  --artifact-dir "<artifact_directory>"
```

### Direct Input from Stdin (Streaming / Ad-hoc Content)
```powershell
$content | uv run python E:\program\markdown-to-pdf\scripts\md_to_pdf.py `
  --input "-" `
  --output "output.pdf" `
  --title "分析报告" `
  --artifact-dir "<artifact_directory>"
```

---

## 3. Options Reference

| 参数 | 说明 | 可选值 / 示例 | 默认值 |
| :--- | :--- | :--- | :--- |
| `-i`, `--input` | 输入 Markdown 文件路径，或 `-` 读取标准输入 | `report.md` / `-` | *(必填)* |
| `-o`, `--output` | 输出 PDF 文件绝对或相对路径 | `dist/output.pdf` | `<input_name>.pdf` |
| `--theme` | 排版视觉主题 | `modern`, `academic`, `report`, `minimal`, `github` | `modern` |
| `--title` | 文档主标题（可覆盖 Frontmatter） | `--title "技术方案报告"` | Frontmatter 或 首个 H1 |
| `--subtitle` | 文档副标题 | `--subtitle "企业级落地指南"` | 无 |
| `--author` | 作者署名 | `--author "haownz"` | `Antigravity` |
| `--date` | 日期字符串 | `--date "2026-10-11"` | 当天日期 |
| `--cover` | 是否生成独立规范的封面页 | 启用该标志即可 | 关闭 |
| `--toc` | 是否自动生成目录（Table of Contents） | 启用该标志即可 | 关闭 |
| `--page-size` | 页面纸张规格 | `A4`, `Letter` | `A4` |
| `--orientation` | 页面方向 | `portrait`, `landscape` | `portrait` |
| `--no-header-footer`| 隐藏页眉与页脚 | 启用该标志即可 | 默认显示页眉页脚 |
| `--artifact-dir` | Antigravity Artifact 目录，生成 HTML & MD 预览 | `<appDataDir>\brain\<id>` | 无 |
| `--open` | 生成后自动在操作系统默认阅读器中打开 | 启用该标志即可 | 关闭 |
| `--json` | 输出机器可读的 JSON 元数据（供 Agent 自动化调用） | 启用该标志即可 | 关闭 |

---

## 4. Theme Styles Showcase

- **`modern`**: 科技清爽风格。深蓝重音、精致边框与现代无衬线字体，最适合通用技术文档与产品方案。
- **`academic`**: 严谨学术论文风格。衬线字体（Georgia / 宋体）、居中标题、经典三线表（Booktabs）与首行缩进。
- **`report`**: 商务研究报告风格。青翠/墨绿商务色调、优雅边线装饰卡片、适合交付客户的商业白皮书与咨询研报。
- **`minimal`**: 黑白极简风格。瑞士网格排版，纯黑白高反差，专注纯文本阅读与印刷。
- **`github`**: GitHub 经典 Markdown 风格。与开发者最熟悉的 GitHub 渲染完全一致。

---

## 5. Artifact Sync in Antigravity Workflow

When generating PDF in an Antigravity conversation:
1. Pass `--artifact-dir "<artifact_directory>"` (e.g. `C:\Users\haowu\.gemini\antigravity\brain\<conversation-id>`).
2. The script automatically outputs:
   - `<name>_preview.html`: Interactive Generative UI card with metadata and PDF open button.
   - `<name>_summary.md`: Markdown summary artifact with file link.
3. The agent points the user to the artifact panel for instantaneous side-by-side review!

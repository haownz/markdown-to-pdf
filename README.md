# Markdown-to-PDF 📄✨

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Managed by: uv](https://img.shields.io/badge/Managed%20by-uv-purple)](https://github.com/astral-sh/uv)

**Markdown-to-PDF** is a lightweight, publication-grade PDF generation and typesetting engine. Tailored for software documentation, research reports, and technical whitepapers, it delivers optimized typography, LaTeX mathematical expressions, Pygments syntax highlighting, structured tables, and GitHub-style Callouts—while integrating natively with the **Google Antigravity** agentic runtime for real-time interactive artifact preview.

---

## 🌟 Key Features

- 🎨 **Five Curated Themes**:
  - **`modern`**: Clean tech aesthetic with indigo accents and crisp typography.
  - **`academic`**: Scholarly paper style featuring serif typography and classic booktabs tables.
  - **`report`**: Executive briefing look with teal corporate borders and section cards.
  - **`minimal`**: Monochrome Swiss minimalist layout maximizing high-contrast readability.
  - **`github`**: Familiar developer-first GitHub markdown style.
- 📐 **Vector Math Rendering**: Full support for inline `$E=mc^2$` and multi-line display equations via KaTeX.
- 📦 **GitHub-Style Callouts**: Native rendering of `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, and `[!CAUTION]` alert boxes.
- 📑 **Smart Page Break Control**: Eliminates orphaned headings (`break-after: avoid`) and prevents table rows from splitting mid-cell across pages.
- 🎯 **Cover Page & TOC**: One-click generation of formal title pages (Title, Subtitle, Abstract, Author, Date) and table of contents.
- 🚀 **Zero Heavy C-Dependencies**: Directly leverages local Headless Chromium (`Google Chrome` or `Microsoft Edge`) already present on Windows. No GTK+ or Cairo DLL issues.
- 🤖 **Native Antigravity Artifact Sync**: Automatically outputs Generative UI preview widgets and Markdown summaries directly into the Antigravity artifact panel.
- ⚡ **Built for uv**: Ultra-fast environment provisioning and dependency management via `uv`.

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/haownz/markdown-to-pdf.git
cd markdown-to-pdf
```

Synchronize virtual environment and dependencies using [uv](https://github.com/astral-sh/uv):

```bash
uv sync
```

### 2. Basic Conversion

Convert a Markdown file into a PDF:

```bash
uv run python scripts/md_to_pdf.py -i examples/sample_report.md -o output.pdf
```

Select a theme (e.g., `academic` or `report`):

```bash
uv run python scripts/md_to_pdf.py -i report.md -o report.pdf --theme academic
```

Generate a complete technical whitepaper with cover page, TOC, and running headers/footers:

```bash
uv run python scripts/md_to_pdf.py `
  -i technical_proposal.md `
  -o technical_proposal.pdf `
  --theme report `
  --title "2026 Technical Architecture Whitepaper" `
  --subtitle "High-Availability Service Modernization" `
  --author "haownz" `
  --cover `
  --toc
```

### 3. Stream from Standard Input

```powershell
Get-Content README.md -Raw | uv run python scripts/md_to_pdf.py -i - -o readme.pdf
```

---

## 🛠️ CLI Options Reference

| Option | Description | Default | Example |
| :--- | :--- | :--- | :--- |
| `-i`, `--input` | Input Markdown file path, or `-` for stdin | *(Required)* | `-i doc.md` |
| `-o`, `--output` | Destination PDF path | `<input_name>.pdf` | `-o dist/doc.pdf` |
| `--theme` | Visual theme (`modern`, `academic`, `report`, `minimal`, `github`) | `modern` | `--theme report` |
| `--title` | Document title (overrides frontmatter) | First H1 / stem name | `--title "User Manual"` |
| `--subtitle` | Document subtitle | None | `--subtitle "Quickstart Guide"` |
| `--author` | Document author | `Antigravity` | `--author "haownz"` |
| `--date` | Publication date | Current date | `--date "2026-10-11"` |
| `--cover` | Generate formal title page | Disabled | `--cover` |
| `--toc` | Generate Table of Contents | Disabled | `--toc` |
| `--page-size` | Page size (`A4`, `Letter`) | `A4` | `--page-size A4` |
| `--orientation`| Page orientation (`portrait`, `landscape`) | `portrait` | `--orientation landscape` |
| `--no-header-footer` | Suppress running headers and footers | Show headers/footers | `--no-header-footer` |
| `--artifact-dir` | Antigravity artifact directory for side-pane preview | None | `--artifact-dir "<path>"` |
| `--open` | Open PDF in default viewer upon completion | Disabled | `--open` |
| `--json` | Output machine-readable JSON summary | Disabled | `--json` |

---

## 📁 Repository Structure

```text
markdown-to-pdf/
├── scripts/
│   ├── md_to_pdf.py         # Core conversion engine and CLI entrypoint
│   └── browser.py           # Headless Chromium / Edge automation engine
├── templates/
│   ├── document.html        # Jinja2 template for print layout
│   ├── artifact_preview.html# Generative UI template for Antigravity viewer
│   └── styles/
│       ├── base.css         # Typography baseline, @page rules, and orphan control
│       ├── modern.css       # Clean tech theme
│       ├── academic.css     # Scholarly paper theme
│       ├── report.css       # Executive report theme
│       ├── minimal.css      # Swiss minimalist theme
│       └── github.css       # GitHub classic theme
├── examples/
│   ├── sample_report.md     # Reference document demonstrating all features
│   └── sample_output.pdf    # Compiled reference PDF output
├── tests/
│   └── test_conversion.py   # Multi-theme end-to-end automated test suite
├── pyproject.toml           # uv project configuration
├── SKILL.md                 # Antigravity Skill specification
└── README.md
```

---

## 🧪 Automated Testing

Execute the automated test suite across all 5 themes:

```bash
uv run python tests/test_conversion.py
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

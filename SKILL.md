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
   - Optimized font stacks (`Segoe UI`, `Georgia`, `Cascadia Code`, with fallbacks `PingFang SC`, `Microsoft YaHei`, `Noto Sans SC`).
   - Smart page breaks preventing orphan headings (`break-after: avoid;`).
   - Clean table layouts preventing mid-row splits across pages (`break-inside: avoid;`).
2. **Mathematical Formulas**:
   - High-fidelity vector rendering for inline (`$E = mc^2$`) and block (`$$\int_{-\infty}^\infty e^{-x^2} dx = \sqrt{\pi}$$`) formulas via KaTeX.
3. **Rich Elements**:
   - GitHub-style alert callouts (`[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, `[!CAUTION]`).
   - Syntax-highlighted code blocks via Pygments.
   - Optional Table of Contents (`--toc`) and formal Cover Page (`--cover`).
4. **Antigravity Artifact Synchronization**:
   - Generates an interactive Generative UI HTML preview (`<name>_preview.html`) and summary report (`<name>_summary.md`) directly in Antigravity's artifact directory so the user can inspect the document immediately in the side pane.
5. **Zero Heavy C-Dependencies**:
   - Natively uses local Headless Chromium (`Google Chrome` or `Microsoft Edge`) already installed on Windows. No GTK+ or Cairo DLL issues.

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
  --title "System Architecture & Engineering Specification" `
  --author "haownz" `
  --cover `
  --toc `
  --artifact-dir "<artifact_directory>"
```

### Direct Input from Stdin (Piped Content)
```powershell
$content | uv run python E:\program\markdown-to-pdf\scripts\md_to_pdf.py `
  --input "-" `
  --output "output.pdf" `
  --title "Technical Report" `
  --artifact-dir "<artifact_directory>"
```

---

## 3. Options Reference

| Option | Description | Allowed Values / Examples | Default |
| :--- | :--- | :--- | :--- |
| `-i`, `--input` | Path to input Markdown file, or `-` for stdin | `report.md` / `-` | *(Required)* |
| `-o`, `--output` | Destination path for output PDF file | `dist/output.pdf` | `<input_name>.pdf` |
| `--theme` | Visual typesetting theme | `modern`, `academic`, `report`, `minimal`, `github` | `modern` |
| `--title` | Document title (overrides frontmatter) | `--title "Technical Proposal"` | Frontmatter or first H1 |
| `--subtitle` | Document subtitle | `--subtitle "Enterprise Architecture Guide"` | None |
| `--author` | Document author | `--author "haownz"` | `Antigravity` |
| `--date` | Publication date string | `--date "2026-10-11"` | Current date |
| `--cover` | Generate formal cover page | Flag only | Disabled |
| `--toc` | Generate Table of Contents | Flag only | Disabled |
| `--page-size` | Paper size specification | `A4`, `Letter` | `A4` |
| `--orientation` | Page orientation | `portrait`, `landscape` | `portrait` |
| `--no-header-footer` | Suppress running headers and footers | Flag only | Headers/footers enabled |
| `--artifact-dir` | Antigravity artifact directory for HTML & MD preview | `<appDataDir>\brain\<id>` | None |
| `--open` | Open PDF in default viewer upon completion | Flag only | Disabled |
| `--json` | Output machine-readable JSON metadata | Flag only | Disabled |

---

## 4. Theme Styles Showcase

- **`modern`**: Clean contemporary tech theme with deep blue accents, refined borders, and modern sans-serif typography. Ideal for technical documentation and system design specs.
- **`academic`**: Formal scholarly publication aesthetic. Features serif typography (Georgia / Cambria), centered headings, classic booktabs tables, and justified paragraphs.
- **`report`**: Executive briefing theme with teal/emerald corporate accents, section accent borders, and structured card blocks.
- **`minimal`**: Monochrome Swiss minimalist style with clean lines and high contrast, focused purely on reading clarity.
- **`github`**: Classic GitHub markdown aesthetic familiar to all software engineers.

---

## 5. Artifact Sync in Antigravity Workflow

When generating PDF in an Antigravity conversation:
1. Pass `--artifact-dir "<artifact_directory>"` (e.g., `C:\Users\haowu\.gemini\antigravity\brain\<conversation-id>`).
2. The script automatically outputs:
   - `<name>_preview.html`: Interactive Generative UI card with metadata and PDF open button.
   - `<name>_summary.md`: Markdown summary artifact with file link.
3. The agent points the user to the artifact panel for instantaneous side-by-side review!

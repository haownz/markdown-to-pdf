"""Markdown to PDF Converter & Typesetting Engine with Antigravity Artifact Integration.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import frontmatter
import jinja2
import markdown
from pygments.formatters import HtmlFormatter
from pypdf import PdfReader

# Relative imports
try:
    from scripts.browser import find_browser, html_to_pdf
except ImportError:
    from browser import find_browser, html_to_pdf


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
STYLES_DIR = TEMPLATES_DIR / "styles"


def load_file_content(path: Path) -> str:
    """Load text content from a path safely."""
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def preprocess_github_alerts(text: str) -> str:
    """Convert GitHub-style alert blockquotes into styled HTML callout structures.

    Recognizes:
    > [!NOTE]
    > text
    """
    alert_types = {
        "NOTE": ("callout-note", "ℹ️", "NOTE"),
        "TIP": ("callout-tip", "💡", "TIP"),
        "IMPORTANT": ("callout-important", "📌", "IMPORTANT"),
        "WARNING": ("callout-warning", "⚠️", "WARNING"),
        "CAUTION": ("callout-caution", "🛑", "CAUTION"),
    }

    lines = text.splitlines()
    output_lines = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        match = re.match(r"^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$", line.strip(), re.IGNORECASE)
        if match:
            alert_key = match.group(1).upper()
            initial_text = match.group(2).strip()
            css_class, icon, title_label = alert_types.get(alert_key, ("callout-note", "ℹ️", alert_key))

            callout_body_lines = []
            if initial_text:
                callout_body_lines.append(initial_text)

            i += 1
            while i < n and (lines[i].startswith(">") or lines[i].strip() == ""):
                quote_line = lines[i]
                if quote_line.startswith(">"):
                    callout_body_lines.append(re.sub(r"^>\s?", "", quote_line))
                elif quote_line.strip() == "":
                    # Empty line inside blockquote
                    if i + 1 < n and lines[i + 1].startswith(">"):
                        callout_body_lines.append("")
                    else:
                        break
                i += 1

            body_content = "\n".join(callout_body_lines).strip()
            # Wrap as an HTML raw block
            callout_html = (
                f'<div class="callout {css_class}">\n'
                f'  <div class="callout-title"><span class="callout-icon">{icon}</span> {title_label}</div>\n'
                f'  <div class="callout-content">\n\n{body_content}\n\n</div>\n'
                f'</div>'
            )
            output_lines.append(callout_html)
        else:
            output_lines.append(line)
            i += 1

    return "\n".join(output_lines)


def parse_markdown(
    raw_markdown: str,
    enable_toc: bool = True,
) -> Tuple[Dict[str, Any], str, Optional[str], str]:
    """Parse Markdown frontmatter, normalize alerts, and convert to HTML.

    Returns:
        (metadata, content_html, toc_html, body_markdown)
    """
    post = frontmatter.loads(raw_markdown)
    meta = post.metadata or {}
    raw_body = post.content
    body_md = raw_body

    # If title not in meta, try to extract first H1
    if "title" not in meta:
        h1_match = re.search(r"^#\s+(.+)$", body_md, re.MULTILINE)
        if h1_match:
            meta["title"] = h1_match.group(1).strip()
        else:
            meta["title"] = "Document"

    # Preprocess callout alerts
    body_md = preprocess_github_alerts(body_md)

    # Configure Python-Markdown extensions
    extensions = [
        "extra",
        "tables",
        "footnotes",
        "attr_list",
        "def_list",
        "abbr",
        "toc",
        "pymdownx.arithmatex",
        "pymdownx.superfences",
        "pymdownx.highlight",
        "pymdownx.tasklist",
        "pymdownx.details",
    ]

    extension_configs = {
        "pymdownx.arithmatex": {
            "generic": True,
        },
        "pymdownx.highlight": {
            "use_pygments": True,
            "noclasses": False,
            "pygments_style": "default",
        },
        "pymdownx.superfences": {
            "custom_fences": [
                {
                    "name": "mermaid",
                    "class": "mermaid",
                    "format": lambda source, language, css_class, options, md, **kwargs: (
                        f'<div class="{css_class}">{source}</div>'
                    ),
                }
            ]
        },
        "pymdownx.tasklist": {
            "custom_checkbox": True,
        },
        "toc": {
            "permalink": False,
        },
    }

    md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
    content_html = md.convert(body_md)
    toc_html = md.toc if (enable_toc and getattr(md, "toc", None) and md.toc.strip() != '<div class="toc">\n<ul>\n</ul>\n</div>') else None

    return meta, content_html, toc_html, raw_body


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def convert_markdown_to_pdf(
    input_file: Optional[Path | str] = None,
    markdown_content: Optional[str] = None,
    output_pdf: Optional[Path | str] = None,
    theme: str = "modern",
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    author: Optional[str] = None,
    date: Optional[str] = None,
    page_size: str = "A4",
    orientation: str = "portrait",
    cover_page: bool = False,
    enable_toc: bool = False,
    enable_header_footer: bool = True,
    artifact_dir: Optional[Path | str] = None,
    browser_path: Optional[str] = None,
    virtual_time_budget: int = 3000,
) -> Dict[str, Any]:
    """Execute complete Markdown to PDF conversion pipeline and produce Antigravity artifacts."""
    # 1. Resolve Markdown content
    if markdown_content is None:
        if input_file is None:
            raise ValueError("Either input_file or markdown_content must be provided.")
        input_path = Path(input_file).resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"Input Markdown file not found: {input_path}")
        raw_markdown = input_path.read_text(encoding="utf-8")
        stem_name = input_path.stem
    else:
        raw_markdown = markdown_content
        stem_name = "document"

    # 2. Parse Markdown & metadata
    meta, content_html, toc_html, body_md = parse_markdown(raw_markdown, enable_toc=enable_toc)

    doc_title = title or meta.get("title", stem_name.replace("_", " ").title())
    doc_subtitle = subtitle or meta.get("subtitle", "")
    doc_author = author or meta.get("author", "Antigravity")
    doc_date = date or meta.get("date", datetime.date.today().strftime("%Y-%m-%d"))
    doc_version = meta.get("version", "")
    doc_abstract = meta.get("abstract", "")

    # Theme selection
    theme_name = theme or meta.get("theme", "modern")
    theme_css_file = STYLES_DIR / f"{theme_name}.css"
    if not theme_css_file.exists():
        theme_css_file = STYLES_DIR / "modern.css"

    base_css = load_file_content(STYLES_DIR / "base.css")
    theme_css = load_file_content(theme_css_file)
    pygments_css = HtmlFormatter(style="friendly").get_style_defs(".highlight")

    # 3. Resolve output PDF path
    if output_pdf is None:
        if input_file is not None:
            output_pdf_path = Path(input_file).resolve().with_suffix(".pdf")
        else:
            output_pdf_path = PROJECT_ROOT / f"{stem_name}.pdf"
    else:
        output_pdf_path = Path(output_pdf).resolve()

    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    # 4. Render print-optimized HTML via Jinja2
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)))
    doc_template = env.get_template("document.html")

    rendered_html = doc_template.render(
        title=doc_title,
        subtitle=doc_subtitle,
        author=doc_author,
        date=doc_date,
        version=doc_version,
        abstract=doc_abstract,
        cover_page=cover_page or meta.get("cover", False),
        toc_html=toc_html if enable_toc else None,
        content_html=content_html,
        base_css=base_css,
        theme_css=theme_css,
        pygments_css=pygments_css,
        page_size=page_size,
        orientation=orientation,
        has_header_footer=enable_header_footer,
    )

    # 5. Write temporary HTML and render to PDF
    temp_dir = Path(tempfile.gettempdir())
    temp_html_path = temp_dir / f"antigravity_doc_{os.getpid()}_{datetime.datetime.now().strftime('%H%M%S%f')}.html"
    temp_html_path.write_text(rendered_html, encoding="utf-8")

    try:
        html_to_pdf(
            html_path=temp_html_path,
            pdf_path=output_pdf_path,
            browser_path=browser_path,
            landscape=(orientation.lower() == "landscape"),
            display_header_footer=False,  # We use our precise embedded CSS headers
            virtual_time_budget=virtual_time_budget,
        )
    finally:
        if temp_html_path.exists():
            try:
                temp_html_path.unlink()
            except OSError:
                pass

    # 6. Analyze generated PDF
    reader = PdfReader(str(output_pdf_path))
    page_count = len(reader.pages)
    file_size_bytes = output_pdf_path.stat().st_size
    file_size_str = format_file_size(file_size_bytes)

    # 7. Generate Antigravity Artifacts if artifact_dir is requested
    artifact_paths: Dict[str, str] = {}
    if artifact_dir:
        art_dir = Path(artifact_dir).resolve()
        art_dir.mkdir(parents=True, exist_ok=True)

        # 7a. Interactive Generative UI HTML Artifact
        preview_template = env.get_template("artifact_preview.html")
        html_artifact_content = preview_template.render(
            title=doc_title,
            author=doc_author,
            date=doc_date,
            theme=theme_name,
            page_count=page_count,
            file_size_str=file_size_str,
            pdf_path=str(output_pdf_path),
            content_html=content_html,
            base_css=base_css,
            pygments_css=pygments_css,
        )
        html_artifact_file = art_dir / f"{stem_name}_preview.html"
        html_artifact_file.write_text(html_artifact_content, encoding="utf-8")
        artifact_paths["html_preview"] = str(html_artifact_file)

        # 7b. Markdown Summary Artifact
        md_summary_lines = [
            f"# 📄 {doc_title} (PDF Export Complete)",
            "",
            "> [!NOTE] Typesetting & Export Summary",
            f"> - **File Path**: [{output_pdf_path.name}](file:///{str(output_pdf_path).replace(chr(92), '/')})",
            f"> - **Theme**: `{theme_name}`",
            f"> - **Total Pages**: {page_count}",
            f"> - **File Size**: {file_size_str}",
            f"> - **Generated At**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"### [📄 Click to open PDF in default viewer](file:///{str(output_pdf_path).replace(chr(92), '/')})",
            "",
            "---",
            "",
            "## 📖 Document Content Preview",
            "",
            body_md,
        ]
        md_artifact_file = art_dir / f"{stem_name}_summary.md"
        md_artifact_file.write_text("\n".join(md_summary_lines), encoding="utf-8")
        artifact_paths["md_summary"] = str(md_artifact_file)

    result = {
        "status": "success",
        "title": doc_title,
        "theme": theme_name,
        "page_count": page_count,
        "file_size_bytes": file_size_bytes,
        "file_size": file_size_str,
        "pdf_path": str(output_pdf_path),
        "artifacts": artifact_paths,
    }
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Antigravity Markdown-to-PDF: Professional document typesetter with Antigravity Artifact support."
    )
    parser.add_argument("-i", "--input", help="Path to input Markdown file (or - for stdin)")
    parser.add_argument("-o", "--output", help="Path for output PDF file")
    parser.add_argument(
        "--theme",
        choices=["modern", "academic", "report", "minimal", "github"],
        default="modern",
        help="Visual layout theme (default: modern)",
    )
    parser.add_argument("--title", help="Document title (overrides frontmatter)")
    parser.add_argument("--subtitle", help="Document subtitle")
    parser.add_argument("--author", help="Author name (default: Antigravity)")
    parser.add_argument("--date", help="Document date (default: today)")
    parser.add_argument("--page-size", default="A4", help="Page size (A4, Letter; default: A4)")
    parser.add_argument(
        "--orientation",
        choices=["portrait", "landscape"],
        default="portrait",
        help="Page orientation",
    )
    parser.add_argument("--cover", action="store_true", help="Generate a formal cover page")
    parser.add_argument("--toc", action="store_true", help="Generate Table of Contents")
    parser.add_argument(
        "--no-header-footer",
        action="store_true",
        help="Disable running headers and footers",
    )
    parser.add_argument(
        "--artifact-dir",
        help="Antigravity artifact directory to sync interactive preview and markdown report",
    )
    parser.add_argument("--open", action="store_true", help="Open PDF in default viewer after generation")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()

    # Read from stdin if input is '-' or omitted without input file
    markdown_content = None
    input_file = None

    if args.input == "-" or (not args.input and not sys.stdin.isatty()):
        markdown_content = sys.stdin.read()
    elif args.input:
        input_file = Path(args.input)
    else:
        parser.print_help()
        sys.exit(1)

    try:
        result = convert_markdown_to_pdf(
            input_file=input_file,
            markdown_content=markdown_content,
            output_pdf=args.output,
            theme=args.theme,
            title=args.title,
            subtitle=args.subtitle,
            author=args.author,
            date=args.date,
            page_size=args.page_size,
            orientation=args.orientation,
            cover_page=args.cover,
            enable_toc=args.toc,
            enable_header_footer=not args.no_header_footer,
            artifact_dir=args.artifact_dir,
        )

        if args.open and sys.platform == "win32":
            os.startfile(result["pdf_path"])

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("==================================================")
            print("  ✨ Markdown-to-PDF Conversion Complete")
            print("==================================================")
            print(f"📄 Title:      {result['title']}")
            print(f"🎨 Theme:      {result['theme']}")
            print(f"📑 Pages:      {result['page_count']}")
            print(f"💾 File Size:  {result['file_size']}")
            print(f"📍 PDF Path:   {result['pdf_path']}")
            if result.get("artifacts"):
                print("🎯 Artifact Outputs:")
                for k, v in result["artifacts"].items():
                    print(f"   • {k}: {v}")
            print("==================================================")

    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

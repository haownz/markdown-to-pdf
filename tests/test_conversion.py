"""End-to-end verification test for Markdown-to-PDF conversion and Artifact generation.
"""

import sys
from pathlib import Path
from pypdf import PdfReader

# Add scripts directory to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.md_to_pdf import convert_markdown_to_pdf


def test_conversion():
    sample_md = PROJECT_ROOT / "examples" / "sample_report.md"
    output_pdf = PROJECT_ROOT / "examples" / "sample_output.pdf"
    artifact_dir = PROJECT_ROOT / "examples" / "test_artifacts"

    print(f"Testing conversion of {sample_md}...")
    result = convert_markdown_to_pdf(
        input_file=sample_md,
        output_pdf=output_pdf,
        theme="modern",
        cover_page=True,
        enable_toc=True,
        artifact_dir=artifact_dir,
    )

    print("Result summary:", result)

    # Assertions
    assert output_pdf.exists(), f"Output PDF does not exist at {output_pdf}"
    size = output_pdf.stat().st_size
    assert size > 5000, f"Output PDF size is too small ({size} bytes)"

    reader = PdfReader(str(output_pdf))
    page_count = len(reader.pages)
    assert page_count >= 1, f"Unexpected page count: {page_count}"

    assert "html_preview" in result["artifacts"], "Missing html_preview artifact"
    assert "md_summary" in result["artifacts"], "Missing md_summary artifact"
    assert Path(result["artifacts"]["html_preview"]).exists(), "html_preview file does not exist"
    assert Path(result["artifacts"]["md_summary"]).exists(), "md_summary file does not exist"

    print("==================================================")
    print(" [PASS] End-to-end conversion test succeeded!")
    print(f" - Pages: {page_count}")
    print(f" - PDF Size: {size} bytes")
    print(f" - HTML Artifact: {result['artifacts']['html_preview']}")
    print(f" - MD Artifact: {result['artifacts']['md_summary']}")
    print("==================================================")

    # Test all other themes
    for th in ["academic", "report", "minimal", "github"]:
        th_pdf = PROJECT_ROOT / "examples" / f"test_{th}.pdf"
        r = convert_markdown_to_pdf(input_file=sample_md, output_pdf=th_pdf, theme=th)
        print(f" [PASS] Theme '{th}': {r['page_count']} pages, {r['file_size']}")
        if th_pdf.exists():
            th_pdf.unlink()


if __name__ == "__main__":
    test_conversion()

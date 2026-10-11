"""Browser automation engine for rendering HTML to PDF via headless Chromium / Edge.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


def find_browser() -> Optional[str]:
    """Find an available Chromium-based browser (Chrome, Edge, Chromium, Brave) on the system."""
    # 1. Environment variable override
    env_browser = os.environ.get("ANTIGRAVITY_BROWSER_PATH") or os.environ.get("CHROME_PATH")
    if env_browser and Path(env_browser).exists():
        return env_browser

    # 2. Windows typical locations
    if sys.platform == "win32":
        candidates = [
            # Google Chrome
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            # Microsoft Edge
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
            # Brave
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
        ]
        for candidate in candidates:
            if candidate and Path(candidate).is_file():
                return candidate

        # Check PATH via where.exe
        for cmd in ["chrome", "msedge", "brave", "chromium"]:
            path = shutil.which(cmd)
            if path:
                return path

    # 3. macOS locations
    elif sys.platform == "darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
        for candidate in candidates:
            if Path(candidate).is_file():
                return candidate
        for cmd in ["google-chrome", "chromium", "microsoft-edge", "brave"]:
            path = shutil.which(cmd)
            if path:
                return path

    # 4. Linux locations
    else:
        for cmd in [
            "google-chrome",
            "google-chrome-stable",
            "chromium",
            "chromium-browser",
            "microsoft-edge",
            "brave-browser",
        ]:
            path = shutil.which(cmd)
            if path:
                return path

    return None


def html_to_pdf(
    html_path: str | Path,
    pdf_path: str | Path,
    browser_path: Optional[str] = None,
    landscape: bool = False,
    display_header_footer: bool = False,
    header_template: Optional[str] = None,
    footer_template: Optional[str] = None,
    virtual_time_budget: int = 3000,
    timeout_seconds: int = 60,
) -> bool:
    """Convert an HTML file to PDF using headless Chrome/Edge.

    Args:
        html_path: Source HTML file path.
        pdf_path: Target PDF file path.
        browser_path: Path to browser executable (auto-detected if None).
        landscape: If True, print in landscape orientation.
        display_header_footer: If True, include browser-rendered header and footer.
        header_template: HTML template for running header.
        footer_template: HTML template for running footer.
        virtual_time_budget: Milliseconds to wait for JS rendering (KaTeX, Mermaid, fonts).
        timeout_seconds: Subprocess timeout in seconds.

    Returns:
        True if PDF was successfully created.
    """
    html_file = Path(html_path).resolve()
    pdf_file = Path(pdf_path).resolve()

    if not html_file.exists():
        raise FileNotFoundError(f"Source HTML file does not exist: {html_file}")

    browser = browser_path or find_browser()
    if not browser:
        raise RuntimeError(
            "Could not locate a Chromium-based browser (Google Chrome, Microsoft Edge, Brave). "
            "Please install Chrome or Edge, or set the CHROME_PATH environment variable."
        )

    # Ensure parent output directory exists
    pdf_file.parent.mkdir(parents=True, exist_ok=True)

    # Convert path to file URL
    file_url = html_file.as_uri()

    args = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--run-all-compositor-stages-before-draw",
        f"--virtual-time-budget={virtual_time_budget}",
        f"--print-to-pdf={pdf_file}",
    ]

    if landscape:
        args.append("--landscape")

    if display_header_footer:
        args.append("--display-header-footer")
        if header_template:
            args.append(f"--header-template={header_template}")
        else:
            args.append(
                '--header-template=<div style="font-size:8pt;color:#888;width:100%;text-align:right;padding-right:15mm;"><span class="title"></span></div>'
            )

        if footer_template:
            args.append(f"--footer-template={footer_template}")
        else:
            args.append(
                '--footer-template=<div style="font-size:8pt;color:#888;width:100%;display:flex;justify-content:space-between;padding:0 15mm;"><span>Document</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>'
            )
    else:
        args.append("--no-pdf-header-footer")

    # Add the input URL
    args.append(file_url)

    # Execute browser print
    proc = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )

    if not pdf_file.exists() or pdf_file.stat().st_size == 0:
        err_msg = (
            f"Failed to generate PDF at {pdf_file}.\n"
            f"Command: {' '.join(args)}\n"
            f"Exit Code: {proc.returncode}\n"
            f"Stderr: {proc.stderr}\n"
            f"Stdout: {proc.stdout}"
        )
        raise RuntimeError(err_msg)

    return True

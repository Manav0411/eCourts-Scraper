# eCourts_Scraper

This Python script downloads the daily cause list webpage from the Indian eCourts services site and saves it as a PDF.

## What it does

`main.py` fetches the cause list page and converts it to a PDF. By default it uses `pdfkit` (wkhtmltopdf). If that fails, it can fall back to a headless browser (Playwright) to render JavaScript-heavy pages.

## Prerequisites

- Python 3.7+
- pip
- wkhtmltopdf installed and accessible on your PATH, or note its installation path to configure in `main.py`.
 - wkhtmltopdf installed and accessible on your PATH (for `pdfkit`) or Playwright installed (optional) for the fallback.

Download wkhtmltopdf for Windows from: https://wkhtmltopdf.org/downloads.html

## Setup

1. Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. If wkhtmltopdf is installed in a non-standard location, the script will try to detect it. You can also use the Playwright fallback (optional).


# eCourts_Scraper

A tiny utility to download the daily cause list from the Indian eCourts services site and save it as a PDF.

This repository contains a single-purpose script, `main.py`, that produces a PDF of the cause list using either:

- pdfkit (wkhtmltopdf) for fast HTML-to-PDF conversion, or
- Playwright (headless browser) as a fallback when JavaScript rendering is required.

## Quick summary

- Input: a cause list URL (default: the ecourts cause list index URL)
- Output: a PDF file saved to `data/` (default name: `cause_list_<YYYY-MM-DD>.pdf`)
- Primary renderers: `wkhtmltopdf` (via `pdfkit`) and Playwright as a fallback

## Requirements

- Python 3.7+
- pip
- One of:
  - wkhtmltopdf installed and available on PATH (used by `pdfkit`), or
  - Playwright installed (optional) for the fallback

Download wkhtmltopdf for Windows: https://wkhtmltopdf.org/downloads.html

## Installation

1. (Recommended) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install required packages:

```powershell
pip install -r requirements.txt
```

3. (Optional) Install Playwright and its browsers if you plan to use the fallback:

```powershell
pip install -r requirements-optional.txt
python -m playwright install
```

## Usage

Run with defaults (writes to `data/cause_list_<date>.pdf`):

```powershell
python main.py
```

Specify a URL or output file:

```powershell
python main.py --url "https://services.ecourts.gov.in/ecourtindia_v6/?p=caselist/index/"
python main.py --out data/my_cause_list.pdf
```

Example successful output:

```
Saved PDF to: data\cause_list_2025-10-15.pdf
```

## Configuration & tips

- The script attempts to detect common Windows locations for `wkhtmltopdf`. If yours is installed elsewhere, add it to PATH or update `find_wkhtmltopdf_config()` in `main.py`.
- If the site returns a non-200 response or `wkhtmltopdf` cannot render the dynamic page, the script will try the Playwright fallback (requires optional deps and browsers).
- If you hit rendering issues with `wkhtmltopdf`, consider increasing `javascript-delay` in `download_with_pdfkit()`.

## File structure

```
ecourts_scraper/
├─ .gitignore
├─ LICENSE
├─ main.py                # scraper/renderer script
├─ README.md
├─ requirements.txt       # required Python packages
├─ requirements-optional.txt  # optional packages (Playwright)
└─ data/
   ├─ .gitkeep
   └─ cause_list_2025-10-15.pdf
```

## Troubleshooting

- Network errors: verify connectivity and whether the site is blocking automated requests.
- Missing Playwright: install optional deps and run `python -m playwright install`.
- wkhtmltopdf errors: confirm wkhtmltopdf is installed and on PATH, or use Playwright for rendering.

## License

See the `LICENSE` file in the repository.

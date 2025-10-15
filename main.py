import argparse
import logging
import os
from datetime import date

import pdfkit
import requests


def download_with_pdfkit(html: str, out_path: str, wk_config=None) -> None:
    options = {
        'enable-local-file-access': None,
        'no-stop-slow-scripts': None,
        'javascript-delay': '2000',
        'load-error-handling': 'ignore',
    }
    if wk_config:
        pdfkit.from_string(html, out_path, configuration=wk_config, options=options)
    else:
        pdfkit.from_string(html, out_path, options=options)


def download_with_playwright(url: str, out_path: str) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        raise RuntimeError("Playwright is not installed. Install with: pip install playwright") from e

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        })
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(1500)
        page.pdf(path=out_path, format='A4')
        browser.close()


def find_wkhtmltopdf_config():
    candidates = [
        r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
        r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
    ]
    for p in candidates:
        if os.path.isfile(p):
            return pdfkit.configuration(wkhtmltopdf=p)
    try:
        return pdfkit.configuration()
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description='Download ecourts cause list as PDF')
    parser.add_argument('--url', default='https://services.ecourts.gov.in/ecourtindia_v6/?p=caselist/index/',
                        help='Cause list URL')
    parser.add_argument('--out', default=None, help='Output PDF path')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(message)s')
    url = args.url

    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)

    if args.out:
        out_path = args.out
    else:
        today = date.today().isoformat()
        out_path = os.path.join(data_dir, f'cause_list_{today}.pdf')

    logging.info('Fetching page...')
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://services.ecourts.gov.in/',
    })

    # Prime the site (some servers expect an initial root request)
    try:
        session.get('https://services.ecourts.gov.in/', timeout=10)
    except Exception:
        pass

    resp = session.get(url, timeout=20)
    if resp.status_code != 200:
        logging.warning('Primary fetch returned HTTP %s; will try Playwright fallback', resp.status_code)
        # Try Playwright fallback
        try:
            download_with_playwright(url, out_path)
            logging.info('Saved PDF via Playwright to: %s', out_path)
            return
        except Exception as e:
            logging.error('Playwright fallback failed: %s', e)
            raise SystemExit(1)

    html = resp.text
    wk_cfg = find_wkhtmltopdf_config()
    try:
        download_with_pdfkit(html, out_path, wk_cfg)
        logging.info('Saved PDF to: %s', out_path)
    except Exception as e:
        logging.warning('pdfkit failed: %s; trying Playwright...', e)
        download_with_playwright(url, out_path)
        logging.info('Saved PDF via Playwright to: %s', out_path)


if __name__ == '__main__':
    main()

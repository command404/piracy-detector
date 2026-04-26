from crawler.fetcher import fetch
from crawler.parser import extract_text
from crawler.deep_scanner import deep_scan
from detector.ai_classifier import classify_website

def run(urls):
    results = []

    for url in urls:
        html = fetch(url)
        if not html:
            continue

        text = extract_text(html)
        findings = deep_scan(html, url)

        ai_result = classify_website(text, findings)

        results.append({
            "url": url,
            "findings": findings,
            "ai": ai_result
        })

    return results
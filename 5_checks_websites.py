from crawler.fetcher import fetch
from crawler.parser import extract_text
from crawler.deep_scanner import deep_scan
from detector.ai_classifier import classify_website
import time

def run(urls):
    results = []
    MAX_WEBSITES = 5  # Limit to 5 websites only

    for url in urls[:MAX_WEBSITES]:
        print(f"Scanning: {url}")

        html = fetch(url)
        if not html:
            print("Failed to fetch")
            continue

        text = extract_text(html)
        findings = deep_scan(html, url)

        try:
            ai_result = classify_website(text, findings)
            time.sleep(12)  # Stay under free-tier rate limit

        except Exception as e:
            ai_result = f"Error: {e}"

        results.append({
            "url": url,
            "findings": findings,
            "ai": ai_result
        })

    return results


if __name__ == "__main__":
    urls = []

    with open("data/seed_urls.txt") as f:
        for i, line in enumerate(f):
            line = line.strip()

            if not line:
                continue

            if i == 0:  # Skip header
                continue

            url = line.split(",")[0].strip()
            urls.append(url)

    output = run(urls)

    for result in output:
        print(result)
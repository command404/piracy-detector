from crawler.fetcher import fetch
from crawler.parser import extract_text
from crawler.deep_scanner import deep_scan
import time


def run(urls):
    flagged_sites = []
    MAX_WEBSITES = 5
    checked = 0

    # Bottom URLs first
    for url in reversed(urls):

        if checked >= MAX_WEBSITES:
            break

        html = fetch(url)
        if not html:
            continue

        text = extract_text(html)
        findings = deep_scan(html, url)

        # Rule-based suspicious detection first
        if findings["suspicious_keywords"] or findings["video_links"]:
            flagged_sites.append({
                "url": url,
                "reason": "Suspicious keywords or media/download links detected"
            })

        checked += 1

        # Delay between sites
        time.sleep(65)

    return flagged_sites


if __name__ == "__main__":
    urls = []

    with open("data/seed_urls.txt") as f:
        for i, line in enumerate(f):
            line = line.strip()

            if not line:
                continue

            if i == 0:
                continue

            url = line.split(",")[0].strip()
            urls.append(url)

    flagged_results = run(urls)

    print("\n--- FLAGGED WEBSITES ---\n")

    if not flagged_results:
        print("No suspicious websites detected.")

    else:
        for site in flagged_results:
            print(f"FLAGGED URL: {site['url']}")
            print(f"Reason: {site['reason']}")
            print("-" * 50)
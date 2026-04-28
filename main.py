from crawler.fetcher import fetch
from crawler.parser import extract_text
from crawler.deep_scanner import deep_scan
import time


def run(urls):
    flagged_sites = []

    # First 3 safe websites from top
    safe_urls = urls[:3]

    # Last 3 pirated websites from bottom
    pirated_urls = urls[-3:]

    # Combine them
    mixed_urls = safe_urls + pirated_urls

    for url in mixed_urls:

        html = fetch(url)
        if not html:
            continue

        text = extract_text(html)
        findings = deep_scan(html, url)

        # Safe or Pirated verdict
        if findings["suspicious_keywords"] or findings["video_links"]:

            piracy_reason = []

            if findings["video_links"]:
                piracy_reason.append("unauthorized streaming/download links")
                
            if findings["suspicious_keywords"]:
                piracy_reason.append("piracy-related keywords")


            verdict = "This website contains pirated content."
            reason = f"Detected {' and '.join(piracy_reason)}."

        else:
            verdict = "This website appears safe."
            reason = "No piracy indicators detected."

        flagged_sites.append({
            "url": url,
            "verdict": verdict,
            "reason": reason
        })

        # Delay between websites
        time.sleep(1)

    return flagged_sites


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

    results = run(urls)

    print("\n--- WEBSITE ANALYSIS RESULTS ---\n")

    for i, site in enumerate(results, start=1):
        print(f"Website {i}:")
        print(f"URL: {site['url']}")
        print(f"VERDICT: {site['verdict']}")
        print(f"REASON: {site['reason']}")
        print("-" * 60)
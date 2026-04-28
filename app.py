from flask import Flask, render_template, request
from main import run
from crawler.fetcher import fetch
from crawler.parser import extract_text
from crawler.deep_scanner import deep_scan

# Global memory for all scanned URLs
all_results = []

app = Flask(__name__)


@app.route("/")
def dashboard():
    print("Dashboard route triggered")

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

    # Use persistent dashboard memory
    global all_results

    # Only auto-scan once
    if not all_results:
        all_results = run(urls)

    total_scanned = len(all_results)

    flagged_count = len([
        site for site in all_results
        if "pirated" in site["verdict"].lower()
    ])

    safe_count = total_scanned - flagged_count

    return render_template(
        "index.html",
        results=all_results,
        total_scanned=total_scanned,
        flagged_count=flagged_count,
        safe_count=safe_count
    )


@app.route("/scan", methods=["POST"])
def scan_custom_url():

    custom_url = request.form.get("custom_url")

    global all_results

    # Prevent duplicate scans
    existing_urls = [site["url"] for site in all_results]

    if custom_url not in existing_urls:

        # Now scan custom URL separately
        html = fetch(custom_url)

        if html:

            text = extract_text(html)
            findings = deep_scan(html, custom_url)

            if findings["suspicious_keywords"] or findings["video_links"]:
                verdict = "This website contains pirated content."
                reason = "Detected piracy-related keywords or unauthorized streaming/download links."

            else:
                verdict = "This website appears safe."
                reason = "No piracy indicators detected."

            # Add custom result to dashboard memory
            all_results.insert(0, {
                "url": custom_url,
                "verdict": verdict,
                "reason": reason
            })

    total_scanned = len(all_results)

    flagged_count = len([
        site for site in all_results
        if "pirated" in site["verdict"].lower()
    ])

    safe_count = total_scanned - flagged_count

    return render_template(
        "index.html",
        results=all_results,
        total_scanned=total_scanned,
        flagged_count=flagged_count,
        safe_count=safe_count
    )


if __name__ == "__main__":
    app.run(debug=True)

app = app
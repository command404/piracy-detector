from flask import Flask, render_template
from main import run

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

    # Use backend
    results = run(urls)

    total_scanned = len(results)

    flagged_count = len([
        site for site in results
        if "pirated" in site["verdict"].lower()
    ])

    safe_count = total_scanned - flagged_count

    return render_template(
        "index.html",
        results=results,
        total_scanned=total_scanned,
        flagged_count=flagged_count,
        safe_count=safe_count
    )


if __name__ == "__main__":
    app.run(debug=True)
from crawler.fetcher import fetch
from crawler.parser import extract_text
from detector.rules import rule_based_detection
from detector.ai_classifier import classify
import json

def run(urls):
    results = []

    for url in urls:
        print(f"\nProcessing: {url}")

        html = fetch(url)
        if not html:
            print("Failed to fetch")
            continue

        text = extract_text(html)

        # Step 1: Rule-based detection
        rule_result = rule_based_detection(text)

        # Step 2: AI classification (Gemini 2.5 Flash)
        try:
            ai_result = classify(text)
        except Exception as e:
            ai_result = f"Error: {e}"

        result = {
            "url": url,
            "rule": rule_result,
            "ai": ai_result
        }

        print(result)
        results.append(result)

    return results


if __name__ == "__main__":
    # Load URLs
    urls = []

    with open("data/seed_urls.txt") as f:
        for i, line in enumerate(f):
            line = line.strip()

            if not line:
                continue

            if i == 0:  # skip header
                continue

            parts = line.split(",")

            if len(parts) >= 1:
                url = parts[0].strip()
                urls.append(url)

    # Run pipeline
    output = run(urls)

    # Save results to file (VERY useful for hackathon demo)
    with open("data/results.json", "w") as f:
        json.dump(output, f, indent=4)

    print("\n✅ Results saved to data/results.json")
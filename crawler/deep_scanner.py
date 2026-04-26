from bs4 import BeautifulSoup
from urllib.parse import urljoin

def deep_scan(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    findings = {
        "links": [],
        "video_links": [],
        "images": [],
        "suspicious_keywords": []
    }

    piracy_keywords = [
        "free download", "watch free", "torrent", "1080p",
        "hd download", "no signup", "stream free", "full movie"
    ]

    # Scan page text
    page_text = soup.get_text(" ").lower()

    for keyword in piracy_keywords:
        if keyword in page_text:
            findings["suspicious_keywords"].append(keyword)

    # Scan links
    for tag in soup.find_all("a", href=True):
        link = urljoin(base_url, tag["href"])
        findings["links"].append(link)

        if any(x in link.lower() for x in ["torrent", "download", ".mp4", ".mkv", "magnet:"]):
            findings["video_links"].append(link)

    # Scan images
    for img in soup.find_all("img", src=True):
        findings["images"].append(urljoin(base_url, img["src"]))

    return findings
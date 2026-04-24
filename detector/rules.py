def rule_based_detection(text):
    keywords = ["free download", "watch free", "torrent", "HD movies"]

    for word in keywords:
        if word in text.lower():
            return "Suspicious"

    return "Safe"
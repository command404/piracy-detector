from google import genai
import os
from dotenv import load_dotenv
load_dotenv(override=True)
client = genai.Client(api_key=os.getenv("AIzaSyDwaHPgvCapNxaEcp_lHNgFSCp1mNgVxLo"))

def classify_website(page_text, findings):
    prompt = f"""
You are analyzing a website for piracy risk.

Website text:
{page_text[:3000]}

Detected suspicious keywords:
{findings['suspicious_keywords']}

Detected suspicious media/download links:
{findings['video_links'][:20]}

Classify as:
- Pirated
- Suspicious
- Safe

Also provide:
- Confidence (0-100)
- Reason

Format:
Label:
Confidence:
Reason:
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text.strip()
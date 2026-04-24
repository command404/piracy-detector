from google import genai

# Initialize client once
client = genai.Client(api_key="")

def classify(text):
    prompt = f"""
You are an AI that classifies websites into one of three categories:
- Pirated
- Suspicious
- Safe

Rules:
- Pirated: illegal streaming, torrents, free premium content
- Suspicious: unclear legality, misleading download/stream claims
- Safe: legitimate websites

ONLY return one word: Pirated, Suspicious, or Safe.

Website content:
{text[:1500]}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()
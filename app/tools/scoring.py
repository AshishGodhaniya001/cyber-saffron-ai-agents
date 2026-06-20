import json
import asyncio
import re
import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel(settings.gemini_model)

async def score_lead(raw_data_json: str) -> int:
    try:
        data = json.loads(raw_data_json)
    except:
        data = {"text": raw_data_json}
    prompt = f"Score the following business lead from 0 to 100 based on likelihood to need digital services (websites, AI, marketing, SEO, cybersecurity). Return ONLY an integer score between 0 and 100. Lead info: {json.dumps(data)}"
    response = await asyncio.to_thread(model.generate_content, prompt)
    text = response.text.strip()
    match = re.search(r'\b([0-9]{1,3})\b', text)
    if match:
        score = int(match.group(1))
    else:
        score = 0
    return min(100, max(0, score))
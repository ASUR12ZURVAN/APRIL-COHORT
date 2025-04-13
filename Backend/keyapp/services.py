import json
import requests
from django.conf import settings

def extract_keywords(transcript_data):
    endpoint = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Extract 10-15 important keywords from this JSON transcript.
    Return ONLY a JSON array of keywords, nothing else.
    
    Transcript:
    {json.dumps(transcript_data)}
    """
    
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        return json.loads(response.json()['choices'][0]['message']['content'])
    except Exception as e:
        print(f"API Error: {str(e)}")
        return []
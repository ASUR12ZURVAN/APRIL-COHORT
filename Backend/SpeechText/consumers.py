import json
import json
import re
import aiohttp
from statistics import mean
from channels.generic.websocket import AsyncWebsocketConsumer

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HUGGINGFACE_API_TOKEN = "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"  # Replace with your token

class SentimentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected to Sentiment WebSocket"}))

    async def disconnect(self, close_code):
        print(f"Disconnected: {close_code}")

    async def analyze_sentiment(self, text):
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                HUGGINGFACE_API_URL,
                headers=headers,
                json={"inputs": text}
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result[0]  # Expecting single sentence result
                else:
                    error_text = await resp.text()
                    raise Exception(f"API error {resp.status}: {error_text}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        transcript_text = data.get("transcript", "")
        if transcript_text:
            print("Transcript received in the consumer.py")

        turns = re.split(r'(?<=[.?!])\s+', transcript_text.strip())
        caller_turns = turns[::2]

        scores = []
        sentiment_results = []

        for turn in caller_turns:
            try:
                result = await self.analyze_sentiment(turn)
                sentiment = result["label"]
                score = result["score"]
                signed_score = score if sentiment == "POSITIVE" else -score
                scores.append(signed_score)

                sentiment_results.append({
                    "turn": turn,
                    "sentiment": sentiment,
                    "score": round(score, 2)
                })
            except Exception as e:
                sentiment_results.append({
                    "turn": turn,
                    "sentiment": "ERROR",
                    "score": 0.0,
                    "error": str(e)
                })

        avg_score = mean(scores) if scores else 0.0

        await self.send(text_data=json.dumps({
            "caller_sentiments": sentiment_results,
            "avg_sentiment": round(avg_score, 2)
        }))

import json
import re
from statistics import mean
from channels.generic.websocket import AsyncWebsocketConsumer
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification


# Load model once globally
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

class SentimentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected to Sentiment WebSocket"}))

    async def disconnect(self, close_code):
        print(f"Disconnected: {close_code}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        transcript_text = data.get("transcript", "")
        if(transcript_text):
            print("Transcript received in the consumer.py")

        turns = re.split(r'(?<=[.?!])\s+', transcript_text.strip())
        caller_turns = turns[::2]

        scores = []
        sentiment_results = []

        for i, turn in enumerate(caller_turns):
            result = sentiment_pipeline(turn)[0]
            sentiment = result["label"]
            score = result["score"]
            signed_score = score if sentiment == "POSITIVE" else -score
            scores.append(signed_score)

            sentiment_results.append({
                "turn": turn,
                "sentiment": sentiment,
                "score": round(score, 2)
            })
        
        avg_score = mean(scores)

        await self.send(text_data=json.dumps({
            "caller_sentiments": sentiment_results,
            "avg_sentiment": round(avg_score, 2)
        }))
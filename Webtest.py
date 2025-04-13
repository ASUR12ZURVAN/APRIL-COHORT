import asyncio
import websockets
import json

async def test_sentiment_ws():
    uri = "ws://localhost:8000/ws/sentiment/"  # Make sure your server is running

    async with websockets.connect(uri) as websocket:
        # Send transcript data
        transcript = """My boss yelled on me. 
        Im really angry rn.
        But atleast i learnt something new """
        await websocket.send(json.dumps({
            "transcript": transcript
        }))
        print("📤 Sent transcript.")

        # Receive the sentiment results
        response = await websocket.recv()
        print("Raw response:", response)

        response = await websocket.recv()
        print("Raw response:", response)

        data = json.loads(response)
        print("📥 Received Sentiment Analysis:\n")

        if 'caller_sentiments' in data:
            for idx, item in enumerate(data['caller_sentiments']):
                print(f"Caller Turn {idx + 1}: {item['turn']}")
                print(f"  ➤ Sentiment: {item['sentiment']} (Score: {item['score']})\n")

            print(f"📊 Average Sentiment Score: {data['avg_sentiment']}")
        else:
            print("⚠️ Server response did not contain expected data.")
            print(data)

# Run the test
asyncio.run(test_sentiment_ws())

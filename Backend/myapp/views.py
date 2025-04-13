from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
import requests

@api_view(["POST"])
def chatgroq_response(request):
    """
    Handle customer support tickets by providing AI-generated solutions.
    Expects JSON with {'ticket': 'ticket content'} in the request body.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    try:
        # Parse request data
        try:
            body = json.loads(request.body)
            ticket = body.get("ticket", "").strip()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        if not ticket:
            return JsonResponse({"error": "Ticket content cannot be empty"}, status=400)

        # API configuration
        API_KEY = "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"
        API_BASE = "https://api.groq.com/openai/v1/chat/completions"
        MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

        # Prepare the request
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert customer support agent. For each ticket:
1. First identify if this is a technical, account, billing, or general inquiry
2. Provide a concise problem summary (1-2 sentences)
3. Give step-by-step solution (bullet points)
4. Offer preventive measures (if applicable)
5. Include any relevant warnings/caveats

Format with clear Markdown headings."""
                },
                {"role": "user", "content": f"Support ticket: {ticket}"}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }

        # Make the API request with timeout
        try:
            response = requests.post(
                API_BASE,
                headers=headers,
                json=payload,
                timeout=10  # 10 seconds timeout
            )
            response.raise_for_status()  # Raises exception for 4XX/5XX responses
        except requests.Timeout:
            return JsonResponse({"error": "API request timed out"}, status=504)
        except requests.RequestException as e:
            return JsonResponse({
                "error": f"API request failed",
                "details": str(e)
            }, status=502)

        # Process successful response
        result = response.json()
        solution = result['choices'][0]['message']['content'].strip()
        
        # Return structured response
        return JsonResponse({
            "status": "success",
            "solution": solution,
            "model": MODEL,
            "tokens_used": result.get('usage', {}).get('total_tokens', 0)
        })

    except Exception as e:
        # Log the error here (you should implement proper logging)
        return JsonResponse({
            "error": "Internal server error",
            "message": str(e)
        }, status=500)
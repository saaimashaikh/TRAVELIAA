import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
GROQ_KEY = os.getenv("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")

@app.route("https://travelia-backend.onrender.com/generate", methods=["POST"])
def generate():
    data = request.json

    prompt = f"""
    Create a travel itinerary to {data['to']} from {data['from']}.
    Budget: {data['budget']}.
    Interests: {data['interests']}.
    Output ONLY valid JSON in this structure:
    {{ "title": "Trip Title", "total": "Estimated Cost",
      "days": [{{"day": 1, "morning": "...", "afternoon": "...",
      "evening": "...", "cost": "..."}}] }}
    """

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You strictly output JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
    )

    result = response.json()

    return jsonify(
        json.loads(result["choices"][0]["message"]["content"])
    )

if __name__ == "__main__":
    app.run(debug=True)


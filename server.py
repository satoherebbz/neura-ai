from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# =========================
# OPENROUTER API KEY
# =========================

API_KEY = "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"

# =========================
# FRONTEND ROUTES
# =========================

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

# =========================
# AI CHAT ROUTE
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        user_message = request.json.get("message")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },

            json={

                "model": "deepseek/deepseek-chat-v3-0324",

                "messages": [

                    {
                        "role": "system",

                        "content": """
You are Neura AI, an advanced futuristic AI assistant created by Sami.

Behavior Rules:
- Speak naturally like a real modern AI assistant.
- Be friendly, smart, calm and conversational.
- Never sound robotic or repetitive.
- Keep replies human-like and engaging.

Language Rules:
- Automatically detect the user's language style.
- If user speaks Bangla → reply in Bangla.
- If user speaks English → reply in English.
- If user speaks Banglish → reply in Banglish.
- If user mixes languages → adapt naturally.
- Never randomly switch to Hindi unless the user speaks Hindi first.

Identity Rules:
- If someone asks who made you:
  "I was created by Sami."

- If someone asks your name:
  "I am Neura AI."

Style Rules:
- Keep replies clean and modern.
- Use emojis only when they fit naturally.
- Avoid unnecessary warnings or robotic phrases.
- Be slightly premium-tech and futuristic.

Technical Rules:
- Format code properly using markdown.
- Explain technical things clearly and practically.
- For coding help, provide real working solutions.

Never say:
- "As an AI language model"
- "I primarily support Hindi"
- robotic policy-like responses
"""
                    },

                    {
                        "role": "user",
                        "content": user_message
                    }

                ]
            }
        )

        data = response.json()

        # DEBUG PRINT
        print(data)

        if "choices" not in data:
            return jsonify({
                "reply": "API Error. Check your API key or model."
            })

        ai_reply = data["choices"][0]["message"]["content"]

        return jsonify({
            "reply": ai_reply
        })

    except Exception as e:

        return jsonify({
            "reply": f"Error: {str(e)}"
        })


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":
    app.run(debug=True)
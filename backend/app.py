# Basic Flask server to handle chatbot messages

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

# Get full path to .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_key = os.getenv("OPENROUTER_API_KEY")
print("LOADED API KEY:", api_key)

HF_API_URL = "https://openrouter.ai/api/v1/chat/completions"



# Add your free token here (or skip if using public model)
HF_HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Human-written comment:
# Sends user's message to OpenRouter (Kimi-K2-Instruct) and returns reply

def get_llm_reply(prompt):
    payload = {
        "model": "moonshotai/kimi-k2",  # OpenRouter uses aliases; Kimi-K2 is auto-routed
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that understands user taste and preferences."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        print(response.status_code)
        print(response.text)
        return "I'm sorry, I couldn't generate a reply right now."



app = Flask(__name__)
CORS(app)  # Allow frontend JS to call this backend

# Route to handle chat messages
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Placeholder response
    bot_reply = get_llm_reply(user_message)

    return jsonify({"reply": bot_reply})


# Run the app
if __name__ == "__main__":
    app.run(debug=True)

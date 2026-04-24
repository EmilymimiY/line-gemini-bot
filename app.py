from flask import Flask, request
import requests
import os

app = Flask(__name__)

LINE_TOKEN = os.getenv("LINE_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/webhook", methods=['POST'])
def webhook():
    body = request.json

    for event in body.get("events", []):
        if event["type"] == "message":
            user_msg = event["message"]["text"]
            reply_token = event["replyToken"]

            ai_reply = ask_gemini(user_msg)
            reply_line(reply_token, ai_reply)

    return "OK"

def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    data = {
        "contents": [{"parts":[{"text": text}]}]
    }

    res = requests.post(url, json=data)
    result = res.json()

    print("Gemini response:", result)  # 👈 方便你看 log

    try:
        return result['candidates'][0]['content']['parts'][0]['text']
    except:
        return "AI目前有點忙，請稍後再試 🙏"

def reply_line(token, text):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "replyToken": token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, headers=headers, json=data)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

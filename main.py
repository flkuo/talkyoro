from flask import Flask, request
from linebot.v3.messaging import MessagingApi, ReplyMessageRequest
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.models import TextMessage, MessageEvent

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


# Get credentials from environment variables
ACCESS_TOKEN = "NvXHSPCDi6py44u4NgrWgahVHfxAjX9dLG4JZtNTfLXEA1LtwhEF4kOQ3F1zhGMrcK7jBU+UqmKIteFcpswRsOfSCHyVYiCTVFGBy2dGsx5GbmPjQ8OzMOXZ+zmOEVpCuoWGAOJZLHNahnhvzlSucwdB04t89/1O/w1cDnyilFU="
SECRET = "c749fff4b2508936fee2d32212ce3b7e"

app = Flask(__name__)

# LINE API v3
line_bot_api = MessagingApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid Signature", 400

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text  # Get user message
    reply_text

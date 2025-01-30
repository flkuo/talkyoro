from flask import Flask, request
from linebot.v3.messaging import MessagingApi, ApiClient
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhook.models import MessageEvent, TextMessageContent

app = Flask(__name__)

# LINE Bot credentials
LINE_ACCESS_TOKEN = "NvXHSPCDi6py44u4NgrWgahVHfxAjX9dLG4JZtNTfLXEA1LtwhEF4kOQ3F1zhGMrcK7jBU+UqmKIteFcpswRsOfSCHyVYiCTVFGBy2dGsx5GbmPjQ8OzMOXZ+zmOEVpCuoWGAOJZLHNahnhvzlSucwdB04t89/1O/w1cDnyilFU="  # Replace with your Channel Access Token
LINE_CHANNEL_SECRET = "c749fff4b2508936fee2d32212ce3b7e"      # Replace with your Channel Secret

# Initialize Messaging API and Webhook Handler
api_client = ApiClient()
line_bot_api = MessagingApi(api_client=api_client, channel_access_token=LINE_ACCESS_TOKEN)
handler = WebhookHandler(channel_secret=LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"Error: {e}")
        return "Error", 400

    return "OK", 200

@handler.add(MessageEvent)
def handle_message(event):
    if isinstance(event.message, TextMessageContent):
        user_message = event.message.text  # User's message
        reply_token = event.reply_token

        # Respond to the user
        if user_message.lower() in ["hi", "hello"]:
            reply_text = "Hello! How can I assist you?"
        else:
            reply_text = "Sorry, I didn't understand that."

        line_bot_api.reply_message(reply_token, [{"type": "text", "text": reply_text}])

if __name__ == "__main__":
    app.run(port=5000)

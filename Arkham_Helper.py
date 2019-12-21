import configparser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("config.ini")
line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
commands = ["功能", "功能解說", "加入遊戲", "創建角色", "查詢角色", "更新角色", "紀錄冒險", "查詢冒險"]


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))"""

    if event.message.text == "功能":
        info = "\n".join(commands)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=info))

    if event.message.text == "功能解說":
        with open("help.txt", "r", encoding='Big5', errors='ignore') as f:
            helper = f.read()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=helper))

    if event.message.text == "加入遊戲":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))





if __name__ == "__main__":
    app.run()
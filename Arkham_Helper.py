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
str = "初次使用請先輸入:加入遊戲創建角色請依照以下規格輸入:/創建角色,玩家名稱,角色名稱,經驗值,肉體創傷/精神創傷,永久卡片更新角色請依照以下規格輸入(括弧內只需輸入須更新之內容即可):/更新角色,(經驗值:,肉體創傷/精神創傷:,永久卡片:)例:/更新角色,經驗值:5"


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
    if event.message.text == "指令":
        info = "\n".join(commands)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=info))

    if event.message.text == "功能解說":
        with open("help.txt", "r", encoding='utf-8', errors='ignore') as f:
            helper = f.read()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=""))

    if event.message.text == "加入遊戲":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))





if __name__ == "__main__":
    app.run()
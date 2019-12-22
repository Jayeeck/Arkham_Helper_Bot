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

from AdventureHandler import AdventureHandler
from CharacterHandler import CharacterHandler

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("config.ini")
clientToken = config['mongo_db']['Client_Access_Token']
line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
commands = ["指令", "功能解說", "創建角色", "查詢角色", "更新角色", "紀錄冒險", "冒險日誌"]
cHandler = CharacterHandler(clientToken)
aHandler = AdventureHandler(clientToken)


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
    message = event.message.text.split("，")
    head = message[0]
    del message[0]
    if head == "指令":
        info = "\n".join(commands)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=info))

    if head == "功能解說":
        with open("help.txt", "r", encoding='Big5', errors='ignore') as f:
            helper = f.read()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=helper))

    if head == "創建角色":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=cHandler.createCharacter(event.source.user_id, message)))

    if head == "查詢角色":
        result = cHandler.searchCharacters(event.source.user_id)
        if type(result) == list:
            if len(result) > 0:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="\n\n".join(result)))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="該玩家尚未創建角色"))
        elif type(result) == str:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))

    if head == "更新角色":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=cHandler.updateCharacter(event.source.user_id, message)))

    if head == "紀錄冒險":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=aHandler.newLog(event.source.user_id, message)))

    if head == "冒險日誌":
        result = aHandler.showLogs(event.source.user_id)
        if type(result) == list:
            if len(result) > 0:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="\n\n".join(result)))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="沒有冒險紀錄!"))
        elif type(result) == str:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))


if __name__ == "__main__":
    app.run()

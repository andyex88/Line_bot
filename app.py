from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('HoJ0nQHtY8OVpkdKFbSG/b2xfbGJIzNO+rPEEYdG7r3d5LKI2eHNHlW/iOAva9GwfDZjVAE+EvzdFGoWtJOBwUmxHkAJKKONcl63yuyfCPvdyM1SLPjeDJT6iZPkqKdQb4ErmTglRXU1a89/GTfr9gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b47911335ec1c42c12b43bfcd84201fd')


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
    msg = event.message.text
    r = "Hi, There!\nPlease enter specific words\n1. Sticker\n2. Have you eaten?\n3. How are you?\n4. Who are you?"

    if msg in ['Sticker', 'sticker']:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1')

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)

        return

    elif msg in ['Have you eaten?', 'have you eaten?']:
        r = "No"
    elif msg in ['How are you?', 'how are you?']:
        r = "Hey, I am fine!"
    elif msg in ['Who are you?', 'who are you?']:
        r = "I am a Line robot"


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()

    
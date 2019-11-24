from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)
import os

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["coWmXP5AQuEvAXR+dVPQlsjLUGbRJqyyO5KoDt4JIaLSrOjbakB+O5ZxOYIb9x77nPDXppgXaJ12+G93QQepUV6QR+Yk4oAB+kS3LFZPSSmCFnVJGlD1ZPDbpfYFTTPO7f0X7utim2C2S+3UifM0bQdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["0c6ea2975865835d3d3e1a76bc4b0fc3"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        HttpResponseForbidden()
    return HttpResponse('OK', status=200)


# オウム返し
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=event.message.text))

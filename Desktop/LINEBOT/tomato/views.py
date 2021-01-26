from django.shortcuts import render
from django.http import JsonResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from django.conf import settings
from flask import Flask
import os, time

line_bot_api=LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(settings.LINE_CHANNEL_SECRET)


    
app=Flask(__name__)

@app.route("https://tttomato.herokuapp.com/callback",method=['POST'])
def webhook_view(request):
    signature=request.headers["X-Line-Signature"]
    body_decode=request.body.decode('utf-8')
    
    try:
        handler.handle(body_decode, signature)
    except InvalidSignatureError:
        return HttpResponseBadRequest
    return HttpResponse("OK")
    

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event:MessageEvent):
    while event.message.text=="start":
        
        for i in range(1,5):
            time.sleep(300)  
        
            line_bot_api.reply_message(
                reply_token=event.reply_token,
                messages=TextSendMessage(text="{} minutes passed.".format(i*5))
                )
    
            time.sleep(300)
            line_bot_api.reply_message(
                reply_token=event.reply_token,
                messages=TextSendMessage(text="five minutes to rest!")
                )
            time.sleep(300)
    if event.message.text=="stop":
        line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text="tomato timer has stopped."))
        
    
    
      
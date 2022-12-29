from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageAction, FlexSendMessage, 
    QuickReply, QuickReplyButton
)

import re
import myfun
import json

app = Flask(__name__)

line_bot_api = LineBotApi('+83vAxJpGIgdbXx/Z/ydEZ+hSEoOgUT6MeoZ/875ZxVJgnp/qajR5aWv6AF449eQ2iaFBsHzY1NcnKccg8mDNyh2v7K+QzssVF76FocV7mbyhwVLQf6P9ZmjfeXUhqFkdKFIRRPCUJ2RvyX7K4UlAgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7353e5bd2cc77001f5181fc4f9daf087')

import requests
line_token = 'qdtX8sI1V5mvUIaqddzI4mKftsKZbhsHyvoGxSGaVaW'
def lineNotifyMessage(token, msg):
    headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"}
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
    return r.status_code

# line_bot_api.push_message('', TextSendMessage(text='LineBot已經重新部署'))

# @app.route('/', methods=["GET","POST"])
# def home():
#     return "HOME"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    body_json = json.loads(body)
    # print(type(body_json))
    userId = body_json['events'][0]['source']['userId']

    if userId == 'U2673b3f13b19e17c33c6303183927b83':
        lineNotifyMessage(line_token, '媛婷測試中')
    elif userId == 'U3edcec9e79359b29e7b95af2f2e679f2':
        lineNotifyMessage(line_token, '毓權測試中')
    # elif userId == 'U6eafb09dfb16a8550ca085e278dd227d':
    #     lineNotifyMessage(line_token, '嘉欣測試中')
    # elif userId == 'U6eafb09dfb16a8550ca085e278dd227d':
    #     lineNotifyMessage(line_token, '幃尹測試中')

    
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
    
    msg_text = event.message.text
    if re.match('@最新消息', msg_text):
        # obj = TextSendMessage(text = myfun.moex_news())
        obj = FlexSendMessage(alt_text = '機器人',contents = myfun.moex_news())
    elif re.match('@考試公告', msg_text):
        # obj =TextSendMessage(text = myfun.wfrm_news())
        obj = FlexSendMessage(alt_text = '機器人',contents = myfun.wfrm_news())
    
    elif re.match('@代碼查詢', msg_text):
        # out = myfun.subject_id()
        # obj = TemplateSendMessage(
        #     alt_text='請選擇',
        #     template=ConfirmTemplate(
        #         text='考試類型',
        #         actions=[
        #             MessageAction(label='高考',text='@高考代碼'),
        #             MessageAction(label='普考',text='@普考代碼')
        #         ])
        #     )
        obj = TextSendMessage(text='請點擊', quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label='高考', text='@高考代碼')),
                QuickReplyButton(action=MessageAction(label='普考', text='@普考代碼'))]))
    elif re.match('@高考代碼', msg_text):
        obj1 =FlexSendMessage(alt_text = '高考代碼',contents = myfun.subject_id('高考'))
        obj2 = TextSendMessage(text = '請輸入代碼：')
        obj = [obj1, obj2]
        # obj =TextSendMessage(text = myfun.subject_id('高考'))
    elif re.match('@普考代碼', msg_text):
        obj1 =FlexSendMessage(alt_text = '普考代碼',contents = myfun.subject_id('普考'))
        obj2 = TextSendMessage(text = '請輸入代碼：')
        obj = [obj1, obj2]
        # obj =TextSendMessage(text = myfun.subject_id('普考'))

    elif re.match('@錄取率排行', msg_text):
        # out = myfun.subject_id()
        obj = TemplateSendMessage(
            alt_text='請選擇',
            template=ConfirmTemplate(
                text='考試類型',
                actions=[
                    MessageAction(label='高考錄取率',text='@高考錄取率'),
                    MessageAction(label='普考錄取率',text='@普考錄取率')
                ])
            )
    elif re.match('@高考錄取率', msg_text):
        obj =FlexSendMessage(alt_text = '高考錄取率',contents = myfun.acceptance_rate('高考錄取率'))
    elif re.match('@普考錄取率', msg_text):
        obj =FlexSendMessage(alt_text = '普考錄取率',contents = myfun.acceptance_rate('普考錄取率'))

    elif re.match('@國考介紹', msg_text):
        obj =FlexSendMessage(alt_text = '機器人',contents = myfun.test_introduction())
    
    elif re.match('@使用說明', msg_text):
        obj =TextSendMessage(myfun.app_introduction())

    elif re.match('@國考類型', msg_text):
        obj = TextSendMessage(text='請點擊', quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label='高普初考', text='@高普初考介紹')),
                QuickReplyButton(action=MessageAction(label='特種考試', text='@特種考試介紹')),
                QuickReplyButton(action=MessageAction(label='國營事業', text='@國營事業介紹'))]))
    elif re.match('@高普初考介紹', msg_text):
        obj =FlexSendMessage(alt_text = '高普初考介紹',contents = myfun.test_introduction_1())
    elif re.match('#高考詳細介紹', msg_text):
        obj =FlexSendMessage(alt_text = '高考詳細介紹',contents = myfun.test_introduction_1h())
    elif re.match('#普考詳細介紹', msg_text):
        obj =FlexSendMessage(alt_text = '普考詳細介紹',contents = myfun.test_introduction_1m())
    elif re.match('#初考詳細介紹', msg_text):
        obj =FlexSendMessage(alt_text = '初考詳細介紹',contents = myfun.test_introduction_1l())

    elif re.match('@特種考試介紹', msg_text):
        obj =FlexSendMessage(alt_text = '特種考試介紹',contents = myfun.test_introduction_2())
    elif re.match('#聯招詳細介紹', msg_text):
        obj =FlexSendMessage(alt_text = '聯招詳細介紹',contents = myfun.test_introduction_3_1())
    elif re.match('#獨招詳細介紹', msg_text):
        obj =FlexSendMessage(alt_text = '獨招詳細介紹',contents = myfun.test_introduction_3_2())

    elif re.match('@國營事業介紹', msg_text):
        obj =FlexSendMessage(alt_text = '國營事業介紹',contents = myfun.test_introduction_3())

    elif re.match('H', msg_text[0]):
        obj =FlexSendMessage(alt_text = '高考介紹',contents = myfun.test_subject_introduction('高考', msg_text[1:4]))
    elif re.match('S', msg_text[0]):
        obj =FlexSendMessage(alt_text = '普考介紹',contents = myfun.test_subject_introduction('普考', msg_text[1:3]))
        
    # elif re.match('@exam', msg_text[0:5]):
    #     obj =TextSendMessage(text = myfun.exam(msg_text[6:]))
    elif re.match('@exam', msg_text[0:5]):
        print(msg_text[6:])
        obj =FlexSendMessage(alt_text = '考古題', contents = myfun.exam(msg_text[6:]))
    elif re.match('#exam', msg_text[0:5]):
        obj =TextSendMessage(text = myfun.exam_link(msg_text[6:]))


    elif re.match('9527', msg_text):
        # James
        # line_bot_api.push_message('U3edcec9e79359b29e7b95af2f2e679f2', TextSendMessage(text='LineBot已經重新部署'))
        # 媛婷
        line_bot_api.push_message('U2673b3f13b19e17c33c6303183927b83', TextSendMessage(text='LineBot已經重新部署'))
        obj =TextSendMessage(text = '已通知群組')
    else:
        obj = TextSendMessage(text = f'error {msg_text}')
    # print(obj)
    line_bot_api.reply_message(event.reply_token, obj)

if __name__ == "__main__":
    # app.run()
    app.run(host="192.168.0.107",ssl_context=('civiltool.cc_server.crt', 'civiltool.cc_server.key'), port = 443)


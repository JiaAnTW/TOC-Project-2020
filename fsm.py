from transitions.extensions import GraphMachine

from utils import send_text_message, send_template_message
from linebot.models import ButtonsTemplate,PostbackTemplateAction,TemplateSendMessage

stateOneTemplate=TemplateSendMessage(
        alt_text='Buttons Template',
        template=ButtonsTemplate(
            title='歡迎使用waku計時器！',
            text='根據您的需求點選點選下方功能',
            thumbnail_image_url='https://swordshield.portal-pokemon.com/tc/pokemon/img/pokemon-image_v10_1-1.png',
            actions=[
                PostbackTemplateAction(
                    label='自訂計時',
                    text='userDefine',
                    data='userDefine'
                ),
                PostbackTemplateAction(
                    label='查詢計時',
                    text='query',
                    data='query'
                )
            ]
        )
    )

timeTemplate=TemplateSendMessage(
        alt_text=' Template',
        template=ButtonsTemplate(
            title='目前設定為',
            text='利用下方按鍵開始設定\n設定完成請點選確定',
            thumbnail_image_url='https://swordshield.portal-pokemon.com/tc/pokemon/img/pokemon-image_v10_1-1.png',
            actions=[
                PostbackTemplateAction(
                    label='設定地點',
                    text='設定地點',
                    data='min'
                ),
                PostbackTemplateAction(
                    label='設定時間',
                    text='設定時間',
                    data='sec'
                ),
                PostbackTemplateAction(
                    label='確定送出',
                    text='確定送出',
                    data='send'
                ),
                PostbackTemplateAction(
                    label='返回',
                    text='返回',
                    data='back'
                )
            ]
        )
    )

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return True

    def is_going_to_state2(self, event):
        text = event.message.text
        print("Check if it can go to state 2")
        return text.lower() == "query"

    def on_enter_state1(self, event):
        print("I'm entering state1")
        reply_token = event.reply_token
        send_template_message(reply_token, stateOneTemplate)

    def on_exit_state1(self,ev):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")
        reply_token = event.reply_token
        send_template_message(reply_token, timeTemplate)
        #self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")

from linebot.models import ButtonsTemplate,PostbackTemplateAction,TemplateSendMessage

def get_center_msg():
    stateOneTemplate=TemplateSendMessage(
        alt_text='Buttons Template',
        template=ButtonsTemplate(
            title='歡迎使用waku計時器！',
            text='根據您的需求點選點選下方功能',
            thumbnail_image_url='https://swordshield.portal-pokemon.com/tc/pokemon/img/pokemon-image_v10_1-1.png',
            actions=[
                PostbackTemplateAction(
                    label='自訂計時',
                    text='開啟自訂計時',
                    data='userDefine'
                ),
                PostbackTemplateAction(
                    label='查詢計時',
                    text='開啟查詢計時',
                    data='query'
                )
            ]
        )
    )
    return stateOneTemplate

def get_set_clock_msg(timer):
    min=str(timer['min'])
    sec=str(timer['sec'])
    timeTemplate=TemplateSendMessage(
        alt_text=' Template',
        template=ButtonsTemplate(
            title='目前設定為\n間隔 '+min+'分 '+sec+'秒',
            text='利用下方按鍵開始設定\n設定完成請點選確定',
            actions=[
                PostbackTemplateAction(
                    label='設定時間',
                    text='設定時間',
                    data='time'
                ),
                PostbackTemplateAction(
                    label='設定號碼牌',
                    text='設定號碼牌',
                    data='number'
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
    return timeTemplate
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

def get_set_clock_msg(timer,number):
    #min=str(timer['min'])
    #sec=str(timer['sec'])
    now=str(number['now'])
    target=str(number['target'])
    timeTemplate=TemplateSendMessage(
        alt_text=' Template',
        template=ButtonsTemplate(
            title='目前設定為\n每號間隔 '+str(timer)+',由'+now+'號開始等到'+target+'號',
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

def get_set_clockCenter_msg(timer,isCounting):
    #min=str(timer['min'])
    #sec=str(timer['sec'])
    if(isCounting==True):
        counterBtn=PostbackTemplateAction(
                    label='結束計時',
                    text='結束計時',
                    data='start'
        )
        topic='計時中,可按下「結束計時」以完成計時'
        
    else:
        counterBtn=PostbackTemplateAction(
                    label='開始計時',
                    text='開始計時',
                    data='start'
        )
        topic='目前設定為\n每號間隔 '+str(timer)

    timeTemplate=TemplateSendMessage(
        alt_text=' Template',
        template=ButtonsTemplate(
            title=topic,
            text='利用下方按鍵開始設定\n設定完成請點選確定',
            actions=[
                counterBtn,
                PostbackTemplateAction(
                    label='直接輸入時間',
                    text='直接輸入時間',
                    data='input'
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

def get_set_number_msg(number):
    now=str(number['now'])
    target=str(number['target'])
    numberTemplate=TemplateSendMessage(
        alt_text=' Template',
        template=ButtonsTemplate(
            title='您的號碼為 '+target+',目前號碼為 '+now,
            text='利用下方按鍵開始設定\n設定完成請點選確定',
            actions=[
                PostbackTemplateAction(
                    label='設定你的號碼',
                    text='設定你的號碼',
                    data='target'
                ),
                PostbackTemplateAction(
                    label='設定目前號碼',
                    text='設定目前號碼',
                    data='now'
                ),
                PostbackTemplateAction(
                    label='返回',
                    text='返回',
                    data='back'
                )
            ]
        )
    )
    return numberTemplate
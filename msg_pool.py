from linebot.models import MessageTemplateAction,ButtonsTemplate,PostbackTemplateAction,TemplateSendMessage,CarouselTemplate,CarouselColumn
import datetime

def get_center_msg():
    stateOneTemplate=TemplateSendMessage(
        alt_text='歡迎使用waku計時器！',
        template=ButtonsTemplate(
            title='歡迎使用waku計時器！',
            text='根據您的需求點選點選下方功能',
            thumbnail_image_url='https://swordshield.portal-pokemon.com/tc/pokemon/img/pokemon-image_v10_1-1.png',
            actions=[
                MessageTemplateAction(
                    label='新增計時',
                    text='開啟自訂計時'
                ),
                MessageTemplateAction(
                    label='以地點新增計時',
                    text='以地點新增計時'
                ),
                MessageTemplateAction(
                    label='查看目前計時器',
                    text='查看目前計時器'
                ),
                MessageTemplateAction(
                    label='不要偷看啦',
                    text='還是要偷看'
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
        alt_text=' 設定計時器',
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
        alt_text=' 設定時間',
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
        alt_text='設定號碼',
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

def get_book_msg(dataArray):
    card=[]
    i=1
    card.append(
                CarouselColumn(
                title= "往左滑動即可察看目前的號碼牌",
                text='.',
                actions=[
                    MessageTemplateAction(
                        label='返回',
                        text='返回'
                    ),MessageTemplateAction(
                        label='返回',
                        text='返回'
                    ),MessageTemplateAction(
                        label='返回',
                        text='返回'
                    )
                ]
            )

        )
    for data in dataArray:
        start=data['clock']['start']
        period=data['clock']['time']
        number=data['number']
        print(str(data))
        if data['name']!=None:
            name=data['name']
        else:
            name="計時器"+str(i)
        waitRate=(number['target']-number['now'])
        predictTime=datetime.timedelta(hours=start.hour,minutes = start.minute, seconds = start.second)+waitRate*period
        card.append(
            CarouselColumn(
                title= name+", 從"+str(number['now'])+"等到"+str(number['target'])+"號",
                text='預計於'+str(predictTime)+'輪到你',
                actions=[
                    PostbackTemplateAction(
                        label='更改計時器名稱',
                        text='更改計時器名稱',
                        data=i-1
                    ),
                    PostbackTemplateAction(
                        label='修改號碼牌內容',
                        text='修改號碼牌內容',
                        data=i-1
                    ),
                    PostbackTemplateAction(
                        label='輸入位置資訊',
                        text='輸入位置資訊',
                        data=i-1
                    ),
                ]
            )

        )
        i=i+1

    Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(columns=card)
    )
    return Carousel_template

def get_locationCenter_msg(spotName,locationInfo):
    if spotName!=None:
        name=spotName
    else:
        name="尚未設定"
    if locationInfo!=None:
        info=locationInfo['address']+" (經度"+str(locationInfo['latitude'])+", 緯度"+str(locationInfo['longitude'])+")"
    else:
        info="尚未設定"

    timeTemplate=TemplateSendMessage(
        alt_text=' 設定地點',
        template=ButtonsTemplate(
            title= "地點： "+name,
            text="地理資訊: "+str(info),
            actions=[
                MessageTemplateAction(
                    label='輸入地點名稱',
                    text='輸入地點名稱'
                ),
                MessageTemplateAction(
                    label='回傳地理資訊',
                    text='回傳地理資訊'
                ),
                MessageTemplateAction(
                    label='返回',
                    text='返回'
                )
            ]
        )
    )
    return timeTemplate
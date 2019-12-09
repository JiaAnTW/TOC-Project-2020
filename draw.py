import pygraphviz as pgv

node_array=[
            "開始",
            "號碼牌中心",
            "設定時間",
            "設定號碼牌",
            "接收手動輸入時間",
            "接收自己號碼",
            "接收目前號碼",
            "瀏覽目前計時器",
            "設定地點",
            "接收地點名稱",
            "接收地理資訊"]   


A=pgv.AGraph(directed=True,splines='curved')
   
(x,y)=(0,0)
#增加四个点1 2 3 4
for i in range(len(node_array)):
    A.add_node(node_array[i])
    A.get_node(node_array[i]).attr['shape']='circle'
    A.get_node(node_array[i]).attr['fixedsize']=True
    A.get_node(node_array[i]).attr['width']=1.5    
    A.get_node(node_array[i]).attr['height']=1.5
      
   
#指定四个点的坐标位置 注意 “！”
A.get_node("開始").attr['pos']="%d,%d!"%(x,y)
A.get_node("瀏覽目前計時器").attr['pos']="%d,%d!"%(x+4,(y-4))
A.get_node("設定地點").attr['pos']="%d,%d!"%(x+8,y-3-4)
A.get_node("接收地點名稱").attr['pos']="%d,%d!"%(x+12,y-2-4)
A.get_node("接收地理資訊").attr['pos']="%d,%d!"%(x+12,y-4-4)

A.get_node("號碼牌中心").attr['pos']="%d,%d!"%(x+8,y)
A.get_node("設定時間").attr['pos']="%d,%d!"%(x+12,y+2)
A.get_node("設定號碼牌").attr['pos']="%d,%d!"%(x+12,1*(y-2))
A.get_node("接收手動輸入時間").attr['pos']="%d,%d!"%(x+16,(y+2))
A.get_node("接收自己號碼").attr['pos']="%d,%d!"%(x+16,y-1)
A.get_node("接收目前號碼").attr['pos']="%d,%d!"%(x+16,y-3)



   
#增加三条边
A.add_edge("開始","號碼牌中心")
A.get_edge("開始","號碼牌中心").attr['label']="自訂計時器,λ,開始"

A.add_edge("號碼牌中心","開始")
A.get_edge("號碼牌中心","開始").attr['label']="返回,開始,λ"

A.add_edge("開始","瀏覽目前計時器")
A.get_edge("開始","瀏覽目前計時器").attr['label']="查看目前計時器,λ,λ"

A.add_edge("瀏覽目前計時器","開始")
A.get_edge("瀏覽目前計時器","開始").attr['label']="返回,λ,λ"

A.add_edge("瀏覽目前計時器","號碼牌中心")
A.get_edge("瀏覽目前計時器","號碼牌中心").attr['label']="修改號碼牌內容,λ,瀏覽目前計時器"

A.add_edge("號碼牌中心","瀏覽目前計時器")
A.get_edge("號碼牌中心","瀏覽目前計時器").attr['label']="返回,瀏覽目前計時器,λ"

A.add_edge("瀏覽目前計時器","設定地點")
A.get_edge("瀏覽目前計時器","設定地點").attr['label']="輸入位置資訊,λ,λ"

A.add_edge("設定地點","瀏覽目前計時器")
A.get_edge("設定地點","瀏覽目前計時器").attr['label']="返回,λ,λ"

A.add_edge("設定地點","接收地點名稱")
A.get_edge("設定地點","接收地點名稱").attr['label']="輸入地點名稱,λ,設定地點"

A.add_edge("接收地點名稱","設定地點")
A.get_edge("接收地點名稱","設定地點").attr['label']="*,設定地點,λ"

A.add_edge("設定地點","接收地理資訊")
A.get_edge("設定地點","接收地理資訊").attr['label']="輸入地理資訊,λ,設定地點"

A.add_edge("接收地理資訊","設定地點")
A.get_edge("接收地理資訊","設定地點").attr['label']="*,設定地點,λ"

A.add_edge("號碼牌中心","設定時間")
A.get_edge("號碼牌中心","設定時間").attr['label']="設定時間,λ,λ"

A.add_edge("設定時間","設定時間")
A.get_edge("設定時間","設定時間").attr['label']="開始計時,λ,開始計時"

A.add_edge("設定時間","設定時間")
A.get_edge("設定時間","設定時間").attr['label']="停止計時,開始計時,λ"

A.add_edge("設定時間","號碼牌中心")
A.get_edge("設定時間","號碼牌中心").attr['label']="返回,λ,λ"

A.add_edge("號碼牌中心","設定號碼牌")
A.get_edge("號碼牌中心","設定號碼牌").attr['label']="設定號碼牌,λ,λ"

A.add_edge("設定號碼牌","號碼牌中心")
A.get_edge("設定號碼牌","號碼牌中心").attr['label']="返回,λ,λ"

A.add_edge("設定時間","接收手動輸入時間")
A.get_edge("設定時間","接收手動輸入時間").attr['label']="直接輸入時間,λ,λ"

A.add_edge("接收手動輸入時間","設定時間")
A.get_edge("接收手動輸入時間","設定時間").attr['label']="*,λ,λ"

A.add_edge("接收自己號碼","設定號碼牌")
A.get_edge("接收自己號碼","設定號碼牌").attr['label']="設定自己號碼,λ,λ"

A.add_edge("設定號碼牌","接收自己號碼")
A.get_edge("設定號碼牌","接收自己號碼").attr['label']="*,λ,λ"

A.add_edge("接收目前號碼","設定號碼牌")
A.get_edge("接收目前號碼","設定號碼牌").attr['label']="設定目前號碼,λ,λ"

A.add_edge("設定號碼牌","接收目前號碼")
A.get_edge("設定號碼牌","接收目前號碼").attr['label']="*,λ,λ"

A.write('simple.dot')  # write to simple.dot
A.layout()             # neato, node pos isnot available in dot
A.draw('simple.png')   # draw picture
print(A.string())
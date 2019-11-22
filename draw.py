import pygraphviz as pgv

node_array=["開始","計時器","取得目前時間","取得可能點","輸入小時","輸入分鐘","輸入秒數"]   

A=pgv.AGraph(directed=True)
   
(x,y)=(0,0)
#增加四个点1 2 3 4
for i in range(len(node_array)):
    A.add_node(node_array[i])
    A.get_node(node_array[i]).attr['shape']='circle'    
   
#指定四个点的坐标位置 注意 “！”
A.get_node("開始").attr['pos']="%d,%d!"%(x,y)
A.get_node("計時器").attr['pos']="%d,%d!"%(x+5,(y+2))
A.get_node("取得目前時間").attr['pos']="%d,%d!"%(x+5,-1*(y+2))
A.get_node("取得可能點").attr['pos']="%d,%d!"%(x+10,y)
A.get_node("輸入小時").attr['pos']="%d,%d!"%(x+15,y+2)
A.get_node("輸入分鐘").attr['pos']="%d,%d!"%(x+15,y)
A.get_node("輸入秒數").attr['pos']="%d,%d!"%(x+15,y-2)
   
#增加三条边
A.add_edge("開始","計時器")
A.add_edge("開始","取得目前時間")
A.add_edge("計時器","取得目前時間")
A.add_edge("計時器","輸入小時")
A.add_edge("計時器","輸入分鐘")
A.add_edge("計時器","輸入秒數")   

A.write('simple.dot')  # write to simple.dot
A.layout()             # neato, node pos isnot available in dot
A.draw('simple.png')   # draw picture
print(A.string())
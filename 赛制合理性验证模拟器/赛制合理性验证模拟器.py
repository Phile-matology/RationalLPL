'''
这是一次验证赛制合理性的简单尝试。
代码中保留了一些最终没有使用到的功能，由于时间原因，没有再单独开发接口来使用
更新rank列表以使用最新常规赛排名
修改Init函数中的部分注释以开启自定义队名模式（注意，这一功能要求每一次模拟都要输入一次，如果更改用于大规模模拟，请修改rank列表
print均用于单次模拟结果的展示，包括每一个BO5的每一小局，这可以让你开启自己版本的季后赛旅程，但他们的胜败是不能被操控的
大批量模拟是基于极差的变化，观察季后赛队伍水平差距对常规赛冠军夺冠几率带来的影响
特别的，对比大批量模拟被用于比较LPL新旧赛制的合理性
'''



import random
import math
import matplotlib.pyplot as plt

global Teamlist
Teamlist = []
rank = ['fpx','edg','ra','rng','tes','blg','we','lng','sn','omg']       #这是默认的常规赛排名，数据来源：2021LPL夏季赛
def Init(format,varience):
    global flag
    global Teamlist
    global rank
    Teamlist=[]
    if Format == '半区淘汰赛':
        for i in range(8):
            Teamlist.append(["",random.uniform(0.5,0.5+varience)])
    elif Format == '四强双败赛':
        for i in range(10):
            Teamlist.append(["",random.uniform(0.5,0.5+varience)])
    else:
        print("暂不支持此赛制") 
    Teamlist.sort(key = lambda x:x[1],reverse=True)
    #if flag:
        #print("请按常规赛排名顺序输入队伍名称")                   如果要开启自定义队名模式，请取消该行和上一行的注释，并修改下一个循环中的输入方式
    for j in range(len(Teamlist)):
        #Teamlist[j][0]=input("第"+str(j+1)+"名：")
        Teamlist[j][0]=rank[j]
    if flag:
        print("战队原始实力榜：")
        for j in range(len(Teamlist)):
            print(Teamlist[j])
    
def BestOf5Games(teamx,teamy):
    global flag
    global Teamlist
    strenth1 = Teamlist[teamx][1]+random.uniform(-0.1,0.1)
    strenth2 = Teamlist[teamy][1]+random.uniform(-0.1,0.1)
    tactics1 = random.uniform(0.8,1.2)
    tactics2 = random.uniform(0.8,1.2)
    wins={teamx:0,teamy:0}
    if flag:
        print("Origin: "+Teamlist[teamx][0]+" : "+str(strenth1*tactics1)+", "+Teamlist[teamy][0]+" : "+str(strenth2*tactics2))
    while(wins[teamx] < 3 and wins[teamy] < 3):
        if strenth1*tactics1>=strenth2*tactics2:
            teamxwinrate=1.72*math.log(strenth1*tactics1-strenth2*tactics2+1,math.e)+0.5
        else:
            teamxwinrate=1-(1.72*math.log(strenth2*tactics2-strenth1*tactics1+1,math.e)+0.5)
        result = random.random()-teamxwinrate
        if result <= 0:
            wins[teamx]+=1
        else:
            wins[teamy]+=1
        if flag:
            print("Game"+str(wins[teamx]+wins[teamy])+": "+str(result))
        strenth1+=random.uniform(-0.02,0.02)
        strenth2+=random.uniform(-0.02,0.02)
        if flag:
            print("After Game"+str(wins[teamx]+wins[teamy])+": "+Teamlist[teamx][0]+" : "+str(strenth1*tactics1)+", "+Teamlist[teamy][0]+" : "+str(strenth2*tactics2))
    winner = max(wins,key=wins.get)
    loser = min(wins,key=wins.get)
    if flag:
        print(Teamlist[teamx][0]+" vs "+Teamlist[teamy][0]+" : "+Teamlist[winner][0]+" wins at 3 : "+str(wins[loser])+"\n")
    return (winner,loser)

def SemifinalsForKnockout(Team1,Team2,Team3,Team4):
    return BestOf5Games(BestOf5Games(Team1,Team4)[0],BestOf5Games(Team2,Team3)[0])[0]

def SemifinalsForDoubledefeat(Team1,Team2,Team3,Team4,Team5):
    return (Team1,BestOf5Games(Team2,BestOf5Games(Team3,BestOf5Games(Team4,Team5)[0])[0])[0])


def Playoffs(Format,va):
    Init(Format,va/100)
    if Format == '半区淘汰赛':
        if flag:
            print("上半区赛况：")
        DivWinner1=SemifinalsForKnockout(0,3,4,7)
        if flag:
            print("下半区赛况：")
        DivWinner2=SemifinalsForKnockout(1,2,5,6)
        Champion=BestOf5Games(DivWinner1,DivWinner2)[0]
        if flag:
            print("总冠军队伍是："+Teamlist[Champion][0])
    elif Format == '四强双败赛':
        if flag:
            print("上半区赛况：")
        DivWinners1=SemifinalsForDoubledefeat(0,3,4,7,8)
        if flag:
            print("下半区赛况：")
        DivWinners2=SemifinalsForDoubledefeat(1,2,5,6,9)
        if flag:
            print("双败赛赛况：")
        (win1,lose1)=BestOf5Games(DivWinners1[0],DivWinners1[1])
        (win2,lose2)=BestOf5Games(DivWinners2[0],DivWinners2[1])
        (winchampion,lose3)=BestOf5Games(win1,win2)
        lose4=BestOf5Games(lose1,lose2)[0]
        losechampion=BestOf5Games(lose3,lose4)[0]
        Champion=BestOf5Games(winchampion,losechampion)[0]
        if flag:
            print("总冠军队伍是："+Teamlist[Champion][0])
    else:
        print("暂不支持此赛制")
        Champion=-1
    return Champion



#以下是函数入口
flag=0
Mode=input("请输入模式：单次模拟/大规模模拟/对比大规模模拟:")
if Mode == '单次模拟':
    Format=input("请输入你想模拟的赛制：半区淘汰赛/四强双败赛：")
    flag=1
    varience=eval(input("请输入队伍实力极差："))
    Playoffs(Format,varience)
elif Mode == '大规模模拟':
    Format=input("请输入你想模拟的赛制：半区淘汰赛/四强双败赛：")
    times=eval(input("请输入实验次数："))
    recordx = []
    recordy = []
    for varience in range(5,50,1):
        count = 0
        recordx.append(varience/100)
        for i in range(times):
            count+=(Playoffs(Format,varience)==0)
        recordy.append(count/times)
    plt.plot(recordx,recordy)
    plt.show()
elif Mode == '对比大规模模拟':
    times=eval(input("请输入实验次数："))
    Format='半区淘汰赛'
    recordx = []
    recordy = []
    for varience in range(5,50,1):
        count = 0
        recordx.append(varience/100)
        for i in range(times):
            count+=(Playoffs(Format,varience)==0)
        recordy.append(count/times)
    plt.plot(recordx,recordy,color='red')
    Format='四强双败赛'
    recordx = []
    recordy = []
    for varience in range(5,50,1):
        count = 0
        recordx.append(varience/100)
        for i in range(times):
            count+=(Playoffs(Format,varience)==0)
        recordy.append(count/times)
    plt.plot(recordx,recordy,color='blue')
    plt.show()
else:
    print("暂不支持此模式")
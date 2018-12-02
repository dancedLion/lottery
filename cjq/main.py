#encoding="utf-8"
import tkinter
import random
import threading
import time
import os
from settings import drawsettings

#初始化窗口
root=tkinter.Tk()
root.title("随机抽取名单")
root.geometry('600x350+400+200')
root.resizable(False,False)
root.flag = True

#全局变量 /轮数/等待时间/已抽取数[可以不用]
roundcount=[]
roundname=[]
randomnum=[]
roundreset=0
roundno=1
waittime=15
randinsettings=1
waitfornextRound=False
#三个Lable标签
first = tkinter.Label(root,text='',font = ("microsoft yahei", 20,"normal"),wraplength=450,justify="left")
first.place(x=50,y=100,width=450,height=200)

#second = tkinter.Label(root,text='',font = ("宋体", 20,"normal"))
#second['fg'] = 'red'
#second.place(x=180,y=200,width=150,height=100)

#third = tkinter.Label(root,text='',font = ("宋体", 20,"normal"))
#third.place(x=180,y=300,width=150,height=100)

currentround=tkinter.Label(root,text='',font=("microsoft yahei",20,"normal"))
currentround.place(x=50,y=70,width=300,height=30)
currentroundprogress=tkinter.Label(root,text='',font=('microsoft yahei',20,"normal"))
currentroundprogress.place(x=360,y=70,width=200,height=30)
message=tkinter.Label(root,text='',font=('microsoft yahei',20,"normal"))
message.place(x=30,y=300,width=500,height=30)
#定义抽奖i
i=-1

students=['杨姐姐1','杨姐姐2','杨姐姐3','杨姐姐4','杨姐姐5','杨姐姐6']
studentsin=[]

def dorandom():
    #获取抽取数量,来自于设置，如果大于待抽人数，则为待抽人数，如果大于本轮剩余人数，则为本轮剩余人数
    global roundno,randomnum,roundcount,studentsin,students,waitfornextRound
    nums=randomnum[roundno-1]
    if nums>len(students):
        nums=len(students)
    if eval(roundcount[roundno-1].split(":")[1])-len(studentsin)<nums:
        nums=eval(roundcount[roundno-1].split(":")[1])-len(studentsin)
    if nums<=0:
        #goto the next round
        showmessage("本轮次已经抽取完成所有人，请进入一下轮！")
        waitfornextRound=True
    else:
        randtext=""
        for i in range(nums):
            rand=random.randint(0,len(students)-1)
            randtext+=students[rand]+","
            studentsin.append(students[rand])
            students.remove(students[rand])
        showstudents(randtext)
        currentroundprogress["text"]=str(len(studentsin))+ ("/"+str(roundcount[roundno-1].split(":")[1]) if randinsettings==1 else "")
        if eval(roundcount[roundno-1].split(":")[1])==len(studentsin):
            showmessage("本轮次已经抽取完成所有人，请进入一下轮！")
            waitfornextRound=True
        #如果人数达到，则进入下一轮
        #if(nums+len(studentsin)>=eval(roundcount[roundno].split(":")[1])):
        #    gotonext()
def showstudents(string):
    first["text"]=string


def gotonext():
    global roundno,roundcount,randomnum,roundreset,roundname,randinsettings,studentsin
    studentsin=[]
    if len(roundcount)>=roundno:
        currentround["text"]="当前轮次："+roundname[roundno-1]
        currentroundprogress["text"]="0/"+roundcount[roundno-1].split(":")[1]
        if roundreset==1:
            readStudents()
            #按顺序重新读取
    else:
        showmessage("所有抽取已经结束，将进入自由模式")
        randinsettings=-1
        gotononprogram()

def gotononprogram():
    global randinsettings
    randinsettings=-1
    currentround["text"]="自由模式:"+str(roundno-len(roundcount))
    currentroundprogress["text"]="0"
    showmessage("非程序设定模式")
def showinstudents():
    global studentsin
    sts=""
    for student in studentsin:
        sts=sts+student+","
    first["text"]=sts

def showmessage(string):
    message["text"]=string

def loadtxtsettings():
    #从配置文件中获取配置
    #返回轮数-人数,轮次名称,每轮结束是否重置,每次抽取人数       
    rounds=[]   #轮次和人数
    roundsname=[]   #轮次显示名称
    roundreset=1    #每轮重置
    randomnum=[]   #每次抽取人数
    with open("settings.txt",'rb') as f:
        for line in f:
            rowstr=line.decode("utf-8").replace("\r\n","")
            if rowstr[0]=="#":
                continue
            if rowstr[:len("roundcount")]=="roundcount":
                setting=rowstr.split('=')[1]
                if setting:
                    rounds=setting.split(',')
            if rowstr[:len("roundname")]=="roundname":
                setting=rowstr.split("=")[1]
                if setting:
                    roundsname=setting.split(",")
            if rowstr[:len("randomnum")]=="randomnum":
                setting=rowstr.split('=')[1]
                if setting:
                    setting=setting.split(',')
                    for num in setting:
                        randomnum.append(eval(num))
            if rowstr[:len("roundreset")]=="roundreset":
                setting=rowstr.split("=")[1]
                if setting:
                    roundreset=eval(setting)
                else:
                    roundreset=0
    return rounds,roundsname,roundreset,randomnum

def switch():
    global i
    root.flag=True
    while root.flag:
        i=random.randint(0, len(students)-1)
        first['text']=students[i]
        #second['text']=third['text']
        #third['text']=students[i]
        time.sleep(0.1)

def readStudents():
    global students
    #os.path.abspath(__file__)
    students.clear()
    print(os.getcwd())
    f=open('list.txt','rb')
    for line in f:
        students.append(line.decode("utf-8").replace("\r\n",""))
    f.close()
    #print(students)

#开始按钮
def butStartClick():
    global waitfornextRound
    if waitfornextRound:
        return
    t=threading.Thread(target=switch)
    showmessage("抽取中.....")
    t.start()

btnStart=tkinter.Button(root,text='开始',command=butStartClick)
btnStart.place(x=30, y=30, width=80, height=20)

#结束按钮
def btnStopClick():
    global i
    root.flag=False
    showmessage("")
    if randinsettings==1:
        dorandom()
    else:
        studentsin.append(students[i])
        students.remove(students[i])
        currentroundprogress["text"]=str(len(studentsin))
    #print(studentsin)

#等待时间到了以后，自动抽取结果


def nextRound():
    global studentsin,i,roundno,waitfornextRound
    waitfornextRound=False
    roundno+=1
    if roundno<=len(roundcount):
        gotonext()
    else:
        readStudents()
        studentsin=[]
        i=-1 
        gotononprogram()

def opensettings():
    setform=drawsettings()
    setform.writeform()
    setform.start()
    
def loadsettings():
    global roundcount,roundname,randomnum,roundreset
    roundcount,roundname,roundreset,randomnum=loadtxtsettings()


butStop=tkinter.Button(root,text='停止',command=btnStopClick)
butStop.place(x=120, y=30, width=80, height=20)
butNext=tkinter.Button(root,text="下一轮",command=nextRound)
butNext.place(x=330,y=30,width=80,height=20)

buttonShowIns=tkinter.Button(root,text="显示人员",command=showinstudents)
buttonShowIns.place(x=220,y=30,width=80,height=20)
butSet=tkinter.Button(root,text="设置",command=opensettings)
butSet.place(x=450,y=30,width=80,height=20)


#启动主程序
def main():
    global roundcount,randinsettings,roundname
    loadsettings()
    readStudents()
    if len(roundcount)==0:
        randinsettings=-1
        currentround["text"]="当前轮次：自由"
        currentroundprogress["text"]="0"
    else:
        currentround["text"]="当前轮次："+roundname[roundno-1]
        currentroundprogress["text"]="0/"+roundcount[roundno-1].split(":")[1]
    root.mainloop()

if __name__=='__main__':
    main()
import tkinter
import random
import threading
import time
import os
#初始化窗口
root=tkinter.Tk()
root.title("随机名单")
root.geometry('500x500+400+200')
root.resizable(False,False)
root.flag = True


#三个Lable标签
first = tkinter.Label(root,text='',font = ("宋体", 20,"normal"))
first.place(x=180,y=100,width=150,height=100)

second = tkinter.Label(root,text='',font = ("宋体", 20,"normal"))
second['fg'] = 'red'
second.place(x=180,y=200,width=150,height=100)

third = tkinter.Label(root,text='',font = ("宋体", 20,"normal"))
third.place(x=180,y=300,width=150,height=100)
#定义抽奖i
i=-1

students=['杨姐姐1','杨姐姐2','杨姐姐3','杨姐姐4','杨姐姐5','杨姐姐6']
studentsin=[]

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
    f=open('../lottery/cjq/list.txt','rb')
    for line in f:
        students.append(line.decode().replace("\r\n",""))
    print(students)


#开始按钮
def butStartClick():
    t=threading.Thread(target=switch)
    t.start()
btnStart=tkinter.Button(root,text='开始',command=butStartClick)
btnStart.place(x=30, y=30, width=80, height=20)

#结束按钮
def btnStopClick():
    global i
    root.flag=False
    studentsin.append(students[i])
    students.remove(students[i])
    print(studentsin)

def nextRound():
    global studentsin,i
    readStudents()
    studentsin=[]
    i=-1  
    
butStop=tkinter.Button(root,text='停止',command=btnStopClick)
butStop.place(x=160, y=30, width=80, height=20)
butNext=tkinter.Button(root,text="下一轮",command=nextRound)
butNext.place(x=310,y=30,width=80,height=20)
#启动主程序
readStudents()
root.mainloop()
import os
import tkinter as tk
from tkinter import ttk
import random
class drawsettings():
    def __init__(self):
        self.root=tk.Tk()
        self.root.title("随机抽取设置")
        self.root.geometry('500x400+400+200')
        #self.root=tk.TK()
        #self.tvgrid=ttk.Treeview(self,show="headings",height=18,columns="轮次,抽取人数,轮次显示名称,同时抽取人数")
        #self.frame_left=tk.Frame(self.root,width=400,height=200)
        #self.frame_right=tk.Frame(self.root,width=200,height=200)
        self.tvgrid=ttk.Treeview(self.root,show="headings",height=18,columns=("轮次","抽取人数","同时抽取人数","轮次显示名称"))
        self.tvgrid.place(x=0,y=0)
        self.tvgrid.bind("<Double-1>",self.set_cell_value)
        self.lbl=ttk.Checkbutton(self.root,text="下一轮是否重置")
        self.lbl.place(x=350,y=20)
        self.addrow=tk.Button(self.root,text="增行",command=self.addNewrow)
        self.addrow.place(x=350,y=50,width=80,height=20)
        self.delrow=tk.Button(self.root,text="删行",command=self.delRow)
        self.delrow.place(x=350,y=80,width=80,height=20)
        self.savebutton=tk.Button(self.root,text="保存",command=self.savesettings)
        self.savebutton.place(x=350,y=120,width=80,height=20)

    def addNewrow(self):
        x=self.tvgrid.get_children()
        if(len(x)>0):
            item=x[len(x)-1]
            txts=self.tvgrid.item(item,"values")
            newid=eval(txts[0])+1
            self.tvgrid.insert("","end",values=newid)
        else:
            self.tvgrid.insert("","end",values=1)
    
    def delRow(self):
        x=self.tvgrid.get_children()
        if(len(x)>0):
            self.tvgrid.delete(x[len(x)-1])

    def loadsettings(self):
        #从配置文件中获取配置
        #返回轮数-人数,轮次名称,每轮结束是否重置,每次抽取人数       
        rounds=[]   #轮次和人数
        roundsname=[]   #轮次显示名称
        roundreset=1    #每轮重置
        randomnum=[]   #每次抽取人数
        with open("settings.txt",'rb') as f:
            for line in f:
                str=line.decode("utf-8").replace("\r\n","")
                if self.startwith(str,"#"):
                    continue
                if self.startwith(str,"roundcount"):
                    setting=str.split('=')[1]
                    if setting:
                        rounds=setting.split(',')
                if self.startwith(str,"roundname"):
                    setting=str.split("=")[1]
                    if setting:
                        roundsname=setting.split(",")
                if self.startwith(str,"randomnum"):
                    setting=str.split('=')[1]
                    if setting:
                        setting=setting.split(',')
                        for num in setting:
                            randomnum.append(eval(num))
                if self.startwith(str,"roundreset"):
                    setting=str.split("=")[1]
                    if setting:
                        roundreset=eval(setting)
                    else:
                        roundreset=0
        return rounds,roundsname,roundreset,randomnum
    
    def set_cell_value(self,event):
        for item in self.tvgrid.selection():
            item_text=self.tvgrid.item(item,"values")
        column=self.tvgrid.identify_column(event.x)
        row=self.tvgrid.identify_row(event.y)
        cn=int(str(column).replace("#",""))
        if cn==0:
            return
        rn=int(str(row).replace("I",""))
        entryedit=tk.Text(self.root,width=10+(cn-1)*16,height=1)
        padx=0
        if cn==2:
            padx=50
        elif cn==3:
            padx=130
        else:
            padx=230
        txtwidth=80 if cn==2 else 100
        entryedit.place(x=6+padx,y=6+rn*20,width=txtwidth)
        def saveedit():
            self.tvgrid.set(item,column=column,value=entryedit.get(0.0,"end"))
            entryedit.destroy()
            okb.destroy()
        okb=ttk.Button(self.root,text="OK",width=4,command=saveedit)
        okb.place(x=padx+txtwidth+10,y=6+rn*20,width=40,height=25)



    def readfromform(self):
        #读取grid
        x=self.tvgrid.get_children()
        rounds=[]   #轮次和人数
        roundsname=[]   #轮次显示名称
        roundreset=0    #每轮重置
        randomnum=[]   #每次抽取人数
        if(len(x)>0):
            for i in range(len(x)):
                rounds.append(str(i)+":"+x[i][1])
                roundsname.append(x[i][3])
                randomnum.append(x[i][2])
        roundreset=1 if self.lbl.selected else 0
        return rounds,roundsname,roundreset,randomnum
    
    def writeform(self):
        self.tvgrid.column("轮次",width=50,anchor="center")
        self.tvgrid.column("抽取人数",width=80,anchor="se")
        self.tvgrid.column("同时抽取人数",width=100,anchor="se")
        self.tvgrid.column("轮次显示名称",width=100,anchor="e")
        self.tvgrid.heading("轮次",text="轮次")
        self.tvgrid.heading("抽取人数",text="抽取人数")
        self.tvgrid.heading("同时抽取人数",text="每次抽取人数")
        self.tvgrid.heading("轮次显示名称",text="轮次显示名称")
        roundcount,roundname,roundreset,randomnum=self.loadsettings()
        for i in range(len(roundcount)):
            self.tvgrid.insert("","end",values=(roundcount[i].split(":")[0],\
            roundcount[i].split(":")[1],randomnum[i],roundname[i]))
        self.lbl.selected=False if roundreset==0 else True
        
        
    def savesettings(self):
        #将配置写入文件
        roundcount,roundname,roundreset,randomnum=self.readfromform()
        with open("settings.txt","w") as f:
            pass

    def reloadsettings(self):
        #放弃保存并重新加载
        pass

    def startwith(self,str,substr):
        #print(str,substr)
        if str[:len(substr)]==substr:
            return True
        else:
            return False

    def start(self):
        self.root.mainloop()
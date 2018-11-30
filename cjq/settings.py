import os
import tkinter as tk
from tkinter import ttk
import random
class drawsettings():
    def __init__(self):
        self.root=tk.Tk()
        self.root.title("随机抽取设置")
        #self.root=tk.TK()
        #self.tvgrid=ttk.Treeview(self,show="headings",height=18,columns="轮次,抽取人数,轮次显示名称,同时抽取人数")
        self.frame_left=tk.Frame(self.root,width=400,height=200)
        self.frame_right=tk.Frame(self.root,width=200,height=200)
        self.tvgrid=ttk.Treeview(self.frame_left,show="headings",height=18,columns=("轮次","抽取人数","同时抽取人数","轮次显示名称"))
        self.lbl=ttk.Checkbutton(self.frame_right,text="下一轮是否重置")
        self.addrow=tk.Button(self.frame_right,width=80,text="增行",height=20)
        self.addrow.place(x=10,y=20)
        self.delrow=tk.Button(self.frame_right,text="删行",width=80,height=20)
        self.delrow.place(x=90,y=20)
        self.savebutton=tk.Button(self.frame_right,text="保存",width=80,height=20)
        self.savebutton.place(x=100,y=40)
            
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
    
    def readfromform(self):
        pass
    
    def writeform(self):
        self.tvgrid.column("轮次",width=50,anchor="center")
        self.tvgrid.column("抽取人数",width=100,anchor="se")
        self.tvgrid.column("同时抽取人数",width=150,anchor="se")
        self.tvgrid.column("轮次显示名称",width=200,anchor="e")
        roundcount,roundname,roundreset,randomnum=self.loadsettings()
        for i in range(len(roundcount)):
            self.tvgrid.insert("","end",values=(roundcount[i].split(":")[0],\
            roundcount[i].split(":")[1],randomnum[i],roundname[i]))
        self.lbl.selected=False if roundreset==0 else True
        
    def savesettings(self):
        #将配置写入文件
        pass

    def reloadsettings(self):
        #放弃保存并重新加载
        pass

    def startwith(self,str,substr):
        print(str,substr)
        if str[:len(substr)]==substr:
            return True
        else:
            return False

    def start(self):
        self.root.mainloop()
import os
import tkinter as tk
from tkinter import ttk
import random
class drawsettings(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tvgrid=ttk.Treeview(self,show="headings",height=18,columns="轮次,抽取人数,轮次显示名称")

    
    def loadsettings(self):
        #从配置文件中获取配置
        #返回轮数-人数,轮次名称,每轮结束是否重置,每次抽取人数       
        rounds=[]   #轮次和人数
        roundsname=[]   #轮次显示名称
        roundreset=1    #每轮重置
        randomnum=1     #每次抽取人数
        with open("../lottery/lottery/cjq/settings.txt",'rb') as f:
            for line in f:
                str=line.decode(line).replace("\r\n","")
                if self.startwith(str,"roundcount"):
                    setting=str.split('=')[1]
                    if setting:
                        rounds=setting.split(',')
                                 
        return rounds,roundsname,roundreset,randomnum
    
    def readfromform(self):
        pass
    
    def writeform(self):
        pass
    
    def savesettings(self):
        #将配置写入文件
        pass

    def reloadsettings(self):
        #放弃保存并重新加载
        pass

    def startwith(self,str,substr):
        if str[:len(substr)-1]==substr:
            return True
        else:
            return False

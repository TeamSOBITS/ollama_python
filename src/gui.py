#!/usr/bin/env python3
#coding:utf-8
import os
import rospkg
import time
import ollama
import tkinter as Tkinter
from subprocess import Popen

class ModelDownloader():
    def __init__(self):
        Popen(["xterm", "-font", "r16", "-fg", "floralwhite", "-bg", "darkslateblue", "-e", "ollama", "serve"])
        time.sleep(1)
        self.tk = Tkinter.Tk()
        # 以下にモデルの一例を載せる．ここの一例以外のモデルを使いたい場合はREADMEを参照しながら以下のリストに追加してください．
        self.can_download_models_info = ["llama3", "llama2", "phi3", "llava", "qwen", "dbrx", "dolphin-mixtral", "llama2-chinese", "tinyllama", "openchat"]
        self.download_models_flag = []
        self.reset_models_info()
        rospack = rospkg.RosPack()
        self.iconfile = Tkinter.PhotoImage(file=rospack.get_path("ollama_python")+"/img/icon.png")
        self.tk.call('wm', 'iconphoto', self.tk._w, self.iconfile)
    
    def reset_models_info(self):
        models = ollama.list()
        if (models["models"] is not None):
            for m in self.can_download_models_info:
                self.download_models_flag += [False]
                for lm in models["models"]:
                    if (m == lm["name"].replace(":latest","")):
                        self.download_models_flag[-1] = True
                        break
            for lm in models["models"]:
                match_flag = False
                for m in self.can_download_models_info:
                    if (m == lm["name"].replace(":latest","")):
                        match_flag = True
                        break
                if not match_flag:
                    self.can_download_models_info += [lm["name"].replace(":latest","")]
                    self.download_models_flag += [True]
        else:
            for m in self.can_download_models_info:
                self.download_models_flag += [False]


    def create_gui(self):
        # GUI windowの大きさを定義する
        geometry_x = str(700)
        if (len(self.can_download_models_info) < 2):
            geometry_y = str(30 * 2)
        else:
            geometry_y = 30 * len(self.can_download_models_info)
        # "window width x window height + position right + position down"
        self.tk.geometry(("%sx%s+0+0")%(geometry_x, geometry_y))
        
        for i, container_info in enumerate(self.can_download_models_info):
            container_name = container_info
            
            # コンテナの実行中の場合は"restart"，"stop"，"exec"というボタンを表示させる
            if self.download_models_flag[i]:
                button = Tkinter.Button(self.tk, width=4, text="      ", command=self.button_clicked_callback("dummy" , i)).place(x=100, y=i*30)
                button = Tkinter.Button(self.tk, width=4, text="delete", command=self.button_clicked_callback("delete", i)).place(x=160, y=i*30)
                button = Tkinter.Button(self.tk, width=4, text="copy"  , command=self.button_clicked_callback("copy"  , i)).place(x=220, y=i*30)
                button = Tkinter.Button(self.tk, width=4, text="push"  , command=self.button_clicked_callback("push"  , i)).place(x=280, y=i*30)

            else:
                button = Tkinter.Button(self.tk, width=4, text="pull"  , command=self.button_clicked_callback("pull"  , i)).place(x=100, y=i*30)
                button = Tkinter.Button(self.tk, width=4, text="      ", command=self.button_clicked_callback("dummy" , i)).place(x=160, y=i*30)
                button = Tkinter.Button(self.tk, width=4, text="      ", command=self.button_clicked_callback("dummy" , i)).place(x=220, y=i*30)
                button = Tkinter.Button(self.tk, width=4, text="      ", command=self.button_clicked_callback("dummy" , i)).place(x=280, y=i*30)

            label = Tkinter.Label(text=container_name, font=("",15)).place(x=340, y=i*30)

	    #GUI再起動用のボタンを定義
        btn = Tkinter.Button(self.tk, width=3, text="refresh", command=self.refresh_gui)
        btn.place(x=0, y=0)
        
        #GUI停止用のボタンを定義
        btn = Tkinter.Button(self.tk, width=3, text="close", command=self.quit_gui)
        btn.place(x=0, y=30)

        self.tk.title("[Download] ollama models GUI")
        self.tk.mainloop()


    def button_clicked_callback(self, mode, id):
        def inner():
            if mode != "dummy":
                if mode == "delete":
                    ollama.delete(str(self.can_download_models_info[id]))
                elif mode == "copy":
                    ollama.copy(str(self.can_download_models_info[id]), str(os.environ.get("USER")) + "/" + str(self.can_download_models_info[id]))
                elif mode == "pull":
                    ollama.pull(str(self.can_download_models_info[id]))
                elif mode == "push":
                    ollama.push(str(self.can_download_models_info[id]))
                self.refresh_gui()
        return inner 


    def refresh_gui(self):
        self.can_download_models_info = []
        self.download_models_flag = []
        self.tk.quit()
        self.tk.destroy()
        self.__init__()
        self.create_gui()


    def quit_gui(self):
        self.tk.quit()
        self.tk.destroy()

   

def main():
    md = ModelDownloader()
    md.create_gui()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
#coding:utf-8
import rospy
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
        self.width = self.tk.winfo_screenwidth()
        self.height = self.tk.winfo_screenheight()
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
        geometry_x = 700
        if (len(self.can_download_models_info) < 2):
            geometry_y = 30 * 2
        else:
            geometry_y = 30 * len(self.can_download_models_info)
        # "window width x window height + position right + position down"
        self.tk.geometry(("%sx%s+%s+%s")%(str(geometry_x), str(geometry_y), str((self.width - geometry_x)//2), str((self.height - geometry_y)//2)))
        
        for i, container_info in enumerate(self.can_download_models_info):
            if self.download_models_flag[i]:
                Tkinter.Button(self.tk, width=9, text="delete"   , command=lambda i=i: self.button_clicked_callback("delete", i)).place(x=150, y=i*30)
                Tkinter.Button(self.tk, width=9, text="copy"     , command=lambda i=i: self.button_clicked_callback("copy"  , i)).place(x=250, y=i*30)
                Tkinter.Button(self.tk, width=9, text="push"     , command=lambda i=i: self.button_clicked_callback("push"  , i)).place(x=350, y=i*30)
            else:
                Tkinter.Button(self.tk, width=34, text="download", command=lambda i=i: self.button_clicked_callback("pull"  , i)).place(x=150, y=i*30)

            Tkinter.Label(text=container_info, font=("", 15)).place(x=460, y=i*30)

	    #GUI再起動用のボタンを定義
        btn = Tkinter.Button(self.tk, width=6, text="refresh", command=self.refresh_gui)
        btn.place(x=0, y=0)
        
        #GUI停止用のボタンを定義
        btn = Tkinter.Button(self.tk, width=6, text="close", command=self.quit_gui)
        btn.place(x=0, y=30)

        self.tk.title("[Download] ollama models GUI")
        self.tk.mainloop()


    def button_clicked_callback(self, mode, id):
        if mode != "dummy":
            if mode == "delete":
                ollama.delete(str(self.can_download_models_info[id]))
            elif mode == "copy":
                print("copy")
                ollama.copy(str(self.can_download_models_info[id]), str(os.environ.get("USER")) + "/" + str(self.can_download_models_info[id]))
                print("copy")
            elif mode == "pull":
                ollama.pull(str(self.can_download_models_info[id]))
            elif mode == "push":
                print("push")
                ollama.push(str(self.can_download_models_info[id]))
                print("push")
            self.refresh_gui()

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

    # def get_window_size():
    #     # ウィンドウを表示せずに作成する
    #     # self.tk.withdraw()
    #     # ウィンドウのサイズを取得する
    #     width = self.tk.winfo_screenwidth()
    #     height = self.tk.winfo_screenheight()
    #     return width, height



def main():
    rospy.init_node("model_downloader")
    md = ModelDownloader()
    md.create_gui()


if __name__ == "__main__":
    main()
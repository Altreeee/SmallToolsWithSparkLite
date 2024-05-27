import win32clipboard
import time

from machine_translation_python_demo import AssembleHeaderException,Url,sha256base64,parse_url,assemble_ws_auth_url

import requests
import base64
import json

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os


def get_clipboard_text():
    # 打开剪贴板
    win32clipboard.OpenClipboard()
    try:
        # 尝试获取剪贴板中的文本数据
        clipboard_text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    except TypeError:
        # 如果剪贴板中没有文本数据，则返回空字符串
        clipboard_text = ""
    # 关闭剪贴板
    win32clipboard.CloseClipboard()
    return clipboard_text

class CustomNotebook(ScrolledText):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def save_sentence(self):    
        self.sentence = self.get(1.0, "end-1c")
            
            
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Transapp")
        # 设置窗口大小
        self.geometry("600x500")
        # 设置窗口透明度
        #self.attributes("-alpha", 0.8)  # 设置透明度为 80%
        # 创建一个主框架
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.APPId = ""
        self.APISecret = ""
        self.APIKey = ""
        self.url = 'https://itrans.xf-yun.com/v1/its'

        self.request_url = assemble_ws_auth_url(self.url, "POST", self.APIKey, self.APISecret)
        self.headers = {'content-type': "application/json", 'host': 'itrans.xf-yun.com', 'app_id': self.APPId}
        
        

        # 默认显示一个欢迎界面
        self.show_ToTrans()

    def show_ToTrans(self):
        # 清除容器中的所有组件
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.text_widget = tk.Text(self.main_frame, wrap='word', height=10, width=50)
        self.text_widget.grid(row=0,column=0)


        # 添加一个变量来存储剪贴板的内容，以便进行比较  
        self.prev_clipboard_text = ""  
        # 设置一个定时器来定期检查剪贴板内容  
        self.check_clipboard_interval = 1000  # 每秒检查一次  
        self.check_clipboard()  # 启动检查


        '''self.TransStart()'''

    def TransStart(self):
        self.TEXT = self.current_clipboard_text
        self.body = {
            "header": {
                "app_id": self.APPId,
                "status": 3,
            },
            "parameter": {
                "its": {
                    "from": "en",
                    "to": "cn",
                    "result": {}
                }
            },
            "payload": {
                "input_data": {
                    "encoding": "utf8",
                    "status": 3,
                    "text": base64.b64encode(self.TEXT.encode("utf-8")).decode('utf-8')
                }
            }
        }
        self.response = requests.post(self.request_url, data=json.dumps(self.body), headers=self.headers)
        self.tempResult = json.loads(self.response.content.decode())
    
        decoded_result  = base64.b64decode(self.tempResult['payload']['result']['text']).decode()
        json_result = json.loads(decoded_result )
        self.long_text = json_result['trans_result']['dst']
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, self.long_text)

    '''def watch_clipboard(self,interval=1):
        last_clipboard_text = None
        while True:
            win32clipboard.OpenClipboard()
            try:
                clipboard_text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            except TypeError:
                clipboard_text = ""
            win32clipboard.CloseClipboard()
            if clipboard_text != last_clipboard_text:
                self.TransStart()
                last_clipboard_text = clipboard_text
            time.sleep(interval)'''
    
    def check_clipboard(self):  
        # 检查剪贴板内容  
        self.current_clipboard_text = get_clipboard_text()  
  
        # 如果剪贴板内容有变化，则更新文本组件（假设你有一个名为self.text的ScrolledText实例）  
        if self.current_clipboard_text != self.prev_clipboard_text:  
            self.prev_clipboard_text = self.current_clipboard_text  
            '''if hasattr(self, 'text'):  # 确保self.text存在  
                self.text_widget.delete(1.0, tk.END)  # 清除当前文本  
                self.text_widget.insert(tk.END, current_clipboard_text)  # 插入新的剪贴板内容  '''
            self.TransStart()
        # 设置下一次检查的时间  
        self.after(self.check_clipboard_interval, self.check_clipboard)  
  



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
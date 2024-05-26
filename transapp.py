'''
0，识别框选部分内容

1，统计字数
2，如果存在非汉字字符 -> 翻译
3，如果存在多个并列存在的名词，如用、或，分隔开的数字、物品、人名等时，统计这类名词的数量

'''

from machine_translation_python_demo import AssembleHeaderException,Url,sha256base64,parse_url,assemble_ws_auth_url

import requests
import base64
import json

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os


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
        self.custom_notebook = CustomNotebook(self.main_frame, width=30, height=10)
        self.custom_notebook.grid(row=0, column=0,columnspan=2,sticky="nsew")

        buttonOK = tk.Button(self.main_frame, text="翻译", command=self.TransStart)
        buttonOK.grid(row=1,column=0)
        
        self.text_widget = tk.Text(self.main_frame, wrap='word', height=10, width=50)
        self.text_widget.grid(row=2,column=0)

    def TransStart(self):
        self.custom_notebook.save_sentence()
        #输入的待翻译文字为 self.custom_notebook.sentence
        self.TEXT = self.custom_notebook.sentence

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

        # 打印响应以检查其实际结构
        #print(self.tempResult)
        #print('text字段Base64解码后=>' + base64.b64decode(self.tempResult['payload']['result']['text']).decode())
        
        decoded_result  = base64.b64decode(self.tempResult['payload']['result']['text']).decode()
        json_result = json.loads(decoded_result )
        self.long_text = json_result['trans_result']['dst']
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, self.long_text)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
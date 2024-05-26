from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

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

        #星火认知大模型Spark3.5 Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
        self.SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'
        #星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
        self.SPARKAI_APP_ID = ''
        self.SPARKAI_API_SECRET = ''
        self.SPARKAI_API_KEY = ''
        #星火认知大模型Spark3.5 Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
        self.SPARKAI_DOMAIN = 'general'

        self.spark = ChatSparkLLM(
            spark_api_url=self.SPARKAI_URL,
            spark_app_id=self.SPARKAI_APP_ID,
            spark_api_key=self.SPARKAI_API_KEY,
            spark_api_secret=self.SPARKAI_API_SECRET,
            spark_llm_domain=self.SPARKAI_DOMAIN,
            streaming=False,
        )

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


        self.messages = [ChatMessage(
            role="user",
            content='如果这句话中存在非中文的内容，则将这些内容翻译为中文,如果不存在，则忽略。如果存在多个并列的，被、或，分隔开的名词或数字，则统计这些名词或数字的数量。只回复我翻译过后的我说的全文和统计的名词数量，其余的都不要说，这是我的内容：'+self.TEXT
        )]

        handler = ChunkPrintHandler()
        a = self.spark.generate([self.messages], callbacks=[handler])
        print(a)
        generations = a.generations
        chat_generation = generations[0][0]
        text_content = chat_generation.text  # 提取text属性的内容  
        '''
        generations=[[ChatGeneration(text='你好！很高兴为您提供帮助。请问有什么问题我可以帮您解答吗？', 
        message=AIMessage(content='你好！很高兴为您提供帮助。请问有什么问题我可以帮您解答吗？'))]] 
        llm_output={'token_usage': {'question_tokens': 11, 'prompt_tokens': 11, 'completion_tokens': 16, 'total_tokens': 27}} 
        run=[RunInfo(run_id=UUID('c7f0deb0-7452-461f-84c3-86097a8709b1'))]
        '''
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, text_content)

        



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
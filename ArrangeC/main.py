import os
import json
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

from machine_translation_python_demo import AssembleHeaderException,Url,sha256base64,parse_url,assemble_ws_auth_url
import base64

import tkinter as tk
from tkinter import filedialog


def print_tree(root, prefix=""):
    # 获取目录下的所有文件和文件夹
    items = sorted(os.listdir(root))
    # 计算需要连接的项目数
    total_items = len(items)
    for index, item in enumerate(items):
        # 判断当前项目是否是最后一个项目
        connector = "└── " if index == total_items - 1 else "├── "
        print(prefix + connector + item)
        path = os.path.join(root, item)
        # 如果是文件夹，递归调用print_tree函数
        if os.path.isdir(path):
            extension = "    " if index == total_items - 1 else "│   "
            print_tree(path, prefix + extension)

def build_tree(root):
    tree = {"name": os.path.basename(root), "children": []}
    try:
        items = sorted(os.listdir(root))
        for item in items:
            path = os.path.join(root, item)
            if os.path.isdir(path):
                tree["children"].append(build_tree(path))
            else:
                tree["children"].append({"name": item})
    except PermissionError:
        pass  # 忽略没有权限的文件夹
    return tree

def save_tree_as_json(root, output_file):
    tree = build_tree(root)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tree, f, ensure_ascii=False, indent=4)


#星火认知大模型Spark3.5 Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = ''
SPARKAI_API_SECRET = ''
SPARKAI_API_KEY = ''
#星火认知大模型Spark3.5 Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'general'
spark = ChatSparkLLM(
    spark_api_url=SPARKAI_URL,
    spark_app_id=SPARKAI_APP_ID,
    spark_api_key=SPARKAI_API_KEY,
    spark_api_secret=SPARKAI_API_SECRET,
    spark_llm_domain=SPARKAI_DOMAIN,
    streaming=False,
)
def check(name):
    # 模拟检查器函数
    print(f"Checking: {name}")
    messages = [ChatMessage(
            role="user",
            content='这是我电脑C盘中的一个文件或文件夹的名称: '+name+'告诉我它是什么，如果你不知道的话，请回答: 未知文件。'
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    #print(a)
    generations = a.generations
    chat_generation = generations[0][0]
    text_content = chat_generation.text  # 提取text属性的内容  
    print(text_content)


def recursive_check(item):
    name = item['name']
    check(name)
    if 'children' in item:
        for child in item['children']:
            recursive_check(child)

def Traversal_from_JSON(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        recursive_check(data)

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        return folder_selected
    return None

def create_gui():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    folder_path = browse_folder()
    if folder_path:
        print(f"Selected directory: {folder_path}")
        return folder_path
    else:
        print("No directory selected.")
        return None









if __name__ == "__main__":
    # 替换为你想要打印的目录路径
    directory_name = create_gui()
    '''directory = "./"+ directory_name'''
    if directory_name:
        json_path = "directory_structure.json"
        save_tree_as_json(directory_name, json_path)
        Traversal_from_JSON(json_path)

        print(f"Directory structure saved to {json_path}")
        print(directory_name)
        print_tree(directory_name)
        input()

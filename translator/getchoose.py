import win32clipboard


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

# 调用函数获取剪贴板中的文本
clipboard_text = get_clipboard_text()
print("剪贴板中的文本内容是：", clipboard_text)


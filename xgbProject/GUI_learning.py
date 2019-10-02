# -*- coding: utf-8 -*-
# author:RiceMarch

import tkinter as tk
import tkinter.messagebox
from bs4 import BeautifulSoup
import requests
import re

# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('学工在线 修改工具')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('600x400')  # 这里的乘是小x

# 第4步，在图形界面上设定输入框控件entry框并放置
e = tk.Entry(window, show=None,width=70)  # 显示成明文形式
e.grid(row=1, column=1,padx=5, pady=2, ipadx=5, ipady=5)

def htmlget(urlget):
    global flag
    pattern = "https://www.nefu.edu.cn/info"
    pattern1 = "http://news.nefu.edu.cn/info"
    matchnefu = re.match(pattern, urlget)
    matchnews = re.match(pattern1,urlget)
    if matchnews is None and matchnefu is None:#判断是否为学校网站，如果不是返回-1
        flag = -1
        print("matchnews is None and matchnefu is None")
        return
    r = requests.get(urlget)
    r.encoding = "utf-8"
    demo = r.text  # 服务器返回响应
    soup = BeautifulSoup(demo, "html.parser")
    """
    demo 表示被解析的html格式的内容
    html.parser表示解析用的解析器
    <div class="show02" id="vsb_content">内部为通知公告和学术动态需要提取出的内容
    <div class="v_news_content"> 内部为新闻网所需要提取出的内容
    """
    if matchnefu is not None:#如果是学工动态或者通知公告
        foundHtml = soup.find(class_="show02")
        flag = 1
    elif matchnews is not None:#如果是新闻网
        foundHtml = soup.find(class_="v_news_content")
        flag = 2
    if foundHtml is None:
        flag = -1
        print("foundHtml is None")
        return
    return foundHtml.prettify()
def modifyHtml(htmlcode):#html修改
    pattern = re.compile(r'<p.*')#正则表达式
    pattern1 = re.compile(r'<table.*')#正则表达式查找表格头
    pattern2 = re.compile(r'</table.*')#正则表达式查找表格尾
    pattern3 = re.compile(r' <p.*\s*>.*\s*<img.*?\s*orisrc.*?\s*src="')#正则表达式查图片改大小
    pattern4 = re.compile(r'.*</p>')
    pattern5 = re.compile(r'vheight.*\s*')
    htmlcode = str(htmlcode)
    #进行正则表达式替换
    modifiedcode = re.sub(pattern,'<p style="text-align:justify;"><span style="font-size:14px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', htmlcode)
    modifiedcode = re.sub(pattern1,'<div align="center"><table cellpadding="0" cellspacing="0" width="600">',modifiedcode)
    modifiedcode = re.sub(pattern2,'</table></div>',modifiedcode)
    if flag == 2:
        modifiedcode = re.sub(pattern3,'<p style="text-align: center;"><img src="http://news.nefu.edu.cn',
                              modifiedcode)
    elif flag == 1:
        modifiedcode = re.sub(pattern3, '<p style="text-align: center;"><img src="https://www.nefu.edu.cn',
                              modifiedcode)
    modifiedcode = re.sub(pattern4, '</span></p>', modifiedcode)
    modifiedcode = re.sub(pattern5,' width="600" style="height:auto;"/>',modifiedcode)
    print(modifiedcode)
    return modifiedcode

# 第5步，定义两个触发事件时的函数insert_point和insert_end（注意：因为Python的执行顺序是从上往下，所以函数一定要放在按钮的上面）
def modify():  # 在鼠标焦点处插入输入内容

    var = e.get()
    temp = modifyHtml(htmlget(var))
    print(temp)
    if temp != "None":
        t.delete(0.0, tk.END)
        print("temp is not none")
        t.insert('insert',temp)
    else:
        tk.messagebox.showwarning(title='错误', message='输入网址存在错误，请重新输入')
    print(flag)


def show():
    tkinter.messagebox.showinfo(title='Tips', message="输入官网的地址即可将网页读取并且生成为代码形式，"
                                                    "将代码复制入学工在线平台减少机械化的工作量,值得注意"
                                                    "的是该自动生成代码会默认将每段前加载七个空格，所以在"
                                                    "复制完代码后请及时检查文章格式的正确性\n正确网页格式\nhttps://www.nefu.edu.cn/info/XXXX/XXXXX.htm\n"
                                    "http://news.nefu.edu.cn/info/XXXX/XXXXX.htm\n\n暂时无法读取微信同步内容，仅支持学校页\n复制完代码后请及时检查文章格式的正确性\n复制完代码后请及时检查文章格式的正确性")
    l = tk.Label(window, width=70, text="东北林业大学大学生网络发展中心 校园网络通讯站\nBeta V0.3 问题反馈:ricemarch@nefu.edu.cn")
    l.grid(row=6,column=1)

# 第6步，创建并放置两个按钮分别触发两种情况
b1 = tk.Button(window, text='修改',width=8, command=modify)
b1.grid(row=1, column=5,padx=5, pady=2, ipadx=5, ipady=5)
b2 = tk.Button(window, text='说明',width=8, command=show)
b2.grid(row=2, column=5,padx=5, pady=2, ipadx=5, ipady=5)

# 第7步，创建并放置一个多行文本框text用以显示，指定height=3为文本框是三个字符高度
t = tk.Text(window, height=23,width=70)
t.grid(row=2,column=1,padx=5, pady=2, ipadx=5, ipady=5)


# 第8步，主窗口循环显示
window.mainloop()
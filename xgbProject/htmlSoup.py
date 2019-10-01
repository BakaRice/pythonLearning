from bs4 import BeautifulSoup
import requests
import re
import os
'''测试用例

通知公告：'https://www.nefu.edu.cn/info/1003/10370.htm'
        'https://www.nefu.edu.cn/info/1003/10458.htm'
        'https://www.nefu.edu.cn/info/1003/10282.htm'复杂内容
学术动态：'https://www.nefu.edu.cn/info/1004/10476.htm'
新闻网：'http://news.nefu.edu.cn/info/1011/13626.htm'
'''
#
# HTML获取，传入url return 相对应的html代码文
#
def htmlget(urlget):
    print("输入网页地址为："+urlget+"\n"+"进行网站检测")
    pattern = "https://www.nefu.edu.cn/info"
    pattern1 = "http://news.nefu.edu.cn/info"
    matchnefu = re.match(pattern, urlget)
    matchnews = re.match(pattern1,urlget)
    if matchnews is None and matchnefu is None:#判断是否为学校网站，如果不是返回-1
        print("输入网址为非学校新闻内容页面，请确认使用https://头访问，并确认网址正确！")
        return -1
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
    global flag
    if matchnefu is not None:#如果是学工动态或者通知公告
        foundHtml = soup.find(class_="show02")
        flag = 1
    elif matchnews is not None:#如果是新闻网
        foundHtml = soup.find(class_="v_news_content")
        flag = 2
    if foundHtml is None:
        return -1
        flag = 0
    return foundHtml.prettify()

#
# 初始用户界面
#
def start():
    print('***********************************************************' + '\n'
          '            校园网络通讯站2019 学工在线平台服务工具         ' + '\n'
              '             v0.1 RiceMarch QQ:1079966197        ' + '\n'
              '说明：若输出-1则代表输入网站存在错误或存在其他错误       ' + '\n'
 '输入内容保存在当前目录下的输入“输出代码.txt”文件中，将文件打' +
          '\n'+'开后按下ctrl+A选中全文后复制，点击学工在线后台上传稿件页面的第' + '\n'+'一个按钮 {HTML代码}将复制内容粘贴后上传即可     ' + '\n'
          '***********************************************************' + '\n')

#
# 对html进行修改，每段前加七个空格，将表格自动居中并设置宽度为600
#
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


start()
#url = input("请输入网址内容:")
endcode = modifyHtml(htmlget('https://www.nefu.edu.cn/info/1003/10282.htm'))
print(flag)
f = open("输出代码.txt", mode="wb")
f.write(endcode.encode("utf-8"))
f.flush()
f.close()

os.system("pause")

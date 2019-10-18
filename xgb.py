
from bs4 import BeautifulSoup
import requests
filename = '数据爬出.doc'
f = open(filename, 'a', encoding='utf-8')
# 调用函数
f.writelines("通知公告"+'\n')
f.close()
for pages in range(1,25):
    resp = requests.get('https://xgb.nefu.edu.cn/index.php?m=Article&a=index&method=Notice&p='+str(pages))
    soup = BeautifulSoup(resp.text, 'lxml')
    alldiv = soup.find_all('a', class_='article_base_a')
    filename = '数据爬出.doc'
    f = open(filename, 'a', encoding='utf-8')
    for aa in alldiv:
        names = aa.get_text()+'\n'
        print('find_all():'+str(pages), names)
        f.writelines(names)
    f.close()
import requests
import csv
import time
import re
from bs4 import BeautifulSoup as Bs

url = "https://book.douban.com/tag/编程?start=0&type=S"
kv = {'user-agent': 'Mozilla/5.0'}
proxies = { "http": "http://39.71.43.214:8118", "https": "http://42.51.12.2:808" }

def getHtml(url):
    try:
        r = requests.get(url, headers=kv)
        r.encoding = "utf-8"
        r.raise_for_status()
        return r.text
    except:
        return "获取失败"

#使用bs4获得获得urls
def getItemUrls(resText):
    itemUrls = []
    soup = Bs(resText, 'lxml')
    tags = soup.find_all('a')
    for tag in tags:
        if ('title' in tag.attrs.keys()):
            itemUrls.append(tag.attrs['href'])
            # time.sleep(1)
    return itemUrls

#使用正则表达式获得内容
def dealItemUrls(itemUrls):
    for item in itemUrls:
        time.sleep(2)
        resText = getHtml(item)
        soup = Bs(resText, 'lxml')
        tag = soup.find(id="info")
        text = tag.text.replace(" ", "")
        #print(text)
        author = re.search('作者:\s*(.*?)出版社', text, re.S).group(1).replace('\n', "")
        publish = re.search('出版社:\s*(.*?)\s', text, re.S).group(1).replace('\n', "")

        secondTitle = re.search('原作名:?(.*)\s', text, re.S)
        if secondTitle:
            secondTitle = secondTitle.group(1)
        else:
            secondTitle = ""

        originName = re.search('原作名:?(.*)\s', text, re.S)
        if originName:
            originName = originName.group(1)
        else:
            originName = ""


        translator = re.search('译者:\s*(.*?)\s', text, re.S).group(1).replace('\n', "")
        publishYear = re.search('出版年:\s*(.*?)\s', text, re.S).group(1).replace('\n', "")
        pages = re.search('页数:\s*(.*?)\s', text, re.S).group(1).replace('\n', "")
        price = re.search('定价:\s*(.*?)\s', text, re.S).group(1).replace('\n', "")
        isbn = re.search('ISBN:\s*(.*)', text, re.S).group(1).replace('\n', "")
        print(author,"\n", publish, "\n",translator,"\n",publishYear,"\n",pages, "\n",price,"\n", isbn)
        print("---------------------------------")

items = getItemUrls(getHtml(url))
dealItemUrls(items)


# 写入csv保存
row = []
row.append("xiaohu")
row.append("12")
out = open("test.csv", "a", newline="")
csv_writer = csv.writer(out, dialect="excel")
csv_writer.writerow(row)
out.close()

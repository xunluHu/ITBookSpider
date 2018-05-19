import requests
import csv
import time
import re
from bs4 import BeautifulSoup as Bs

url = "https://book.douban.com/tag/编程?start={position}&type=S"
kv = {'user-agent': 'Mozilla/5.0'}
proxies = { "http": "http://39.71.43.214:8118", "https": "http://42.51.12.2:808" }
tableTitle = ["title", "author", "publish", "secondTitle", "originName", "translator", "publishYear", "Pages", "price", "ISBN"]
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
    return itemUrls

def dealReExpress(rematch, dict, index):
    if(rematch):
        dict[tableTitle[index]] = rematch.group(1).replace('\n', "")
        return rematch.group(1).replace('\n', "")
    else:
        dict[tableTitle[index]] = "无"
        return ""


#使用正则表达式获得内容
def dealItemUrls(itemUrls):
    contentArray = []
    for item in itemUrls:
        contentDict = {}
        time.sleep(2)
        resText = getHtml(item)
        soup = Bs(resText, 'lxml')
        tagTitle = soup.find("span", {"property": "v:itemreviewed"})
        title  = tagTitle.text
        contentDict[tableTitle[0]] = title
        tagBody = soup.find(id="info")
        text = tagBody.text.replace(" ", "")
        author = dealReExpress(re.search('作者:?\s*(.*?)出版社', text, re.S), contentDict, 1)
        publish = dealReExpress(re.search('出版社:?\s*(.*?)\s', text, re.S), contentDict, 2)
        secondTitle = dealReExpress(re.search('副标题:?\s*(.*?)\s', text, re.S), contentDict, 3)
        originName = dealReExpress(re.search('原作名:?\s*(.*?)\s', text, re.S), contentDict, 4)
        translator = dealReExpress(re.search('译者:?\s*(.*?)\s', text, re.S), contentDict, 5)
        publishYear = dealReExpress(re.search('出版年:?\s*(.*?)\s', text, re.S), contentDict, 6)
        pages = dealReExpress(re.search('页数:?\s*(.*?)\s', text, re.S), contentDict, 7)
        price = dealReExpress(re.search('定价:?\s*(.*?)\s', text, re.S), contentDict, 8)
        isbn = dealReExpress(re.search('ISBN:?\s*(.*)', text, re.S), contentDict, 9)
        print(title,"\n", author,"\n", publish, "\n",secondTitle,"\n",originName,"\n", translator,"\n",publishYear,"\n",pages, "\n",price,"\n", isbn)
        print("---------------------------------")
        contentArray.append(contentDict)
    return contentArray

# 写入csv保存
def writeIntoCsv(row):
    csv_writer = csv.writer(out, dialect="excel")
    csv_writer.writerow(row)

if __name__ =='__main__':
    out = open("ITBook.csv", "a", newline="")
    writeIntoCsv(tableTitle)
    for i in range(0, 980, 20):
        items = getItemUrls(getHtml(url.format(position=i)))
        contentArray = dealItemUrls(items)
        for item in contentArray:
            row = []
            for(k,v) in item.items():
                row.append(v)
            writeIntoCsv(row)

    out.close()


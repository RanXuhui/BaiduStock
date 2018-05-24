import requests
from bs4 import BeautifulSoup
import re
# import traceback

def getHTMLText(url, code='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ''

def getStockList(lst, stockURL):    # 获取股票的信息列表
    html = getHTMLText(stockURL, 'GB2312')
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')  # BeautifulSoup中是find_all
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r'[s][hz]\d{6}', href)[0])    # 正则中是findall
        except:
            continue

def getStockInfo(lst, stockURL, fpath): # 获得个股的股票信息
    count = 0

    for stock in lst:
        url = stockURL + stock + '.html'
        html = getHTMLText(url)
        try:
            if html == '':
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})

            name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
            infoDict.update({'股票名称': name.text.split()[0]})

            keylist = stockInfo.find_all('dt')
            valuelist = stockInfo.find_all('dd')
            for i in range(len(keylist)):
                keylist = keylist[i].text
                valuelist = valuelist[i].text
                infoDict.update({'keylist': 'valuelist'})


            with open(fpath, 'a', encoding='utf-8')as f:
                f.write(str(infoDict) + '\n')
                count = count + 1
                print('\r当前进度： {:.2f}%'.format(count*100/len(lst)), end="")
        except:
            # traceback.print_exc()
            count = count + 1
            # print("fail")
            print('\r当前进度： {:.2f}%'.format(count * 100 / len(lst)), end="")
            continue



def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_file = 'F:/Crawler/北理工爬虫网课/【第三周】网络爬虫之实战/单元9：实例3：股票数据定向爬虫/stock'
    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)

main()

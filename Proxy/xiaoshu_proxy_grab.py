import urllib.request
import chardet
import re
import _thread
import time
import ssl
import ProxySqlite
import datetime

ssl._create_default_https_context = ssl._create_unverified_context

xs_url = "http://www.xsdaili.cn/"
dest_url = "http://www.usatoday.com/"
dest_url2 = "http://sina.com//"
header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

def ShowRecord(type, ipAddr, port, useable, delayTime, createTime):
    print("socket type:%s, ip:%s:%s useable:%d delay:%d createTime:%s" % 
          type, ipAddr, port, useable, delayTime, createTime)

def check_proxy(type, ip, port):
    type = type.lower()
    ip_port = ip + ':' + port
    proxy_support = urllib.request.ProxyHandler({type: ip_port})
    opener = urllib.request.build_opener(proxy_support)

    try:
        request1 = urllib.request.Request(dest_url, headers=header)
        request2 = urllib.request.Request(dest_url2, headers=header)

        time_before = datetime.datetime.now()
        page = opener.open(request1)
        page_html = page.read()

        page = opener.open(request2)
        page_html = page.read()

        if page.status == 200:
            time_after = datetime.datetime.now()
            delayTime = time_after - time_before
            ProxySqlite.InsertProxyRecord(type, ip, int(port,10), delayTime.seconds, 1)

    except Exception as a:
        print(f"Unexpect error: { a }")


def get_one_day(day_url):
    page = urllib.request.urlopen(day_url)
    page_html = page.read()

    page_code = chardet.detect(page_html)
    html_data = page_html.decode(page_code["encoding"])

    reg = r'(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3})\b:(\d{2,5})@(HTTP)'
    reg_day = re.compile(reg)

    day_list = reg_day.findall(html_data)

    for x in day_list:
        ip = x[0]
        port = x[1]
        type = x[2]
        _thread.start_new_thread(check_proxy, (type, ip, port))
        time.sleep(0.1)


def get_one_month(month_url):
    page = urllib.request.urlopen(month_url)
    page_html = page.read()

    page_code = chardet.detect(page_html)
    html_data = page_html.decode(page_code["encoding"])

    reg = r'<a href="(.+?)">\d{4}年\d{1,2}月\d{1,2}日 今日国外最新HTTP代理IP</a>'
    reg_day = re.compile(reg)

    day_list = reg_day.findall(html_data)

    for x in day_list:
        url = xs_url + x
        print(url)
        get_one_day(url)


if __name__ == "__main__":
    ProxySqlite.CreateTable()

    page = urllib.request.urlopen(xs_url)
    page_html = page.read()

    page_code = chardet.detect(page_html)
    htmlData = page_html.decode(page_code["encoding"])

    pageFile = open('pageCode.txt', 'wb')
    pageFile.write(page_html)
    pageFile.close()

    reg = r'<a href="(.+?)" class="list-group-item  ">'
    reg_month = re.compile(reg)
    month_list = reg_month.findall(htmlData)

    for x in month_list:
        url = xs_url + x
        #print(url)
        get_one_month(url)

import urllib.request
import chardet
import re
import _thread
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

xs_url = "http://www.xsdaili.com"
dest_url = "https://www.usatoday.com/"
header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

def check_proxy(type, ip_port):
    proxy_support = urllib.request.ProxyHandler({type: ip_port})
    opener = urllib.request.build_opener(proxy_support)
    request = urllib.request.Request(dest_url, headers=header)

    try:
        time_before = time.time()
        page = opener.open(request)
        page_html = page.read()

        if page.status == 200:
            time_after = time.time()
            proxy_file = open("proxy_file.txt", "a+")
            data = {type: ip_port}
            str_out = '{:} usetime = {} \r\n'.format(data, time_after - time_before)

            proxy_file.write(str_out)
            proxy_file.close()

    except Exception as a:
        print(f"Unexpect error: { a }")


def get_one_day(day_url):
    page = urllib.request.urlopen(day_url)
    page_html = page.read()

    page_code = chardet.detect(page_html)
    html_data = page_html.decode(page_code["encoding"])

    reg = r'(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b:\d{2,5})@(HTTP)'
    reg_day = re.compile(reg)

    day_list = reg_day.findall(html_data)

    for x in day_list:
        type = x[1]
        ip_port = x[0]
        _thread.start_new_thread(check_proxy, (type, ip_port))
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

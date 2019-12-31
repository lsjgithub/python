import urllib.request
import chardet
import re
import os

'''
# 读取html
page = urllib.request.urlopen('http://www.meituba.com/tag/juesemeinv.html')
htmlCode = page.read()

# 检测html的编码
pageCode = chardet.detect(htmlCode)
print("pageCode:", pageCode)

# 获取html 数据
data = htmlCode.decode(pageCode['encoding'])

# 写入文件
pageFile = open('pageCode.txt', 'wb')
pageFile.write(htmlCode)
pageFile.close()
'''


# 遍历网页上的链接
def traverse_page(html_data, reg_code, reg_url, reg_type):
    reg_item = re.compile(reg_code)
    url_list = reg_item.findall(html_data)

    for url_item in url_list:
        url = re.search(reg_url, url_item)
        if url:
            url_type = re.search(reg_type, url_item)
            if url_type:
                download_one_page(url[0], url_type.group(1))


# 下载一个页面上的图片
def download_one_page(url, type_name):
    html_page = urllib.request.urlopen(url)
    html_code = html_page.read()
    page_code = chardet.detect(html_code)
    html_data = html_code.decode(page_code['encoding'])

    # 正则表达式匹配图片链接
    reg = r'src="(.+?\.jpg)"'
    reg_img = re.compile(reg)
    img_list = reg_img.findall(html_data)  # 正则表达式进行查找

    x = 0
    for img in img_list:
        print(img)
        filename = type_name
        is_exists = os.path.exists(type_name)
        if not is_exists:
            os.makedirs(type_name)
        filename += ('/%s.jpg' % x)
        try:
            urllib.request.urlretrieve(img, filename)
        finally:
            print("urlretrieve error")
        x += 1


page = urllib.request.urlopen('http://www.meituba.com/tag/')
htmlCode = page.read()

pageCode = chardet.detect(htmlCode)

htmlData = htmlCode.decode(pageCode['encoding'])

regItem = r'(<a href="http://www.meituba.com/tag/.+?\.html" target="_blank">.+?</a>)'
regUrl = r'http://www.meituba.com/tag/.+?\.html'
regType = r'>(.+?)<'

traverse_page(htmlData, regItem, regUrl, regType)


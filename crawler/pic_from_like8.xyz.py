import urllib.request
import re
import chardet
import os

url = 'http://www.like8.xyz'
headers = ("user-agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")

# 创建一个 opener
opener = urllib.request.build_opener()

# 添加 opener
opener.addheaders = [headers]

# 安装全局的 opener
urllib.request.install_opener(opener)

page = urllib.request.urlopen(url)
htmlPage = page.read()

htmlCode = chardet.detect(htmlPage)

htmlData = htmlPage.decode(htmlCode['encoding'])

print(htmlData)

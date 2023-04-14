from datetime import datetime
import scrapy
from spider.items import SpiderItem
import sys
import io
import re
import io
import chardet
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class GetSpider(scrapy.Spider):
    name = 'getspider'
    allowed_domains = 'https://a86666666.net/pc/home'
    start_urls = ['https://a86666666.net/pc/home' ] # 爬取的目标网址

    def parse(self, response):
        item = SpiderItem()
        url = 'https://a86666666.net/pc/home'
        # 配置浏览器选项
        capabilities = DesiredCapabilities.EDGE.copy()
        capabilities['ms:edgeOptions'] = {
            'binary': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            'args': ['--headless']  # 添加其他选项
        }

        # 实例化WebDriver对象
        driver = webdriver.Edge(executable_path=r'C:\Users\LiuAijing\Desktop\edgedriver_win64\msedgedriver.exe',
                                capabilities=capabilities)
        # 打开要访问的网页
        driver.get(url)

        # 等待动态加载内容出现
        wait = WebDriverWait(driver, 30)  # 增加等待时间
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "root"))
        )
        # 获取动态加载内容，并以utf-8编码输出

        dynamic_content = driver.find_element_by_id("root").get_attribute("innerHTML")
        byte_content = dynamic_content.encode('utf-8')
        print(chardet.detect(byte_content))
        decoded_content = byte_content.decode('utf-8')
        chinese_text = decoded_content.encode('utf-8').decode('utf-8')
        chinese = chinese_text.encode('utf-8')
        print(chinese)
        # 打开文件并写入字符串
        string = chinese.decode('utf-8')
        with open('1.txt', 'w', encoding='utf-8') as f:
            f.write(string)

        # 确认写入成功
        with open('1.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)

        # 读取文本文件
        with open('1.txt', encoding='utf-8') as f:
            text = f.read()

        # 从文本中提取UTF-8编码的文本
        utf8_text = re.findall(
            r'[\x00-\x7F\xC0-\xDF][\x80-\xBF]*|[\xE0-\xEF][\x80-\xBF]{2}|\xF0[\x90-\xBF][\x80-\xBF]|\xF1[\x80-\xBF]{2}|\xF2[\x80-\xBF]{2}|\xF3[\x80-\xBF]{2}|\xF4[\x80-\x8F]{2}',
            text)

        # 将UTF-8编码的文本转换为中文字符串
        with open('1.txt', 'r') as f:
            text = f.read()

        # 匹配中文字符
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        result = pattern.findall(text)

        # 输出提取的中文文本
        for item in result:
            print(item)

        # 爬取指定URL的页面内容
        response = requests.get(url)
        html_content = response.text

        # 解析HTML内容并提取所有内部链接
        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all('a')
        internal_links = []
        for link in links:
            href = link.get('href')
            if href and url in href:
                internal_links.append(href)

        # 输出所有内部链接
        print(internal_links)

        # 找出所有图片标签
        soup = BeautifulSoup(dynamic_content, 'html.parser')

        # Find all image tags in the HTML content
        img_tags = soup.find_all('img')
        # 输出所有图片的链接
        for img_tag in img_tags:
            print(img_tag['src'])
            response = requests.get(img_tag['src'])
            # 保存图片二进制数据到本地文件
            with open('image.jpg', 'wb') as f:
                f.write(response.content)

        print(response.body)
        article = html_content.sub("[A-Za-z0-9\,\。\<\>\"\=\.\|\-\!\:\?\(\)\;\[\]\{\}\ \'\_\\\/\+\#\&\^\*\%]", "",response.text)
        article = "".join(article.split())
        print(article)
        with open("1.txt", "w") as f:
            f.write(article)  # 自带文件关闭功能，不需要再写f.close()

        title = response.xpath('//ul[@class="vjs-styles-defaults"]/li[1]/h1/text()').extract_first()
        img = response.xpath('//ul[@class="vjs-styles-defaults"]/li[1]/h1/text()').extract_first()
        article1 = response.xpath('//div[@class="info2"]/div[1]/strong/text()').extract_first()
        article2 = response.xpath('//div[@class="info2"]/div[2]/strong/text()').extract_first()
        article3 = response.xpath('//div[@class="info2"]/div[3]/strong/text()').extract_first()
        article4 = response.xpath('//div[@class="info2"]/div[4]/strong/text()').extract_first()
        article = article1+article2+article3+article4

        # 格式化--列表转字符串
        item['title'] = ''.join(item['title'])
        item['img'] = ''.join(item['img'])
        item['article'] = ''.join(item['article'])

        # 关闭浏览器
        driver.quit()


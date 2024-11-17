# -*- coding: utf-8 -*-

#帶入套件
import requests
import json
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import re
import random
from bs4 import BeautifulSoup
import asyncio
import urllib.parse
import numpy as np
import json
from datetime import datetime

##輸入要爬取的查核標的和頁數
keyword = input("請輸入關鍵字")
num_pages = int(input("請輸入要爬取的頁數"))
ecode = 'utf-8-sig'

##需要存取的資料
#網址
product_links = []
#商品編號
product_ids = []
#品名
product_names = []
#商品描述
product_intros= []
#商品說明
product_dess= []
#商品規格
product_specs= []
#BSMI
bsmi_detect= []

#headers_home
my_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'accept-encoding': 'gzip, deflate, br, zstd',
'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
'sec-ch-ua': "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': "\"Windows\"",
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
'x-api-source': 'pc',
      }

# 關閉通知提醒
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu") 
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

# 開啟瀏覽器
driver = webdriver.Chrome(options=chrome_options)
#service=service
time.sleep(5)

# 開啟網頁
print('---------- 開始進行爬蟲 ----------')
#開始計時
tStart = time.time()

#目標網址
base_url = "https://24h.pchome.com.tw/search/?q=" + keyword
productp_page_url = "https://24h.pchome.com.tw"

    
#翻頁功能
for page in range(1, num_pages + 1):
    # 更新 URL，將頁碼傳入參數"p"
    url = f"{base_url}&p={page}"
    driver.get(url)
    time.sleep(10)  # 等待頁面完全加載

    # 解析當前頁面的 HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 爬取當前頁面的商品連結和編號
    for link_tag in soup.find_all("a", {"class": "c-prodInfoV2__link gtmClickV2"}):
        product_url = productp_page_url + link_tag.get("href")
        product_links.append(product_url)
        product_ids.append(link_tag.get("href").split("/")[-1])

    # 檢查是否有商品，若當前頁面無商品則跳出循環
    if not soup.find_all("a", {"class": "c-prodInfoV2__link gtmClickV2"}):
        print(f"第 {page} 頁無商品，停止爬取。")
        break

# print(product_links)
# print(product_ids)

for link in product_links:
    driver.get(link)
    time.sleep(2)  # 讓頁面完全載入

    # 解析商品頁面 HTML
    product_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # 根據商品頁面的 HTML 取所需的資訊
    # 品名
    product_name_tag = product_soup.find("h1", {"class": "o-prodMainName__grayDarkest o-prodMainName__grayDarkest--l700"})
    product_name = product_name_tag.text.strip() if product_name_tag else "未爬取到商品名稱"
    product_names.append(product_name)

    # 商品描述
    product_intro_tags_li = product_soup.find_all("li", {"class": "c-blockCombine__item c-blockCombine__item--prodSlogan"})
    product_intro_tags_div = product_soup.find_all("div", {"class": "c-blockCombine c-blockCombine--prodSlogan"})
    #https://24h.pchome.com.tw/prod/DYAO44-A900BWUGG
    product_intro_tags_divsm = product_soup.find_all("div", {"class": "c-blockCombine c-blockCombine--smProdSlogan"})
    #https://24h.pchome.com.tw/prod/DYAO46-A900A626T
    product_intro_tags_divgtm = product_soup.find_all("div", {"class": "c-blockCombine__info c-blockCombine__info--prodSlogan is-expanded gtmClickV2"})
    #
    product_intro_tags = product_intro_tags_li+product_intro_tags_div+product_intro_tags_divsm+product_intro_tags_divgtm
    product_intro = " ".join([tag.text.strip() for tag in product_intro_tags]) if product_intro_tags else "未爬取到商品描述"
    product_intros.append(product_intro)
    
    #商品說明找bsmi
    #商品說明
    product_des_tags = product_soup.find_all("div", {"class": "c-blockCombine__item c-blockCombine__item--prodFeatureInfo"})
    product_des = " ".join([tag.text.strip() for tag in product_des_tags]) if product_des_tags else "未爬取到商品說明"
    product_dess.append(product_des)
    
    #商品規格
    product_spec_tags_white = product_soup.find_all("div", {"class": "c-blockCombine__item c-blockCombine__item--prodSpecification"})
    product_spec_tags_gray = product_soup.find_all("div", {"class": "c-blockCombine c-blockCombine--gray"})
    product_spec_tags = product_spec_tags_white+product_spec_tags_gray
    product_spec = " ".join([tag.text.strip() for tag in product_spec_tags]) if product_spec_tags else "未爬取到商品規格"
    product_specs.append(product_spec)
    
    html_text = product_name+product_intro+product_des+product_spec   
    
    words = re.split(r"\W+",html_text)
    
    pattern = r'(M|R|D|T|Q)\s*\d{5}|(M|R|D|T|Q)\s*\d[A-Z]\d{3}|(M|R|D|T|Q)\d{2}[A-Za-z]\d{2}|(J)?C1\d{7}'
    matches = [word for word in words if re.match(pattern, word)]

    # 如果沒有找到符合條件的，則設為 "未爬取到BSMI資訊"
    if not matches:
        matches = "未爬取到BSMI資訊"

    bsmi_detect.append(matches)
    
    

# 關閉 WebDriver
driver.quit()
# print(len(product_names))
# print(len(product_dess))
# print(len(product_specs))
# print(len(product_intros))
# print(len(bsmi_detect))

#把已經有內容的各個存取點(列的形式)，轉成表格式存取方式
# PRODUCT = np.vstack((product_names,product_ids,product_links,product_intros,bsmi_detect))
# PRODUCT = pd.DataFrame(PRODUCT.T)
# # 把文字轉成excel可以讀的檔案，方便閱讀
# PRODUCT.columns = ["商品名稱" ,"商品編號","網址","商品敘述","是否有bsmi"]
PRODUCT = pd.DataFrame({
    "商品名稱": product_names,
    "商品編號": product_ids,
    "網址": product_links,
    "商品敘述": product_intros,
    "是否有bsmi": bsmi_detect
})

# 結束後顯示載了多少的商品(使用shape來看矩陣的大小)
print("下載了 {} 個商品".format(PRODUCT.shape[0]))  

# 取得當前日期和時間
current_time = datetime.now()
formatted_time = current_time.strftime("%y%m%d_%H%M")
NAME = f"{formatted_time}_Pchome_{keyword}.xlsx" 

# 移除非法字符，例如 ASCII < 32 的字元
def remove_illegal_chars(value):
    if isinstance(value, str):
        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', value)
    return value

PRODUCT = PRODUCT.applymap(remove_illegal_chars)
PRODUCT.to_excel(NAME, index=True)

#計時結束
tEnd = time.time()
totalTime = int(tEnd - tStart)
minute = totalTime // 60
second = totalTime % 60
print('資料儲存完成，花費時間（約）： ' + str(minute) + ' 分 ' + str(second) + '秒')



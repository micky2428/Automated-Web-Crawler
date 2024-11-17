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
import pandas as pd
import asyncio
import urllib.parse
import numpy as np
import json
from datetime import datetime

##爬取標的和頁數
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

#headers
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
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")  
#service=service
time.sleep(5)

# 開啟網頁
print('---------- 開始進行爬蟲 ----------')
tStart = time.time()#計時開始

#目標網址
base_url = "https://www.rakuten.com.tw/search/"+ keyword

#翻頁功能
for page in range(1, num_pages + 1):
    # 更新 URL，將頁碼傳入 `p` 參數
    url = f"{base_url}?p={page}"
    driver.get(url)
    time.sleep(10)  # 等待頁面完全加載

    # 滑動頁面並解析當前頁面的 HTML
    # driver.execute_script('window.scrollBy(0,1000)')
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 提取當前頁面的商品連結和編號
    for tag in soup.find_all(attrs={"data-rat-cp": True}):
        # 解析 data-rat-cp 的 JSON 內容
        data_rat_cp = tag.get("data-rat-cp")
        try:
            data_rat_cp_json = json.loads(data_rat_cp)  # 將屬性轉為字典
            dest = data_rat_cp_json.get("dest")  # 取得 dest 標籤中的值
            if dest:  
                product_links.append(dest)
            else:
                print(f"第 {page} 頁無商品，停止爬取。")
                break
            match = re.search(r"/product/([^/]+)/", dest)
            if match:
                product_id = match.group(1)
                if product_id not in product_ids:
                    product_ids.append(product_id)
        except json.JSONDecodeError:
            continue  # 如果 JSON 解析失敗，跳過該項目

    #等待一段時間以確保網站不會封鎖爬蟲
    time.sleep(2)
# print(product_links)
# print(product_ids)


for link in product_links:
    driver.get(link)
    time.sleep(5)  # 讓頁面完全載入

    # 解析商品頁面 HTML
    product_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # 根據商品頁面的 HTML 結構提取所需的資訊
    # 品名
    product_name_tag = product_soup.find("h1", {"class": "qa-ttl-main pPJjbyQzyGTssCo2kJ5p"})
    product_name = product_name_tag.text.strip() if product_name_tag else "未爬取到商品名稱"
    product_names.append(product_name)
   
    #商品說明找bsmi
    #商品說明(樂天這攔多是照片)
    product_des_tags = product_soup.find_all("div", {"class": "ZCr_EWi0bTYONI7QDz_j"})
    product_des = " ".join([tag.text.strip() for tag in product_des_tags]) if product_des_tags else "未爬取到商品說明"
    product_dess.append(product_des)
    
    #商品規格
    product_spec_tags = product_soup.find_all("div", {"class": "FJArRv00DQ_ahNG0nDRG"})
    product_spec = " ".join([tag.text.strip() for tag in product_spec_tags]) if product_spec_tags else "未爬取到商品規格"
    product_specs.append(product_spec)
    
    html_text = product_name+product_des+product_spec   
    
    words = re.split(r"\W+",html_text)
    
    pattern = r'(M|R|D|T|Q)\s*\d{5}|(M|R|D|T|Q)\s*\d[A-Z]\d{3}|(M|R|D|T|Q)\d{2}[A-Za-z]\d{2}|(J)?C1\d{7}'
    matches = [word for word in words if re.match(pattern, word)]

    # 如果沒有找到符合條件的匹配項，則設為 "未爬取到BSMI資訊"
    if not matches:
        matches = "未爬取到BSMI資訊"

    # 將結果附加到 bsmi_detect 清單中
    bsmi_detect.append(matches)
    
    

# 關閉 WebDriver
driver.quit()
# print(len(product_names))
# print(len(product_dess))
# print(len(product_specs))
# print(len(product_intros))
# print(len(bsmi_detect))

#把已經有內容的各個存取點(列的形式)，轉成表格式存取方式
PRODUCT = np.vstack((product_names,product_ids,product_links,product_specs,bsmi_detect))
PRODUCT = pd.DataFrame(PRODUCT.T)
# 把文字轉成excel可以讀的檔案，方便閱讀
PRODUCT.columns = ["商品名稱" ,"商品編號","網址","商品敘述","是否有bsmi"]

# 結束後顯示載了多少的商品(使用shape來看矩陣的大小)
print("下載了 {} 個商品".format(PRODUCT.shape[0]))  

# 取得當前日期和時間
current_time = datetime.now()
formatted_time = current_time.strftime("%y%m%d_%H%M")
NAME = f"{formatted_time}_rakuten_{keyword}.xlsx" 
PRODUCT.to_excel(NAME, index=True)
PRODUCT.to_excel(NAME)  # 將上面爬取的資訊存成.xlsx檔

#計時結束
tEnd = time.time()
totalTime = int(tEnd - tStart)
minute = totalTime // 60
second = totalTime % 60
print('資料儲存完成，花費時間（約）： ' + str(minute) + ' 分 ' + str(second) + '秒')




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

def crawl_pchome(keyword: str, num_pages: int):
    # 爬取的資料
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
    
    # 瀏覽器設定
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # 啟動瀏覽器
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(5)

    # 目標網址
    base_url = "https://24h.pchome.com.tw/search/?q=" + keyword
    product_page_url = "https://24h.pchome.com.tw"

    # 翻頁
    for page in range(1, num_pages + 1):
        url = f"{base_url}&p={page}"
        driver.get(url)
        time.sleep(10)  # 等待頁面加載

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 提取商品資訊
        for link_tag in soup.find_all("a", {"class": "c-prodInfoV2__link gtmClickV2"}):
            product_url = product_page_url + link_tag.get("href")
            product_links.append(product_url)
            product_ids.append(link_tag.get("href").split("/")[-1])

        # 檢查是否有商品
        if not soup.find_all("a", {"class": "c-prodInfoV2__link gtmClickV2"}):
            print(f"第 {page} 頁無商品，停止爬取。")
            break
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

    driver.quit()

    # 將數據轉為 DataFrame
    # PRODUCT = np.vstack((product_names, product_ids, product_links, product_intros, bsmi_detect))
    # PRODUCT = pd.DataFrame(PRODUCT.T, columns=["商品名稱", "商品編號", "網址", "商品敘述", "是否有bsmi"])
    PRODUCT = pd.DataFrame({
    "商品名稱": product_names,
    "商品編號": product_ids,
    "網址": product_links,
    "商品敘述": product_intros,
    "是否有bsmi": bsmi_detect
    })

    # 儲存為 Excel
    current_time = datetime.now().strftime("%y%m%d_%H%M")
    filename = f"{current_time}_Pchome_{keyword}.xlsx"

    # 移除非法字元
    def remove_illegal_chars(value):
        if isinstance(value, str):
            return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", value)
        return value

    PRODUCT = PRODUCT.applymap(remove_illegal_chars)
    PRODUCT.to_excel(filename, index=False)
    #print(f"已保存 {filename}")
import typing
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd


from shopData.schema.dataset import (
    check_schema,
)


import logging
logger = logging.getLogger(__name__)

def some_function():
    logger.info("執行操作")

def myheader():
    return {
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


def gen_task_paramter_list(
    keyword: str, num_pages: int
) -> typing.List[dict]:
    task_list = [
        {
            "keyword": keyword,  # 搜尋的關鍵字
            "num_pages": num_pages,  # 總頁數
            # "data_source": "PchomeData",  # 資料來源
        }
    ]
    return task_list


def initialize_browser():
    try:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.binary_location = "/usr/bin/google-chrome"
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument(f"--user-agent={myheader()['user-agent']}")
        # 設定 chromedriver 路徑
        # chromedriver_path = "/usr/local/bin/chromedriver"
        # service = Service(executable_path=chromedriver_path)
        # 初始化 WebDriver
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=chrome_options)
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error initializing browser: {e}")
        raise

def extract_text(tags):
    return " ".join([tag.text.strip() for tag in tags]) if tags else "未爬取到"

def remove_illegal_chars(value):
    if isinstance(value, str):
        return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", value)
    return value



def fetch_product_list(driver, base_url, num_pages):
    product_links, product_ids = [], []
    product_page_url = "https://24h.pchome.com.tw"

    for page in range(1, num_pages + 1):
        url = f"{base_url}&p={page}"
        driver.get(url)
        time.sleep(10)  # 等待頁面加載
        soup = BeautifulSoup(driver.page_source, "html.parser")

        links = soup.find_all("a", {"class": "c-prodInfoV2__link gtmClickV2"})
        if not links:
            print(f"第 {page} 頁無商品，停止爬取。")
            break

        for link_tag in links:
            product_links.append(product_page_url + link_tag.get("href"))
            product_ids.append(link_tag.get("href").split("/")[-1])

    return product_links, product_ids

def sanitize_string(input_string: str) -> str:
    return input_string.encode('utf-8', 'ignore').decode('utf-8')


def fetch_product_details(driver, product_links):
    product_names, product_intros, product_dess, product_specs, bsmi_detect = (
        [], [], [], [], []
    )

    for link in product_links:
        driver.get(link)
        time.sleep(2)  # 等待頁面完全載入
        product_soup = BeautifulSoup(driver.page_source, "html.parser")

        # 提取商品資訊
        product_name = extract_text(
            product_soup.find("h1", {"class": "o-prodMainName__grayDarkest o-prodMainName__grayDarkest--l700"})
        )
        # 清理商品名稱中的非法字符
        product_name = sanitize_string(product_name)
        product_names.append(product_name)

        # 商品描述
        intro_tags = (
            product_soup.find_all("li", {"class": "c-blockCombine__item c-blockCombine__item--prodSlogan"})
            + product_soup.find_all("div", {"class": "c-blockCombine c-blockCombine--prodSlogan"})
            + product_soup.find_all("div", {"class": "c-blockCombine c-blockCombine--smProdSlogan"})
            + product_soup.find_all("div", {"class": "c-blockCombine__info c-blockCombine__info--prodSlogan is-expanded gtmClickV2"})
        )
        intro_text = extract_text(intro_tags)
        # 清理商品描述中的非法字符
        intro_text = sanitize_string(intro_text)
        product_intros.append(intro_text)

        # 商品說明
        des_tags = product_soup.find_all(
            "div", {"class": "c-blockCombine__item c-blockCombine__item--prodFeatureInfo"}
        )
        des_text = extract_text(des_tags)
        # 清理商品說明中的非法字符
        des_text = sanitize_string(des_text)
        product_dess.append(des_text)

        # 商品規格
        spec_tags = (
            product_soup.find_all("div", {"class": "c-blockCombine__item c-blockCombine__item--prodSpecification"})
            + product_soup.find_all("div", {"class": "c-blockCombine c-blockCombine--gray"})
        )
        spec_text = extract_text(spec_tags)
        # 清理商品規格中的非法字符
        spec_text = sanitize_string(spec_text)
        product_specs.append(spec_text)

        # BSMI 檢測
        html_text = product_name + intro_text + des_text + spec_text
        words = re.split(r"\W+", html_text)
        pattern = r"(M|R|D|T|Q)\s*\d{5}|(M|R|D|T|Q)\s*\d[A-Z]\d{3}|(M|R|D|T|Q)\d{2}[A-Za-z]\d{2}|(J)?C1\d{7}"
        matches = [word for word in words if re.match(pattern, word)]
        bsmi_detect.append(", ".join(matches) if matches else "未爬取到BSMI資訊")

    return product_names, product_intros, product_dess, product_specs, bsmi_detect





# 爬蟲主函數
def crawler(keyword: str, num_pages: str) -> pd.DataFrame:
    driver = initialize_browser()
    base_url = f"https://24h.pchome.com.tw/search/?q={keyword}"
    try:
        # 爬取商品清單
        product_links, product_ids = fetch_product_list(driver, base_url, int(num_pages))

        # 爬取商品詳情
        (
            product_names,
            product_intros,
            product_dess,
            product_specs,
            bsmi_detect,
        ) = fetch_product_details(driver, product_links)

        # 組裝數據框
        inspectionDate = datetime.now().strftime("%Y-%m-%d")
        PRODUCT = pd.DataFrame(
            {
                "inspectionDate": [inspectionDate] * len(product_names),
                "number": list(range(1, len(product_names) + 1)),
                "productName": product_names,
                "productId": product_ids,
                "productLink": product_links,
                "productDescription": product_intros,
                "bsmiStatus": bsmi_detect,
            }
        )

        # 移除非法字元
        PRODUCT = PRODUCT.applymap(remove_illegal_chars)
        # PRODUCT = check_schema(PRODUCT.copy())
        PRODUCT = check_schema(PRODUCT.copy(), dataset="PchomeData")

        return PRODUCT

    finally:
        driver.quit()

#測試瀏覽器       
# if __name__ == "__main__":
#     driver = initialize_browser()
#     driver.get("https://www.google.com")
#     print(driver.title)
#     driver.quit()        


#地端成功:dataset.py沒問題
# if __name__ == "__main__":
#     keyword = "玩具"
#     num_pages = 1
#     try:
#         data = crawler(keyword, int(num_pages))
#         if not data.empty:
#             current_time = datetime.now()
#             formatted_time = current_time.strftime("%y%m%d_%H%M")
#             NAME = f"{formatted_time}_Pchome_{keyword}.xlsx"
#             data.to_excel(NAME, index=True)
#             print(f"資料已儲存至 {NAME}")
#         else:
#             print("未能成功爬取任何資料，請檢查日誌。")

#     except Exception as e:
#         print(f"主程式發生錯誤: {e}")

    

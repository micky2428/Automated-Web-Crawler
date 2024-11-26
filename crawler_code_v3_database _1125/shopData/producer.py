# AttributeError: module 'shopData.crawler.Pchome_Data' has no attribute 'gen_task_paramter_list'

import importlib
import sys

from loguru import logger

# crawler.delay(x=0)

from shopData.backend import db
from shopData.tasks.task import crawler
import pandas as pd
from datetime import datetime

import logging
# 設定logging 
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)


def Update(dataset: str, keyword: str, num_pages: str):
    # 爬蟲的參數列表
    parameter_list = getattr(
        importlib.import_module(f"shopData.crawler.{dataset}"),
        "gen_task_paramter_list",
    )(keyword=keyword, num_pages=num_pages)
    print(parameter_list)  # [{'keyword': '行動電源', 'num_pages': '1', 'data_source': 'PchomeData'}]
    
    for parameter in parameter_list:
        logger.info(f"處理爬取任務: {parameter}")
        try:
            # 提取必要參數
            data_source = parameter.get("data_source", "")

            # 爬取資料
            df = getattr(
                importlib.import_module(f"shopData.crawler.{dataset}"),
                "crawler",
            )(**parameter)
            logger.info(f"爬取任務完成，資料獲取成功: {parameter}")

            # 上傳資料
            db_dataset = dict(
                PchomeData="PchomeData",
            )
            table_name = db_dataset.get(dataset)
            if table_name:
                db.upload_data(df, table_name, db.router.mysql_shopData_conn)
                logger.info(f"資料成功上傳至資料庫: {dataset}")
            else:
                logger.error(f"無法找到對應的資料表: {dataset}")
                logger.error(f"資料上傳失敗: {e}")
                logger.error(f"出錯的數據: {df}")
        
        except Exception as e:
            logger.error(f"爬取或上傳任務失敗: {parameter}, 錯誤: {e}")
            
if __name__ == "__main__":
    dataset, keyword, num_pages = sys.argv[1:]
    # print(f"dataset: {dataset}, keyword: {keyword}, num_pages: {num_pages}")
    print(sys.argv) 
    Update(dataset, keyword, num_pages)



#未來加入分散式爬蟲

#     print(sys.argv) 
#     Update(dataset, keyword, num_pages)


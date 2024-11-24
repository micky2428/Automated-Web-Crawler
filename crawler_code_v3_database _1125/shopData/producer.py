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

# 設定基本的 logging 設定，這樣能顯示訊息
logging.basicConfig(level=logging.INFO)  # 也可以用 DEBUG、ERROR 等
logger = logging.getLogger(__name__)


def Update(dataset: str, keyword: str, num_pages: str):
    # 拿取爬蟲任務的參數列表
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
# def Update(dataset: str, keyword: str, num_pages: int):
#     # 拿取每個爬蟲任務的參數列表，
#     # 包含keyword查核標的(關鍵字)
#     # num_pages 爬取的頁數
#     # try:
#         parameter_list = getattr(
#             importlib.import_module(f"shopData.crawler.{dataset}"),
#             "gen_task_paramter_list",
#         )(keyword=keyword, num_pages=num_pages)
#         print(parameter_list) #[{'keyword': '行動電源', 'num_pages': '1', 'data_source': 'PchomeData'}]
#         for parameter in parameter_list:
#             logger.info(f"處理爬取任務: {parameter}")
#             try:
#                 # 提取必要參數
#                 keyword = parameter.get("keyword")
#                 num_pages = parameter.get("num_pages")
#                 data_source = parameter.get("data_source", "")
#                 print(dataset, parameter) #PchomeData {'keyword': '行動電源', 'num_pages': '1', 'data_source': 'PchomeData'}

#                 # 調用爬蟲任務
#                 task = crawler.s(dataset, parameter)   #task或傳遞具體參數 keyword, num_pages
#                 #task.apply_async(queue=data_source)

#                 logger.info(f"爬取任務成功排入隊列: {parameter}")
#             except Exception as e:
#                 logger.error(f"爬取任務失敗: {parameter}, 錯誤: {e}")
#     #     for parameter in parameter_list:
#     #         logger.info(f"{dataset}, {parameter_list}")
#     #         logger.info(f"爬取中... 關鍵字: {keyword}, 頁數: {num_pages}")
#     #         # task = crawler.s(dataset, parameter)
#     #         # # task.apply_async(queue=parameter.get("data_source", ""))
#     #         # task = crawler.s(parameter_list["keyword"], parameter_list["num_pages"])
#     #         # # queue 參數，可以指定要發送到特定 queue 列隊中
#     #         # task.apply_async(queue=parameter_list.get("data_source", ""))
#     #         try:
#     #             crawler(dataset, parameter)
#     #             logger.info(f"爬取完成並上傳: {keyword}, {num_pages}")
#     #         except Exception as e:
#     #             logger.error(f"爬取失敗: {e}")
#     # except Exception as e:
#     #     logger.error(f"更新過程中出現錯誤: {e}")
              
#         db.router.close_connection()

# if __name__ == "__main__":
#     dataset, keyword, num_pages = sys.argv[1:]
#     # print(f"dataset: {dataset}, keyword: {keyword}, num_pages: {num_pages}")
#     print(sys.argv) 
#     Update(dataset, keyword, num_pages)


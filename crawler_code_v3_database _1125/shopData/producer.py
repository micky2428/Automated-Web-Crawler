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


# def Update(dataset: str, keyword: str, num_pages: int): 地端測試
#     logger.info(f"Received dataset: {dataset}, keyword: {keyword}, num_pages: {num_pages}")
    
#     # 確保 dataset 是有效的模組名稱，例如 'PchomeData'
#     try:
#         module = importlib.import_module(f"shopData.crawler.{dataset}")
#     except ModuleNotFoundError as e:
#         logger.error(f"Module '{dataset}' not found: {e}")
#         return
    
#     # 拿取爬蟲任務的參數列表
#     parameter_list = module.gen_task_paramter_list(keyword=keyword, num_pages=num_pages)

#     for parameter in parameter_list:
#         logger.info(f"{dataset}, {parameter}")
#         data = crawler(parameter["keyword"], parameter["num_pages"])  # 這裡應該獲得爬取的資料
#         # 保存爬取的資料到 Excel 或其他地方
#         current_time = datetime.now()
#         formatted_time = current_time.strftime("%y%m%d_%H%M")
#         file_name = f"{formatted_time}_Pchome_{parameter['keyword']}.xlsx"
#         data.to_excel(file_name, index=True)
#         logger.info(f"爬取完成: {data.shape[0]} 筆資料")

#     db.router.close_connection()

# def Update(dataset: str, keyword: str, num_pages: int):
#     # 拿取每個爬蟲任務的參數列表，
#     # 包含爬蟲資料的日期 date，例如 2021-04-10 的台股股價，
#     # 資料來源 data_source，例如 twse 證交所、tpex 櫃買中心
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

crawler
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
                # 可添加其他資料表映射
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
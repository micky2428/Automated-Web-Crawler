import importlib
import typing
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from shopData.backend import db
from shopData.tasks.worker import (app,)

# # 註冊 task, 有註冊的 task 才可以變成任務發送給 rabbitmq
@app.task()
def crawler(dataset: str, parameter: typing.Dict[str, typing.Any]): #[{'keyword': '行動電源', 'num_pages': '1', 'data_source': 'PchomeData'}]
    # 使用 getattr, importlib,
    # 根據不同 dataset, 使用相對應的 crawler 收集資料
    # 爬蟲
    df = getattr(
        importlib.import_module(f"shopData.crawler.{dataset}"),
        "crawler",
    )(parameter=parameter)
    # 上傳資料庫
    db_dataset = dict(
        PchomeData="PchomeData",
        # Buy123_Data="Buy123Data",
        # Rakuten_Data="RakutenData",   
    )
    try:
        # 假設 db.upload_data 可以將資料上傳到指定資料庫
        db.upload_data(df, db_dataset.get(dataset), db.router.mysql_shopData_conn)
        logger.info(f"資料成功上傳至資料庫: {dataset}")
    except Exception as e:
        logger.error(f"資料上傳失敗: {e}")

# # 註冊 task, 有註冊的 task 才可以變成任務發送給 rabbitmq
# @app.task()
# def crawler(x):
#     print("crawler")
#     print("upload db")
#     return x
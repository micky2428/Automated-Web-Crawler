"""pip install SQLAlchemy"""
from sqlalchemy import create_engine,engine

from shopData.config import (
    MYSQL_DATA_USER,
    MYSQL_DATA_PASSWORD,
    MYSQL_DATA_HOST,
    MYSQL_DATA_PORT,
    MYSQL_DATA_DATABASE,
)
from sqlalchemy import create_engine, engine
import logging

# 設定 logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_mysql_shopData_conn() -> engine.base.Connection:
    address = (
        f"mysql+pymysql://{MYSQL_DATA_USER}:{MYSQL_DATA_PASSWORD}"
        f"@{MYSQL_DATA_HOST}:{MYSQL_DATA_PORT}/{MYSQL_DATA_DATABASE}"
    )
    engine = create_engine(address)
    connect = engine.connect()
    # return connect
    try:
        # 建立資料庫引擎並嘗試連線
        engine = create_engine(address)
        connect = engine.connect()
        logger.info("成功連線至資料庫!")
        logger.info(f"連線至資料庫: {MYSQL_DATA_DATABASE}")
        result = connect.execute("SHOW TABLES;")
        tables = result.fetchall()
        logger.info(f"資料庫中的表格: {tables}")
        return connect
    except Exception as e:
        # 連線失敗，記錄錯誤
        logger.error(f"資料庫連線失敗: {e}")
        return None
    
conn = get_mysql_shopData_conn()
if conn:
    # 如果連線成功，可以繼續執行其他操作
    print("資料庫連線成功")
else:
    # 連線失敗時的處理
    print("資料庫連線失敗")



#測試插入資料
# def insert_data():
#     # 取得資料庫連接
#     connection = get_mysql_shopData_conn()

#     # 插入一筆資料
#     try:
#         insert_query = """
#             INSERT INTO PchomeData (inspectionDate,number,productName,productId,productLink,productDescription,bsmiStatus) 
#             VALUES ('2024-01-01', 1,'test','test','test','test','test');
#         """
#         connection.execute(insert_query)
#         logger.info("資料插入成功")

#     except Exception as e:
#         logger.error(f"資料插入失敗: {e}")
    
#     # 確認插入資料後再關閉連線
#     connection.close()

# # 呼叫插入資料的函數
# insert_data()


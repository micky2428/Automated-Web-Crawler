from pydantic import BaseModel
import importlib
import pandas as pd
from datetime import date
import logging
logger = logging.getLogger(__name__)

class PchomeData(BaseModel):
    inspectionDate: date
    number: int
    productName: str
    productId: str
    productLink: str
    productDescription: str
    bsmiStatus: str


def check_schema(df: pd.DataFrame, dataset: str) -> pd.DataFrame:
    try:
        """檢查資料型態, 確保每次要上傳資料庫前, 型態正確"""
        df_dict = df.to_dict("records")
        schema = getattr(
            importlib.import_module("shopData.schema.dataset"),
            dataset,
        )
        df_schema = [schema(**dd).__dict__ for dd in df_dict]
        df = pd.DataFrame(df_schema)
        return df
    #新增錯誤偵測
    except AttributeError as e:
        logger.error(f"屬性錯誤：無法找到 schema 模組中的 {dataset} 定義。錯誤訊息：{e}")
        print(f"屬性錯誤：無法找到 {dataset} 的 schema 定義。請檢查該模組。")
        return pd.DataFrame()  # 返回空的 DataFrame，您可以根據需要調整處理方式
    
    except Exception as e:
        logger.error(f"發生錯誤：{e}")
        print(f"處理資料時發生錯誤：{e}")
        return pd.DataFrame()  


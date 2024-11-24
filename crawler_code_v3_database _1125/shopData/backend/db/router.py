import time
import typing

from loguru import logger
from sqlalchemy import engine

# from shopData import clients
# from . import clients
from shopData.backend.db import clients


def check_alive(
    connect: engine.base.Connection,
):
    """在每次使用之前，先確認 connect 是否活者"""
    connect.execute("SELECT 1 + 1")


def reconnect(
    connect_func: typing.Callable,
) -> engine.base.Connection:
    """如果連線斷掉，重新連線"""
    try:
        connect = connect_func()
    except Exception as e:
        logger.info(
            f"{connect_func.__name__} reconnect error {e}"
        )
    return connect


def check_connect_alive(
    connect: engine.base.Connection,
    connect_func: typing.Callable,
):
    if connect:
        try:
            check_alive(connect)
            return connect
        except Exception as e:
            logger.info(
                f"{connect_func.__name__} connect, error: {e}"
            )
            time.sleep(1)
            connect = reconnect(
                connect_func
            )
            return check_connect_alive(
                connect, connect_func
            )
    else:
        connect = reconnect(
            connect_func
        )
        return check_connect_alive(
            connect, connect_func
        )


class Router:
    def __init__(self):
        self._mysql_shopData_conn = (
            clients.get_mysql_shopData_conn()
        )

    def check_mysql_shopData_conn_alive(
        self,
    ):
        self._mysql_shopData_conn = check_connect_alive(
            self._mysql_shopData_conn,
            clients.get_mysql_shopData_conn,
        )
        return (
            self._mysql_shopData_conn
        )

    @property
    # def mysql_shopData_conn(self):
    #     """
    #     使用 property，在每次拿取 connect 時，
    #     都先經過 check alive 檢查 connect 是否活著
    #     """
    #     return (
    #         self.check_mysql_shopData_conn_alive()
    #     )
    def mysql_shopData_conn(self):
        """
        使用 property，在每次拿取 connect 時，
        都先經過 check alive 檢查 connect 是否活著。
        並處理可能的錯誤。
        """
        try:
            # 嘗試檢查連線是否仍然有效
            return self.check_mysql_shopData_conn_alive()
        except ConnectionError as e:
            # 當資料庫連線錯誤時，處理錯誤並記錄
            logger.error(f"資料庫連線錯誤: {str(e)}")
            raise RuntimeError("無法連接資料庫，請檢查資料庫狀態或設定。")
        except Exception as e:
            # 捕捉其他所有異常
            logger.error(f"發生未知錯誤: {str(e)}")
            raise RuntimeError("發生未知錯誤，請檢查程式或系統配置。")
        
        
    def close_connection(self):
        self._mysql_shopData_conn.close()
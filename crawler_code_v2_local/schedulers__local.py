from apscheduler.schedulers.background import BackgroundScheduler
import logging
import time
from crawl_pchome import crawl_pchome

# 設定 logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    scheduler = BackgroundScheduler(timezone="Asia/Taipei")

    # 每月 1 號凌晨 3 點執行一次爬蟲
    scheduler.add_job(
        id="pchome_crawler_task",
        func=crawl_pchome,
        trigger="cron",
        day=17,        # 每月第 17 天
        hour=22,       # 凌晨 11 點
        minute=11,
        args=["筆電", 1],  # 傳遞的參數：關鍵字和頁數
    )

    logger.info("Scheduler started.")
    scheduler.start()

    # 保持程式運行
    try:
        while True:
            time.sleep(600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    main()
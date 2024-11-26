
# 啟動 mysql
create-mysql:
	docker-compose -f mysql.yml up -d

# 啟動 rabbitmq
create-rabbitmq:
	docker-compose -f rabbitmq.yml up -d

# 安裝環境
install-python-env:
	pipenv sync

# sent task
sent-shop-data-task:
	pipenv run python shopData/producer.py PchomeData 玩具 1

# 建立 dev 環境變數
gen-dev-env-variable:
	python genenv.py

# 建立 staging 環境變數
gen-staging-env-variable:
	VERSION=STAGING python genenv.py

# 建立 release 環境變數
gen-release-env-variable:
	VERSION=RELEASE python genenv.py


#未來加入分散式爬蟲
# 啟動 celery, 執行 其他平臺 queue 的任務
run-celery-000:
	pipenv run celery -A shopData.tasks.worker worker --loglevel=info --concurrency=1  --hostname=%h -Q twse

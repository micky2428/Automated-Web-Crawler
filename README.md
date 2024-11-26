# Automated web crawler
The automated web crawling system is written in Python to crawl e-commerce platforms and obtain product information, assisting in inspection tasks more efficiently.

## Project Overview

The primary functionalities of the app include:

1. **Web Page Crawling**: Users can utilize the system to crawl information on e-commerce platforms, including product names, descriptions, and whether they have BSMI certification. The system supports multi-page crawling, allowing users to scrape information on multiple products at once.
2. **Database Storage**: The crawled data is stored in a MySQL database, where users can access it as needed.
3. **Data Retrieval via API**: Users can retrieve the data from the MySQL database through FastAPI endpoints.

## Purpose

The motivation behind developing this system is the annual need to inspect thousands of online products. With this crawler system, attention can be focused on potentially non-compliant products (i.e., those lacking BSMI information), significantly improving efficiency.

Initially, the system could only scrape 40 products and output the data as a .csv file for local storage. With the addition of cloud database integration, team members can now efficiently retrieve data from the central database.

## File Descriptions

1. **Makefile**: Contains common commands, such as starting the MySQL database.
2. **Pipfile**: Lists the required Python packages.
3. **Pipfile.lock**: Locks package versions to ensure consistent environments.
4. **create_table.sql**: Creates the PchomeData table in the MySQL database.
5. **genenv.py**: Generates the .env environment file and integrates with pipenv to eliminate the need for manual environment variable setup.
6. **local.ini**: Configures environment variables.
7. **mysql.yml**: Defines parameters for the MySQL database.
8. **setup.py**: Converts the shopData folder into a module for easy importing.
9. **rabbitmq.yml**: Configures parameters for RabbitMQ, which will be used for distributed crawling in the future.
10. **backend**: Contains files for database connections.
11. **crawler -PchomeData**: Crawls product data from PChome.
12. **schema -dataset**: Defines data types to ensure correctness when uploading data.
13. **task**: Stores files for future distributed crawling tasks.

## Design Considerations

**Storage Service**: During development, both MySQL and SQLite were considered. However, MySQL was chosen due to its ability to support remote access and centralized management, which SQLite lacks.

## Future Plans
Implement **distributed crawling** to make the system more efficient and less likely to be blocked.

## References

- [Python 大數據專案 X 工程 X 產品 資料工程師的升級攻略]([https://medium.com/@salman.alamoudi95/integrate-google-drive-for-backup-data-on-android-kotlin-jetpack-compose-e92cff32f71f](https://www.books.com.tw/products/0010964744?gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V9kp31s-cXkZO-qtA28irk0Ykx-GvBCYf7EC1SxKNe-ewxq3-1akl0aAhg2EALw_wcB)])

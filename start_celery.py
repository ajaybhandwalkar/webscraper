from celery_config import app
import celery_tasks
from database import create_db_and_tables


if __name__ == "__main__":
    create_db_and_tables()
    app.start()

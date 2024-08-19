import uuid
import json
from logger import init_logger
import urllib.request
from sqlalchemy.orm import Session
from datetime import date, datetime, UTC
from models import Task, LegitimateSeller
from models import TaskStatus
from database import local_session
from celery_config import app

logging = init_logger()


@app.task(name="scheduler")
def scheduler():
    db: Session = local_session()
    try:
        new_task = Task(
            run_id=str(uuid.uuid4()),
            date=date.today(),
            status=TaskStatus.SCHEDULED
        )
        db.add(new_task)
        db.commit()
        logging.info(f"run_id: {new_task.run_id}")
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to schedule new task: {e}")
    finally:
        db.close()


@app.task(name="executor")
def executor():
    db: Session = local_session()
    try:
        task = db.query(Task).filter_by(status=TaskStatus.SCHEDULED).first()
        if task:
            task.status = TaskStatus.STARTED
            task.started_at = datetime.now(UTC)
            db.commit()

            with open('sites.json') as fp:
                sites = json.load(fp)["sites"]

            for site in sites:
                url = f"https://{site}/ads.txt"
                try:
                    with urllib.request.urlopen(url) as response:
                        if response.getcode() == 200:
                            lines = response.read().decode('utf-8').splitlines()
                            lines = [line for line in lines if ',' in line]
                            for line in lines:
                                line = line.split(',')
                                ssp_domain_name = line[0]
                                publisher_id = line[1]
                                seller_relationship = line[2]
                                try:
                                    tag_id = line[3]
                                except:
                                    tag_id = ""
                                if tag_id:
                                    new_seller = LegitimateSeller(
                                        site=site,
                                        ssp_domain_name=ssp_domain_name,
                                        publisher_id=publisher_id,
                                        seller_relationship=seller_relationship,
                                        tag_id=tag_id,
                                        date=date.today(),
                                        run_id=task.run_id
                                    )
                                else:
                                    new_seller = LegitimateSeller(
                                        site=site,
                                        ssp_domain_name=ssp_domain_name,
                                        publisher_id=publisher_id,
                                        seller_relationship=seller_relationship,
                                        date=date.today(),
                                        run_id=task.run_id
                                    )
                                db.add(new_seller)
                except Exception as e:
                    logging.error(f"Encountered error for site {site}: {e}")
                    raise e

            db.commit()
            task.status = TaskStatus.FINISHED
            task.finished_at = datetime.now(UTC)
            logging.info(f"Task {task.run_id} Finished Successfully.")
        else:
            logging.info("No scheduled task found.")
    except Exception as e:
        if task and task.status == TaskStatus.STARTED:
            task.status = TaskStatus.FAILED
            task.failed_at = datetime.now(UTC)
            task.error = str(e)
            db.commit()
        logging.error(f"Failed to process the task: {e}")
    finally:
        try:
            db.commit()
        except Exception as e:
            logging.error(f"Failed to commit changes to the database: {e}")
        finally:
            db.close()


# scheduler()
# executor()

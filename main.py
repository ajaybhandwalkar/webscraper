import pdb
from fastapi import FastAPI, HTTPException, Depends, Query
from database import create_db_and_tables
from database import get_db
from sqlalchemy.orm import Session
from logger import init_logger
from models import Task, LegitimateSeller
from pydantic_model import TaskModel, LegitimateSellerModel, StatsResponseModel
from datetime import date
from typing import List, Optional

app = FastAPI()
create_db_and_tables()
logging = init_logger()



# @app.get("/tasks", response_model=list[TaskModel])
# async def get_tasks(db: Session = Depends(get_db)):
#     return db.query(Task).all()


@app.get("/tasks", response_model=List[TaskModel])
async def get_tasks_by_date(date: Optional[date] = Query(None), db: Session = Depends(get_db)):
    if date:
        return db.query(Task).filter(Task.date == date).all()
    return db.query(Task).all()


@app.get("/legitimate_sellers", response_model=List[LegitimateSellerModel])
async def get_legitimate_sellers_by_domain(domain: str, db: Session = Depends(get_db)):
    return db.query(LegitimateSeller).filter(LegitimateSeller.ssp_domain_name == domain).limit(10).all()


@app.get("/stats", response_model=StatsResponseModel)
async def get_stats(from_date: date, to_date: date, db: Session = Depends(get_db)):
    if from_date and to_date and from_date <= to_date:
        tasks = db.query(Task).filter(Task.date.between(from_date, to_date)).all()
        execution_times = [(task.finished_at - task.started_at).total_seconds() for task in tasks if
                           task.finished_at and task.started_at]
        if execution_times:
            return {"Average_Execution_Time": sum(execution_times) / len(execution_times)}

    return {"Average_Execution_Time": 0.0,
            "message": ["Check Dates format YYYY-MM-DD", "from_date should be less then to_date"]}

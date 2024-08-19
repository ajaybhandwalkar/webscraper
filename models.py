import uuid
from sqlalchemy import Column, String, Date, DateTime, Enum, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
import enum
from database import Base, create_db_and_tables


class TaskStatus(enum.Enum):
    SCHEDULED = 'SCHEDULED'
    STARTED = 'STARTED'
    FAILED = 'FAILED'
    FINISHED = 'FINISHED'


class Task(Base):
    __tablename__ = 'tasks'
    run_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(Date, default=lambda: date.today())
    status = Column(Enum(TaskStatus), default=TaskStatus.SCHEDULED)
    error = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    failed_at = Column(DateTime, nullable=True)
    legitimate_sellers = relationship('LegitimateSeller', back_populates='task')


class LegitimateSeller(Base):
    __tablename__ = 'legitimate_sellers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    site = Column(String(200))
    ssp_domain_name = Column(String(500))
    publisher_id = Column(String(500))
    seller_relationship = Column(String(500))
    tag_id = Column(String(500), nullable=True)
    date = Column(Date, default=lambda: date.today())
    run_id = Column(String(50), ForeignKey('tasks.run_id'))
    task = relationship('Task', back_populates='legitimate_sellers')


from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Date, BigInteger, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base

class Project(Base):
    __tablename__ = "tbl_projects"
    id = Column(Integer, primary_key=True)
    project_name = Column(String)
    status = Column(Enum("not_started", "in_progress", "on_hold", "completed", "reopened"))
    start_date = Column(Date)
    end_date = Column(Date)
    project_manager_id = Column(Integer, ForeignKey("users.id"))
    manager = relationship("User", foreign_keys=[project_manager_id])

class Phase(Base):
    __tablename__ = "tbl_phases"
    id = Column(Integer, primary_key=True)
    phase_name = Column(String)
    status = Column(Enum("not_started", "in_progress", "completed"))
    project_id = Column(Integer, ForeignKey("tbl_projects.id"))
    phase_manager_id = Column(Integer, ForeignKey("users.id"))

class Task(Base):
    __tablename__ = "tbl_tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(Enum("NOT_STARTED", "IN_PROGRESS", "COMPLETED"))
    estimated_budget = Column(BigInteger)
    actual_budget = Column(BigInteger)
    due_date = Column(Date)
    phase_id = Column(Integer, ForeignKey("tbl_phases.id"))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

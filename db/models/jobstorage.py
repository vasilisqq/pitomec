from db.database import Base
from sqlalchemy import Column,  Integer, String, DateTime, LargeBinary, CheckConstraint, PrimaryKeyConstraint

class JobStorage(Base):
    __tablename__ = 'apscheduler_jobs'

    # ID задания (тот, который вы задаете при add_job)
    id = Column(String(191), primary_key=True, nullable=False)
    
    # Время следующего запуска (Unix-время)
    next_run_time = Column(DateTime, nullable=False)
    
    # Бинарное состояние задания (функция, аргументы, триггер)
    # Используйте LargeBinary для PostgreSQL/SQLite
    job_state = Column(LargeBinary, nullable=False)
    
    # Дополнительные поля, которые могут быть добавлены в более новых версиях
    # или для совместимости с другими JobStore.
    # В минимальной версии достаточно id, next_run_time и job_state.

    # Для PostgreSQL/MySQL может потребоваться явное указание PrimaryKeyConstraint
    # __table_args__ = (
    #     PrimaryKeyConstraint('id'),
    # )
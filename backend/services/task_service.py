from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import json
from datetime import datetime

from backend.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from backend.cache.cache_service import cache_service


def json_serializer(obj):
    if isinstance(obj, (UUID, datetime)):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


class TaskService:

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: UUID) -> TaskRead:
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            user_id=user_id,
        )

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # invalidate cache
        cache_service.delete(f"user_tasks:{user_id}")

        return TaskRead.model_validate(db_task)

    @staticmethod
    def get_user_tasks(session: Session, user_id: UUID) -> List[TaskRead]:
        cache_key = f"user_tasks:{user_id}"

        cached = cache_service.get(cache_key)
        if cached:
            data = json.loads(cached)
            return [TaskRead(**item) for item in data]

        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()

        task_reads = [TaskRead.model_validate(task) for task in tasks]

        cache_service.set(
            cache_key,
            json.dumps(
                [task.model_dump() for task in task_reads],
                default=json_serializer,
            ),
            expire=600,
        )

        return task_reads

    @staticmethod
    def get_task_by_id(
        session: Session, task_id: UUID, user_id: UUID
    ) -> Optional[TaskRead]:

        cache_key = f"task:{task_id}:{user_id}"
        cached = cache_service.get(cache_key)

        if cached:
            return TaskRead(**json.loads(cached))

        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        task = session.exec(statement).first()

        if not task:
            return None

        task_read = TaskRead.model_validate(task)

        cache_service.set(
            cache_key,
            json.dumps(task_read.model_dump(), default=json_serializer),
            expire=600,
        )

        return task_read

    @staticmethod
    def update_task(
        session: Session,
        task_id: UUID,
        task_data: TaskUpdate,
        user_id: UUID,
    ) -> Optional[TaskRead]:

        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        task = session.exec(statement).first()

        if not task:
            return None

        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        cache_service.delete(f"task:{task_id}:{user_id}")
        cache_service.delete(f"user_tasks:{user_id}")

        return TaskRead.model_validate(task)

    @staticmethod
    def delete_task(session: Session, task_id: UUID, user_id: UUID) -> bool:
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        task = session.exec(statement).first()

        if not task:
            return False

        session.delete(task)
        session.commit()

        cache_service.delete(f"task:{task_id}:{user_id}")
        cache_service.delete(f"user_tasks:{user_id}")

        return True

    @staticmethod
    def toggle_task_completion(
        session: Session, task_id: UUID, user_id: UUID
    ) -> Optional[TaskRead]:

        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        task = session.exec(statement).first()

        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        cache_service.delete(f"task:{task_id}:{user_id}")
        cache_service.delete(f"user_tasks:{user_id}")

        return TaskRead.model_validate(task)

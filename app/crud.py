
from sqlalchemy.orm import Session

from app import models, schemas
from app.security import hash_password


# CREATE TASK
def create_task(
    db: Session,
    task: schemas.TaskCreate,
    user_id: int,
):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


# GET ONLY THE CURRENT USER'S TASKS
def get_tasks_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
):
    return (
        db.query(models.Task)
        .filter(models.Task.user_id == user_id)
        .order_by(models.Task.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# GET ONE TASK OWNED BY THE CURRENT USER
def get_task_by_id_and_user(
    db: Session,
    task_id: int,
    user_id: int,
):
    return (
        db.query(models.Task)
        .filter(
            models.Task.id == task_id,
            models.Task.user_id == user_id,
        )
        .first()
    )


# UPDATE THE CURRENT USER'S TASK
def update_task_for_user(
    db: Session,
    task_id: int,
    user_id: int,
    update_data: dict,
):
    db_task = get_task_by_id_and_user(
        db,
        task_id=task_id,
        user_id=user_id,
    )

    if db_task is None:
        return None

    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)

    return db_task


# DELETE THE CURRENT USER'S TASK
def delete_task_for_user(
    db: Session,
    task_id: int,
    user_id: int,
):
    db_task = get_task_by_id_and_user(
        db,
        task_id=task_id,
        user_id=user_id,
    )

    if db_task is None:
        return False

    db.delete(db_task)
    db.commit()

    return True


# FIND USER BY EMAIL
def get_user_by_email(
    db: Session,
    email: str,
):
    return (
        db.query(models.User)
        .filter(models.User.email == email.strip().lower())
        .first()
    )


# REGISTER USER
def create_user(
    db: Session,
    user: schemas.UserCreate,
):
    db_user = models.User(
        email=str(user.email).strip().lower(),
        hashed_password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

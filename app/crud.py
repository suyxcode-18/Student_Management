
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


# CREATE
def create_student(
    db: Session,
    student: schemas.StudentCreate
):
    db_student = models.Student(
        **student.model_dump()
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


# READ ALL
def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    statement = (
        select(models.Student)
        .order_by(models.Student.id)
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()


# READ BY ID
def get_student(db: Session, student_id: int):
    return db.get(models.Student, student_id)


# READ BY EMAIL
def get_student_by_email(db: Session, email: str):
    statement = select(models.Student).where(
        models.Student.email == email
    )

    return db.scalar(statement)


# UPDATE
def update_student(
    db: Session,
    student_id: int,
    student: schemas.StudentUpdate
):
    db_student = get_student(db, student_id)

    if db_student is None:
        return None

    for key, value in student.model_dump().items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)

    return db_student


# DELETE
def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)

    if db_student is None:
        return False

    db.delete(db_student)
    db.commit()

    return True

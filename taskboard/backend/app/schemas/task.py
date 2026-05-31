import sqlite3
from typing import List, Optional
import sys
from taskboard.backend.app.models.task import Task


class SqlTaskRepository:
    def __init__(self, database: str = "task_management_app"):
        self._db = database

    # ---------- CREATE ----------
    def create_task(self, category_id: int, title: str, position: int, comment: str, is_completed: bool,
                    due_date: str, created_at: str) -> Task:

        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO "task" (category_id, title, position, comment, is_completed, due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            category_id,
            title,
            position,
            comment,
            1 if is_completed is True else 0,
            due_date,
        ))
        conn.commit()
        new_task_id = cursor.lastrowid
        conn.close()

        return Task(task_id=new_task_id, category_id=category_id, title=title, position=position, comment=comment,
                    is_completed=is_completed, due_date=due_date, created_at=created_at)

    # ---------- READ ALL ----------
    def read_tasks(self) -> List[dict]:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM \"task\"")
        rows = cursor.fetchall()

        conn.close()

        tasks = [
            Task(
                task_id=row[0],
                category_id=row[1],
                title=row[2],
                position=row[3],
                comment=row[4],
                is_completed=row[5],
                due_date=row[6],
                created_at=row[7]
            ).as_dict()
            for row in rows
        ]

        return tasks

    # ---------- READ ONE ----------
    def read_task(self, id: int) -> Optional[Task]:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM \"task\" WHERE task_id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        task = Task(
            task_id=row[0],
            category_id=row[1],
            title=row[2],
            position=row[3],
            comment=row[4],
            is_completed=row[5],
            due_date=row[6],
            created_at=row[7]
        )

        return task

    # ---------- UPDATE -------------
    def update_task(
            self,
            task_id: int,
            category_id: int,
            title: str,
            position: int,
            comment: Optional[str] = None,
            is_completed: Optional[bool] = False,
            due_date: Optional[str] = None,
            created_at: Optional[str] = None
    ) -> Optional[Task]:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE task
            SET category_id=?,
                title = ?, 
                position = ?, 
                comment = ?, 
                is_completed = ?, 
                due_date = ?
            WHERE task_id = ?
        """, (
            category_id,
            title,
            position,
            comment,
            1 if is_completed is True else 0,
            due_date,
            task_id
        ))
        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return None

        conn.close()

        return Task(
            task_id=task_id,
            category_id=category_id,
            title=title,
            position=position,
            comment=comment,
            is_completed=is_completed,
            due_date=due_date,
            created_at=created_at
        )

    # ---------- DELETE ----------
    def delete_task(self, id: int) -> bool:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM \"task\" WHERE task_id = ?", (id,))
        conn.commit()

        conn.close()

        affected = cursor.rowcount or 0
        return affected > 0

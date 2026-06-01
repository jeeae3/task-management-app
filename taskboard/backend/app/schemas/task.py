import sqlite3
import json
from typing import List, Optional


class Task:
    def __init__(
            self,
            task_id: int,
            project_id: int,
            title: str,
            position: int,
            comment: str,
            status: str,
            priority: str,
            due_date: str,
            created_at: str
    ):
        self.task_id = task_id
        self.project_id = project_id
        self.title = title
        self.position = position
        self.comment = comment
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.created_at = created_at

        self._task = {
            "task_id": self.task_id,
            "project_id": self.project_id,
            "title": self.title,
            "position": self.position,
            "comment": self.comment,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date,
            "created_at": self.created_at
        }

    def as_dict(self):
        return self._task

    def __str__(self) -> str:
        json_task = json.dumps(self._task)
        return json_task


class SqlTaskRepository:
    def __init__(self, database: str = "task_management_app"):
        self._db = database

    # ---------- CREATE ----------
    def create_task(self, project_id: int, title: str, position: int, comment: str,
                    status: str, priority: str, due_date: str, created_at: str) -> Task:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO "task" (project_id, title, position, comment, status, priority, due_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (project_id, title, position, comment, status, priority, due_date, created_at))
        conn.commit()
        new_task_id = cursor.lastrowid
        conn.close()
        return Task(task_id=new_task_id, project_id=project_id, title=title, position=position,
                    comment=comment, status=status, priority=priority, due_date=due_date, created_at=created_at)

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
                project_id=row[1],
                title=row[2],
                position=row[3],
                comment=row[4],
                status=row[5],
                priority=row[6],
                due_date=row[7],
                created_at=row[8]
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
        return Task(
            task_id=row[0],
            project_id=row[1],
            title=row[2],
            position=row[3],
            comment=row[4],
            status=row[5],
            priority=row[6],
            due_date=row[7],
            created_at=row[8]
        )

    # ---------- UPDATE ----------
    def update_task(self, task_id: int, project_id: int, title: str, position: int,
                    comment: Optional[str] = None, status: Optional[str] = 'todo',
                    priority: Optional[str] = 'medium', due_date: Optional[str] = None,
                    created_at: Optional[str] = None) -> Optional[Task]:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE task
            SET project_id=?, title=?, position=?, comment=?, status=?, priority=?, due_date=?
            WHERE task_id=?
        """, (project_id, title, position, comment, status, priority, due_date, task_id))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return None
        conn.close()
        return Task(task_id=task_id, project_id=project_id, title=title, position=position,
                    comment=comment, status=status, priority=priority, due_date=due_date, created_at=created_at)

    # ---------- DELETE ----------
    def delete_task(self, id: int) -> bool:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM \"task\" WHERE task_id = ?", (id,))
        conn.commit()
        affected = cursor.rowcount or 0
        conn.close()
        return affected > 0
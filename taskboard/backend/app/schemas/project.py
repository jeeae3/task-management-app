import sqlite3
from typing import List, Optional
from models.project import Project


class SqlProjectRepository:
    def __init__(self, database: str = "task_management_app"):
        self._db = database

    # ---------- CREATE ----------
    def create_project(self, board_id: int, name: str, position: int) -> Project:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        cursor.execute("""
                    INSERT INTO "project" (board_id, name, position)
                    VALUES (?, ?, ?)
                """, (
            board_id,
            name,
            position,
        ))
        conn.commit()
        new_project_id = cursor.lastrowid
        conn.close()

        return Project(project_id=new_project_id, board_id=board_id, name=name, position=position)

    # ---------- READ ALL ----------
    def read_projects(self) -> List[dict]:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM \"project\"")
        rows = cursor.fetchall()

        conn.close()

        projects = [
            Project(
                project_id=row[0],
                board_id=row[1],
                name=row[2],
                position=row[3]
            ).as_dict()
            for row in rows
        ]

        return projects

    # ---------- READ ONE ----------
    def read_project(self, id: int) -> Optional[Project]:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM \"project\" WHERE project_id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        project = Project(
            project_id=row[0],
            board_id=row[1],
            name=row[2],
            position=row[3]
        )

        return project

        # ---------- UPDATE -------------
    def update_project(
            self,
            project_id: int,
            board_id: int,
            name: str,
            position: int
    ) -> Optional[Project]:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE project
            SET project_id=?,
                board_id = ?, 
                name = ?, 
                position = ?
            WHERE project_id = ?
        """, (
            project_id,
            board_id,
            name,
            position,
            project_id,
        ))
        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return None

        conn.close()

        return Project(
            project_id=project_id,
            board_id=board_id,
            name=name,
            position=position
        )

    # ---------- DELETE ----------
    def delete_project(self, id: int) -> bool:
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM \"project\" WHERE project_id = ?", (id,))
        conn.commit()

        conn.close()

        affected = cursor.rowcount or 0
        return affected > 0

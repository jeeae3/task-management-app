import json


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
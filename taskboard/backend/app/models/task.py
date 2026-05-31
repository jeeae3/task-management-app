import json


class Task:
    def __init__(
            self,
            task_id: int,
            category_id: int,
            title: str,
            position: int,
            comment: str,
            is_completed: bool,
            due_date: str,
            created_at: str
    ):
        self.task_id = task_id
        self.category_id = category_id
        self.title = title
        self.position = position
        self.comment = comment
        self.is_completed = is_completed
        self.due_date = due_date
        self.created_at = created_at

        self._task = {
            "task_id": self.task_id,
            "category_id": self.category_id,
            "title": self.title,
            "position": self.position,
            "comment": self.comment,
            "is_completed": self.is_completed,
            "due_date": self.due_date,
            "created_at": self.created_at
        }

    def as_dict(self):
        return self._task

    def __str__(self) -> str:
        json_task = json.dumps(self._task)
        return json_task

import json


class Project:
    def __init__(
            self,
            project_id: int,
            board_id: int,
            name: str,
            position: int
    ):
        self.project_id = project_id
        self.board_id = board_id
        self.name = name
        self.position = position

        self._project = {
            "project_id": self.project_id,
            "board_id": self.board_id,
            "name": self.name,
            "position": self.position
        }

    def as_dict(self) -> dict:
        return self._project

    def __str__(self) -> str:
        json_project = json.dumps(self._project)
        return json_project

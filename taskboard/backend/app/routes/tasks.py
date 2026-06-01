from flask import request, jsonify, Blueprint
from taskboard.backend.app.schemas.task import SqlTaskRepository

repo = SqlTaskRepository()

task_pages = Blueprint('task_pages', __name__, template_folder='templates')


# ---------- CREATE ----------
@task_pages.route('/tasks', methods=['POST'])
def create_task():
    data = request.json

    new_task = repo.create_task(
        project_id=data.get('project_id'),
        title=data.get('title'),
        position=data.get('position'),
        comment=data.get('comment'),
        status=data.get('status'),
        due_date=data.get('due_date'),
        created_at=data.get('created_at')
    )

    return jsonify({
        "message": "task created"
        , "task_id": new_task.task_id
    }), 201


# ---------- READ ALL ----------
@task_pages.route('/tasks', methods=['GET'])
def read_tasks():
    tasks = repo.read_tasks()

    return jsonify(tasks), 200


# ---------- READ ONE ----------
@task_pages.route('/tasks/<int:id>', methods=['GET'])
def read_task(id):
    task = repo.read_task(id)

    if task:
        return task.as_dict(), 200
    else:
        return jsonify({"error": "task not found"}), 404


# ---------- UPDATE -------------
@task_pages.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json

    task = repo.update_task(
        task_id=id,
        project_id=data.get('project_id'),
        title=data.get('title'),
        position=data.get('position'),
        comment=data.get('comment'),
        status=data.get('status'),
        due_date=data.get('due_date'),
        created_at=data.get('created_at')
    )

    if task:
        return jsonify({"message": "Task updated"}), 200
    else:
        return jsonify({"error": "Task not found"}), 404


# ---------- DELETE ----------
@task_pages.route('/tasks/<int:id>', methods=['DELETE'])
def delete_order(id):
    confirm = repo.delete_task(id)

    if confirm:
        return jsonify({"message": "Task deleted"}), 200
    else:
        return jsonify({"error": "Task not found"}), 404

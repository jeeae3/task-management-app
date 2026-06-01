from flask import request, jsonify, Blueprint
from schemas.project import SqlProjectRepository

repo = SqlProjectRepository()

project_pages = Blueprint('project_pages', __name__, template_folder='templates')


# ---------- CREATE ----------
@project_pages.route('/projects', methods=['POST'])
def create_project():
    data = request.json

    new_project = repo.create_project(
        board_id=data.get('board_id'),
        name=data.get('name'),
        position=data.get('position')
    )

    return jsonify({
        "message": "project created"
        , "project_id": new_project.project_id
    }), 201


# ---------- READ ALL ----------
@project_pages.route('/projects', methods=['GET'])
def read_projects():
    projects = repo.read_projects()

    return jsonify(projects), 200


# ---------- READ ONE ----------
@project_pages.route('/projects/<int:id>', methods=['GET'])
def read_project(id):
    project = repo.read_project(id)

    if project:
        return project.as_dict(), 200
    else:
        return jsonify({"error": "project not found"}), 404


# ---------- UPDATE -------------
@project_pages.route('/projects/<int:id>', methods=['PUT'])
def update_project(id):
    data = request.json

    project = repo.update_project(
        project_id=id,
        board_id=data.get('board_id'),
        name=data.get('name'),
        position=data.get('position')
    )

    if project:
        return jsonify({"message": "Project updated"}), 200
    else:
        return jsonify({"error": "Project not found"}), 404


# ---------- DELETE ----------
@project_pages.route('/projects/<int:id>', methods=['DELETE'])
def delete_order(id):
    confirm = repo.delete_project(id)

    if confirm:
        return jsonify({"message": "Project deleted"}), 200
    else:
        return jsonify({"error": "Project not found"}), 404

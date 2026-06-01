import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import TaskCard from "../components/TaskCard";
import TaskModal from "../components/TaskModal";
import { projectsApi, tasksApi } from "../api";

const COLUMNS = [
  { key: "todo", label: "To Do", color: "#6b7280" },
  { key: "in_progress", label: "In Progress", color: "#f59e0b" },
  { key: "done", label: "Done", color: "#10b981" },
];

export default function BoardPage() {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  const fetchData = async () => {
    try {
      const [proj, allTasks] = await Promise.all([
        projectsApi.getOne(id),
        tasksApi.getAll(),
      ]);
      setProject(proj);
      setTasks(allTasks.filter((t) => t.project_id === Number(id)));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  const handleCreateTask = async (formData) => {
    await tasksApi.create({
      project_id: Number(id),
      title: formData.title,
      comment: formData.description,
      status: formData.status,
      priority: formData.priority,
      position: tasks.length + 1,
      due_date: null,
      created_at: new Date().toISOString(),
    });
    setShowModal(false);
    fetchData();
  };

  const handleUpdateTask = async (formData) => {
    await tasksApi.update(editingTask.task_id, {
      project_id: Number(id),
      title: formData.title,
      comment: formData.description,
      status: formData.status,
      priority: formData.priority,
      position: editingTask.position,
      due_date: editingTask.due_date,
      created_at: editingTask.created_at,
    });
    setEditingTask(null);
    setShowModal(false);
    fetchData();
  };

  const handleStatusChange = async (taskId, newStatus) => {
    const task = tasks.find((t) => t.task_id === taskId);
    await tasksApi.update(taskId, {
      project_id: Number(id),
      title: task.title,
      comment: task.comment,
      status: newStatus,
      priority: task.priority,
      position: task.position,
      due_date: task.due_date,
      created_at: task.created_at,
    });
    fetchData();
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm("Delete this task?")) return;
    await tasksApi.delete(taskId);
    fetchData();
  };

  const openEdit = (task) => {
    setEditingTask(task);
    setShowModal(true);
  };

  if (loading) return <div className="loading">Loading board...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <Link to="/" className="back-link">← Projects</Link>
          <h1>{project?.name}</h1>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          + Add Task
        </button>
      </div>

      <div className="board">
        {COLUMNS.map((col) => {
          const colTasks = tasks.filter((t) => t.status === col.key);
          return (
            <div key={col.key} className="column">
              <div className="column-header" style={{ borderColor: col.color }}>
                <span className="column-title">{col.label}</span>
                <span className="column-count">{colTasks.length}</span>
              </div>
              <div className="column-body">
                {colTasks.map((task) => (
                  <TaskCard
                    key={task.task_id}
                    task={{
                      ...task,
                      id: task.task_id,
                      description: task.comment,
                      priority: task.priority,
                    }}
                    onEdit={() => openEdit(task)}
                    onDelete={() => handleDeleteTask(task.task_id)}
                    onStatusChange={handleStatusChange}
                    columns={COLUMNS}
                  />
                ))}
                {colTasks.length === 0 && (
                  <div className="column-empty">No tasks here</div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {showModal && (
        <TaskModal
          task={editingTask ? {
            ...editingTask,
            description: editingTask.comment,
            priority: editingTask.priority,
          } : null}
          onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
          onClose={() => { setShowModal(false); setEditingTask(null); }}
        />
      )}
    </div>
  );
}
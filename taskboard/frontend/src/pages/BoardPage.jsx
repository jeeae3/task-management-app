import React, { useState } from "react";
import { useParams, Link } from "react-router-dom";
import TaskCard from "../components/TaskCard";
import TaskModal from "../components/TaskModal";

const COLUMNS = [
  { key: "todo", label: "To Do", color: "#6b7280" },
  { key: "in_progress", label: "In Progress", color: "#f59e0b" },
  { key: "done", label: "Done", color: "#10b981" },
];

// Mock data — replace with real API calls once backend is ready
const MOCK_TASKS = [
  { id: 1, project_id: 1, title: "Design mockups", description: "Figma designs for all screens", status: "todo", priority: "high" },
  { id: 2, project_id: 1, title: "Set up repo", description: "Initialize GitHub repo", status: "in_progress", priority: "medium" },
  { id: 3, project_id: 1, title: "Write README", description: "Document the project", status: "done", priority: "low" },
  { id: 4, project_id: 1, title: "Fix login bug", description: "Users can't log in on mobile", status: "todo", priority: "high" },
];

const MOCK_PROJECT = { id: 1, name: "Website Redesign", description: "Revamp the landing page" };

export default function BoardPage() {
  const { id } = useParams();
  const [tasks, setTasks] = useState(MOCK_TASKS);
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  const handleCreateTask = (formData) => {
    const newTask = {
      id: tasks.length + 1,
      project_id: Number(id),
      ...formData,
    };
    setTasks([...tasks, newTask]);
    setShowModal(false);
  };

  const handleUpdateTask = (formData) => {
    setTasks(tasks.map((t) =>
      t.id === editingTask.id ? { ...t, ...formData } : t
    ));
    setEditingTask(null);
    setShowModal(false);
  };

  const handleStatusChange = (taskId, newStatus) => {
    setTasks(tasks.map((t) =>
      t.id === taskId ? { ...t, status: newStatus } : t
    ));
  };

  const handleDeleteTask = (taskId) => {
    if (!window.confirm("Delete this task?")) return;
    setTasks(tasks.filter((t) => t.id !== taskId));
  };

  const openEdit = (task) => {
    setEditingTask(task);
    setShowModal(true);
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <Link to="/" className="back-link">← Projects</Link>
          <h1>{MOCK_PROJECT.name}</h1>
          <p className="project-desc">{MOCK_PROJECT.description}</p>
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
                    key={task.id}
                    task={task}
                    onEdit={() => openEdit(task)}
                    onDelete={() => handleDeleteTask(task.id)}
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
          task={editingTask}
          onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
          onClose={() => { setShowModal(false); setEditingTask(null); }}
        />
      )}
    </div>
  );
}
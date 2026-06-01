import React from "react";

const PRIORITY_COLORS = { low: "#10b981", medium: "#f59e0b", high: "#ef4444" };

export default function TaskCard({ task, onEdit, onDelete, onStatusChange, columns }) {
  const currentIndex = columns.findIndex((c) => c.key === task.status);

  return (
    <div className="task-card">
      <div className="task-card-header">
        <span
          className="priority-badge"
          style={{ background: PRIORITY_COLORS[task.priority] }}
        >
          {task.priority}
        </span>
        <div className="task-card-actions">
          <button className="btn-icon" onClick={onEdit} title="Edit">✎</button>
          <button className="btn-icon btn-danger" onClick={onDelete} title="Delete">✕</button>
        </div>
      </div>

      <h4 className="task-title">{task.title}</h4>
      {task.description && <p className="task-desc">{task.description}</p>}

      <div className="task-card-footer">
        {currentIndex > 0 && (
          <button
            className="btn-move"
            onClick={() => onStatusChange(task.id, columns[currentIndex - 1].key)}
          >
            ← Move Back
          </button>
        )}
        {currentIndex < columns.length - 1 && (
          <button
            className="btn-move btn-move-forward"
            onClick={() => onStatusChange(task.id, columns[currentIndex + 1].key)}
          >
            Move Forward →
          </button>
        )}
      </div>
    </div>
  );
}
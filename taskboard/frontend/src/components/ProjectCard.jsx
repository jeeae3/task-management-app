import React from "react";

export default function ProjectCard({ project, onClick, onEdit, onDelete }) {
  return (
    <div className="project-card" onClick={onClick}>
      <div className="project-card-header">
        <h3>{project.name}</h3>
        <div className="project-card-actions" onClick={(e) => e.stopPropagation()}>
          <button className="btn-icon" onClick={onEdit} title="Edit">✎</button>
          <button className="btn-icon btn-danger" onClick={onDelete} title="Delete">✕</button>
        </div>
      </div>
      {project.description && <p className="project-card-desc">{project.description}</p>}
      <div className="project-card-footer">
        <span className="task-count">{project.task_count ?? 0} tasks</span>
        <span className="arrow">→</span>
      </div>
    </div>
  );
}
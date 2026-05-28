import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import ProjectCard from "../components/ProjectCard";
import ProjectModal from "../components/ProjectModal";

const MOCK_PROJECTS = [
  { id: 1, name: "Website Redesign", description: "Revamp the landing page", task_count: 3 },
  { id: 2, name: "Mobile App", description: "iOS and Android launch", task_count: 5 },
  { id: 3, name: "Database Migration", description: "Move to new server", task_count: 2 },
];

export default function ProjectsPage() {
  const [projects, setProjects] = useState(() => {
    const saved = localStorage.getItem("projects");
    return saved ? JSON.parse(saved) : MOCK_PROJECTS;
  });
  const [showModal, setShowModal] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const navigate = useNavigate();

  const handleCreate = (formData) => {
    const newProject = {
      id: projects.length + 1,
      ...formData,
      task_count: 0,
    };
    const updated = [...projects, newProject];
    setProjects(updated);
    localStorage.setItem("projects", JSON.stringify(updated));
    setShowModal(false);
  };

  const handleUpdate = (formData) => {
    const updated = projects.map((p) =>
      p.id === editingProject.id ? { ...p, ...formData } : p
    );
    setProjects(updated);
    localStorage.setItem("projects", JSON.stringify(updated));
    setEditingProject(null);
    setShowModal(false);
  };

  const handleDelete = (id) => {
    if (!window.confirm("Delete this project and all its tasks?")) return;
    const updated = projects.filter((p) => p.id !== id);
    setProjects(updated);
    localStorage.setItem("projects", JSON.stringify(updated));
  };

  const openEdit = (project) => {
    setEditingProject(project);
    setShowModal(true);
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Projects</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          + New Project
        </button>
      </div>

      {projects.length === 0 ? (
        <div className="empty-state">
          <p>No projects yet. Create your first one!</p>
        </div>
      ) : (
        <div className="projects-grid">
          {projects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onClick={() => navigate(`/projects/${project.id}`)}
              onEdit={() => openEdit(project)}
              onDelete={() => handleDelete(project.id)}
            />
          ))}
        </div>
      )}

      {showModal && (
        <ProjectModal
          project={editingProject}
          onSubmit={editingProject ? handleUpdate : handleCreate}
          onClose={() => {
            setShowModal(false);
            setEditingProject(null);
          }}
        />
      )}
    </div>
  );
}
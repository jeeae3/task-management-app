import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ProjectCard from "../components/ProjectCard";
import ProjectModal from "../components/ProjectModal";
import { projectsApi } from "../api";

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const navigate = useNavigate();

  const fetchProjects = async () => {
    try {
      const data = await projectsApi.getAll();
      setProjects(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreate = async (formData) => {
    await projectsApi.create({
      name: formData.name,
      board_id: 1,
      position: projects.length + 1,
    });
    setShowModal(false);
    fetchProjects();
  };

  const handleUpdate = async (formData) => {
    await projectsApi.update(editingProject.project_id, {
      name: formData.name,
      board_id: 1,
      position: editingProject.position,
    });
    setEditingProject(null);
    setShowModal(false);
    fetchProjects();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this project and all its tasks?")) return;
    await projectsApi.delete(id);
    fetchProjects();
  };

  const openEdit = (project) => {
    setEditingProject(project);
    setShowModal(true);
  };

  if (loading) return <div className="loading">Loading projects...</div>;
  if (error) return <div className="error">Error: {error}</div>;

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
              key={project.project_id}
              project={{ ...project, id: project.project_id, task_count: 0 }}
              onClick={() => navigate(`/projects/${project.project_id}`)}
              onEdit={() => openEdit(project)}
              onDelete={() => handleDelete(project.project_id)}
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
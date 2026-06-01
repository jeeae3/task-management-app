const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:4000";

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (response.status === 204) return null;
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Something went wrong");
  }
  return response.json();
}

export const projectsApi = {
  getAll: () => request("/projects"),
  getOne: (id) => request(`/projects/${id}`),
  create: (data) => request("/projects", { method: "POST", body: JSON.stringify(data) }),
  update: (id, data) => request(`/projects/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  delete: (id) => request(`/projects/${id}`, { method: "DELETE" }),
};

export const tasksApi = {
  getAll: (projectId) => request(`/tasks${projectId ? `?project_id=${projectId}` : ""}`),
  getOne: (id) => request(`/tasks/${id}`),
  create: (data) => request("/tasks", { method: "POST", body: JSON.stringify(data) }),
  update: (id, data) => request(`/tasks/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  delete: (id) => request(`/tasks/${id}`, { method: "DELETE" }),
};
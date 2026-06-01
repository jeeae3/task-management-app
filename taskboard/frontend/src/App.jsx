import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ProjectsPage from "./pages/ProjectsPage";
import BoardPage from "./pages/BoardPage";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <Link to="/" className="nav-brand">
            <span className="brand-icon">⬡</span> TaskBoard
          </Link>
          <div className="nav-links">
            <Link to="/">Projects</Link>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<ProjectsPage />} />
            <Route path="/projects/:id" element={<BoardPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import App from "./App";
import PageShell from "./PageShell";
import Dashboard from "./components/Dashboard.jsx";
// import Tasks from "./components/Tasks.jsx";
// import Settings from "./components/Settings.jsx";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      {/* Keep App as the full dashboard board exactly as before */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<App />} />

      {/* Other pages render inside the same Sidebar/Main shell */}
      {/*
      <Route
        path="/tasks"
        element={
          <PageShell>
            <Tasks />
          </PageShell>
        }
      />
      <Route
        path="/settings"
        element={
          <PageShell>
            <Settings />
          </PageShell>
        }
      />
      */}
      {/* add more as needed: bulk, tracking, tutorial, feedback, rules */}
    </Routes>
  </BrowserRouter>
);

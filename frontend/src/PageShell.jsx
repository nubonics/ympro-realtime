import React from "react";
import Sidebar from "./components/Sidebar";

export default function PageShell({ children }) {
  return (
    <div className="layout-root">
      <Sidebar />
      <main className="main-board">
        {children}
      </main>
    </div>
  );
}

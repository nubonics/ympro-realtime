import React, { useState } from "react";
import {
  FaTachometerAlt,
  FaLayerGroup,
  FaGavel,
  FaRoute,
  FaChalkboardTeacher,
  FaCommentDots,
  FaChevronLeft,
  FaChevronRight,
  FaLock,
} from "react-icons/fa";

// Example: determine if user is admin (replace with real logic)
const isAdmin = window.localStorage.getItem("isAdmin") === "true";

const sidebarItems = [
  { icon: <FaTachometerAlt size={22} />, label: "Dashboard" },
  { icon: <FaLayerGroup size={22} />, label: "Bulk" },
  // Rules is conditionally rendered below
  { icon: <FaRoute size={22} />, label: "Tracking" },
  { icon: <FaChalkboardTeacher size={22} />, label: "Tutorial" },
  { icon: <FaCommentDots size={22} />, label: "Feedback" },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div
      className={`sidebar${collapsed ? " collapsed" : ""}`}
      style={{
        width: collapsed ? "64px" : "200px",
        transition: "width 0.23s cubic-bezier(.4,0,.2,1)",
      }}
    >
      <div className="sidebar-toggle" onClick={() => setCollapsed((c) => !c)}>
        {collapsed ? <FaChevronRight /> : <FaChevronLeft />}
      </div>
      <div className="sidebar-list">
        {sidebarItems.map((item) => (
          <div className="sidebar-item" key={item.label}>
            {item.icon}
            {!collapsed && <span className="sidebar-label">{item.label}</span>}
          </div>
        ))}
        {isAdmin && (
          <div className="sidebar-item" key="Rules">
            <FaGavel size={22} />
            {!collapsed && (
              <span className="sidebar-label">
                Rules <FaLock style={{ marginLeft: 4, fontSize: 14, verticalAlign: "middle" }} />
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
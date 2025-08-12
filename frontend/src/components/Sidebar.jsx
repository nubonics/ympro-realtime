// Sidebar.jsx
import React, { useState } from "react";
import { NavLink } from "react-router-dom";
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
import { IconContext } from "react-icons";
import "./sidebar.css";

const isAdmin = window.localStorage.getItem("isAdmin") === "true";
const ICON_SIZE = 22;

const items = [
  { to: "/dashboard", Icon: FaTachometerAlt, label: "Dashboard" },
  { to: "/bulk",       Icon: FaLayerGroup,    label: "Bulk" },
  { to: "/tracking",   Icon: FaRoute,         label: "Tracking" },
  { to: "/tutorial",   Icon: FaChalkboardTeacher, label: "Tutorial" },
  { to: "/feedback",   Icon: FaCommentDots,   label: "Feedback" },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const wrapCls = `sidebar${collapsed ? " collapsed" : ""}`;
  const linkCls = ({ isActive }) => `sidebar-item ${isActive ? "sidebar-item-active" : ""}`;

  return (
    <div className={wrapCls}>
      <button
        className="sidebar-toggle"
        onClick={() => setCollapsed(c => !c)}
        title={collapsed ? "Expand" : "Collapse"}
        aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
      >
        {collapsed ? <FaChevronRight /> : <FaChevronLeft />}
      </button>

      <IconContext.Provider value={{ size: `${ICON_SIZE}px`, className: "sidebar-svg" }}>
        <nav className="sidebar-list">
          {items.map(({ to, Icon, label }) => (
            <NavLink key={label} to={to} className={linkCls}>
              <span className="sidebar-icon"><Icon /></span>
              <span className="sidebar-label" aria-hidden={collapsed}>{label}</span>
            </NavLink>
          ))}

          {isAdmin && (
            <NavLink to="/rules" className={linkCls}>
              <span className="sidebar-icon"><FaGavel /></span>
              <span className="sidebar-label" aria-hidden={collapsed}>
                Rules <FaLock style={{ marginLeft: 4, fontSize: 14, verticalAlign: "middle" }} />
              </span>
            </NavLink>
          )}
        </nav>
      </IconContext.Provider>
    </div>
  );
}

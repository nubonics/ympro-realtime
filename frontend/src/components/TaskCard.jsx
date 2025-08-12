// src/components/TaskCard.jsx
import React, { useState, useRef, useEffect } from "react";
import { useDrag, useDrop } from "react-dnd";
import { FaLock, FaLockOpen, FaCopy } from "react-icons/fa";
import { TASK_TYPES } from "../constants/taskTypes";
import { useToast } from "./ui/ToastProvider";

export default function TaskCard({
  task,
  isDraggable = true,
  onRemove,
  onDropEmpty,
  isHostlerTask,
  onLockToggle,
}) {
  const toast = useToast();
  const [locked, setLocked] = useState(task.locked ?? false);
  const [showTooltip, setShowTooltip] = useState(false);
  const tooltipTimeout = useRef(null);

  // Drag
  const dragType = String(task?.type || "").toLowerCase();
  const [{ isDragging }, drag] = useDrag({
    type: dragType,
    item: () => ({ type: dragType, task }),
    canDrag: isDraggable,
    collect: (monitor) => ({ isDragging: monitor.isDragging() }),
  });

  // Drop (only on PULL accepts EMPTY)
  const isPull =
    String(task?.type || "").toLowerCase() ===
    String(TASK_TYPES.PULL || "pull").toLowerCase();

  let dropRef = null;
  let dropState = {};
  if (isPull) {
    const [dropCollected, drop] = useDrop({
      accept: [String(TASK_TYPES.EMPTY || "empty").toLowerCase()],
      drop: (item) => onDropEmpty && onDropEmpty(item.task, task),
      collect: (monitor) => ({
        isOver: monitor.isOver(),
        canDrop: monitor.canDrop(),
      }),
    });
    dropRef = drop;
    dropState = dropCollected;
  }

  // Tooltip timing
  const handleMouseEnter = () => {
    tooltipTimeout.current = setTimeout(() => setShowTooltip(true), 3000);
  };
  const handleMouseLeave = () => {
    clearTimeout(tooltipTimeout.current);
    setShowTooltip(false);
  };
  useEffect(() => {
    if (isDragging) {
      clearTimeout(tooltipTimeout.current);
      setShowTooltip(false);
    }
  }, [isDragging]);

  // Copy trailer -> toast
  const handleCopy = async (e) => {
    e.stopPropagation();
    const txt = String(task?.trailer || "").trim();
    if (!txt) return;
    try {
      await navigator.clipboard.writeText(txt);
      toast.push(`Copied trailer ${txt}`, "success");
    } catch {
      toast.push("Copy failed", "error");
    }
  };

  // Lock toggle
  const handleLockToggle = (e) => {
    e.stopPropagation();
    const newLocked = !locked;
    setLocked(newLocked);
    if (typeof onLockToggle === "function") onLockToggle(task, newLocked);
  };

  // Status badge (supports old `pending` boolean and new `status` string)
  const statusRaw = String(
    task?.status ?? (task?.pending ? "pending" : "")
  ).toLowerCase();
  const isCompleted = statusRaw === "completed";
  const isPending = statusRaw === "pending" || (!statusRaw && !isCompleted);
  const statusLabel = isCompleted ? "COMPLETED" : "PENDING";

  const cardRef = (node) => {
    if (isDraggable && drag) drag(node);
    if (dropRef) dropRef(node);
  };

  const dropHighlight = isPull && dropState.isOver && dropState.canDrop;

  const tooltipContent = (
    <div className="task-tooltip">
      <div><strong>Task ID:</strong> {task?.id}</div>
      <div><strong>Type:</strong> {task?.type}</div>
      <div><strong>Trailer:</strong> {task?.trailer}</div>
      {task?.door && <div><strong>Door:</strong> {task.door}</div>}
      {task?.zoneType && <div><strong>Zone:</strong> {task.zoneType}</div>}
      {task?.zoneLocation && <div><strong>Location:</strong> {task.zoneLocation}</div>}
      {task?.priority && <div><strong>Priority:</strong> {task.priority}</div>}
      {task?.note && <div><strong>Note:</strong> {task.note}</div>}
      {(statusRaw || isPending) && <div><strong>Status:</strong> {statusLabel}</div>}
      {typeof task?.locked === "boolean" && <div><strong>Locked:</strong> {locked ? "Yes" : "No"}</div>}
    </div>
  );

  return (
    <div
      ref={cardRef}
      className={`task-card side-icons-layout${isPull ? " pull-drop-target" : ""}${dropHighlight ? " highlight-drop" : ""}${isCompleted ? " is-completed" : ""}`}
      style={{
        opacity: isDragging ? 0.5 : 1,
        cursor: isDraggable ? "grab" : "default",
        position: "relative",
        border: dropHighlight ? "2px solid #2980ef" : undefined,
        background: dropHighlight ? "#eaf5ff" : undefined,
      }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className="side-icon left">
        <button className="lock-btn" onClick={handleLockToggle} title={locked ? "Unlock" : "Lock"}>
          {locked ? <FaLock /> : <FaLockOpen />}
        </button>
      </div>

      <div className="task-main-content">
        <div className="task-main-label" style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <span>{task?.trailer} {task?.door && `(${task.door})`}</span>
          <span className={`task-status ${isCompleted ? "completed" : "pending"}`}>{statusLabel}</span>
        </div>
      </div>

      <div className="side-icon right">
        <button className="copy-btn" onClick={handleCopy} title="Copy trailer number">
          <FaCopy />
        </button>
      </div>

      {showTooltip && !isDragging && (
        <div className="task-tooltip-popup">{tooltipContent}</div>
      )}
    </div>
  );
}

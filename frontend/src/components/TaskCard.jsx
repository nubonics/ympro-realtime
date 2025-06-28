import React, { useState, useRef } from "react";
import { useDrag, useDrop } from "react-dnd";
import { FaLock, FaLockOpen, FaCopy } from "react-icons/fa";
import { TASK_TYPES } from "../constants/taskTypes";

function TaskCard({
  task,
  isDraggable = true,
  onRemove,
  onDropEmpty,
  isHostlerTask,
  onLockToggle,
}) {
  const [copied, setCopied] = useState(false);
  const [locked, setLocked] = useState(task.locked ?? false);
  const [showTooltip, setShowTooltip] = useState(false);
  const tooltipTimeout = useRef(null);

  // Drag source setup (for all tasks)
  const [{ isDragging }, drag] = useDrag({
    type: (task.type || "").toLowerCase(),
    item: () => ({
      type: (task.type || "").toLowerCase(),
      task,
    }),
    canDrag: isDraggable,
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  // Drop target ONLY for pull tasks: accept empties
  const isPull = (task.type || '').toLowerCase() === TASK_TYPES.PULL;
  let dropRef = null;
  let dropState = {};
  if (isPull) {
    // Only allow empties to be dropped here
    const [dropCollected, drop] = useDrop({
      accept: [TASK_TYPES.EMPTY],
      drop: (item, monitor) => {
        if (onDropEmpty) onDropEmpty(item.task, task); // item.task is the empty, task is the pull
      },
      collect: (monitor) => ({
        isOver: monitor.isOver(),
        canDrop: monitor.canDrop(),
      }),
    });
    dropRef = drop;
    dropState = dropCollected;
  }

  const handleMouseEnter = () => {
    tooltipTimeout.current = setTimeout(() => setShowTooltip(true), 3000);
  };
  const handleMouseLeave = () => {
    clearTimeout(tooltipTimeout.current);
    setShowTooltip(false);
  };

  // Hide tooltip instantly if dragging starts (reacts to drag state change)
  React.useEffect(() => {
    if (isDragging) {
      clearTimeout(tooltipTimeout.current);
      setShowTooltip(false);
    }
  }, [isDragging]);

  const handleCopy = (e) => {
    e.stopPropagation();
    if (task.trailer) {
      navigator.clipboard.writeText(task.trailer);
      setCopied(true);
      setTimeout(() => setCopied(false), 1000);
    }
  };

  const handleLockToggle = (e) => {
    e.stopPropagation();
    const newLocked = !locked;
    setLocked(newLocked);
    if (typeof onLockToggle === "function") {
      onLockToggle(task, newLocked);
    }
  };

  const isPending = !!task.pending;

  // Tooltip content (customize as needed)
  const tooltipContent = (
    <div className="task-tooltip">
      <div><strong>Task ID:</strong> {task.id}</div>
      <div><strong>Type:</strong> {task.type}</div>
      <div><strong>Trailer:</strong> {task.trailer}</div>
      {task.door && <div><strong>Door:</strong> {task.door}</div>}
      {task.zoneType && <div><strong>Zone:</strong> {task.zoneType}</div>}
      {task.zoneLocation && <div><strong>Location:</strong> {task.zoneLocation}</div>}
      {task.priority && <div><strong>Priority:</strong> {task.priority}</div>}
      {task.note && <div><strong>Note:</strong> {task.note}</div>}
    </div>
  );

  // Compose refs (drag always, drop only for pull task)
  // If both drag and drop, make sure both refs are applied
  const cardRef = (node) => {
    if (isDraggable && drag) drag(node);
    if (dropRef) dropRef(node);
  };

  // Highlight if a draggable empty is over this pull task
  const dropHighlight = isPull && dropState.isOver && dropState.canDrop;

  return (
    <div
      ref={cardRef}
      className={`task-card side-icons-layout${isPull ? ' pull-drop-target' : ''}${dropHighlight ? ' highlight-drop' : ''}`}
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
        <div className="task-main-label">
          <span>{task.trailer} {task.door && `(${task.door})`}</span>
        </div>
        {isPending && (
          <div className="pending-badge">PENDING</div>
        )}
      </div>
      <div className="side-icon right">
        <button className="copy-btn" onClick={handleCopy} title="Copy trailer number">
          <FaCopy />
        </button>
        {copied && <span className="copied-tooltip">Copied!</span>}
      </div>
      {showTooltip && !isDragging && (
        <div className="task-tooltip-popup">
          {tooltipContent}
        </div>
      )}
    </div>
  );
}

export default TaskCard;
import React from "react";
import { useDrop } from "react-dnd";
import { TASK_TYPES } from "../constants/taskTypes";

/**
 * Props:
 * - onDropRecycle: function(task)
 * - tasks?: number[] (optional counter display)
 */
function RecycleBin({ onDropRecycle, tasks = [] }) {
  const baseTypes = [
    TASK_TYPES.PULL,
    TASK_TYPES.BRING,
    TASK_TYPES.HOOK,
    TASK_TYPES.HOSTLER,
    TASK_TYPES.WORKBASKET,
  ].filter(Boolean);

  // accept the lowercase versions because TaskCard uses lowercase drag types
  const acceptTypes = baseTypes.map((t) => String(t).toLowerCase());

  const [{ isOver, canDrop }, drop] = useDrop({
    accept: acceptTypes,
    canDrop: (item) => String(item?.task?.type || "").toLowerCase() !== String(TASK_TYPES.EMPTY || "empty").toLowerCase(),
    drop: (item) => {
      const t = item?.task;
      if (t && onDropRecycle) onDropRecycle(t);
    },
    collect: (monitor) => ({
      isOver: monitor.isOver(),
      canDrop: monitor.canDrop(),
    }),
  });

  return (
    <div
      ref={drop}
      className={
        "recyclebin-container top-compact" +
        (isOver && canDrop ? " recyclebin-active" : "")
      }
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
      }}
    >
      <span style={{ fontSize: "2rem", fontWeight: 700, color: "#6bbfbf" }}>
        Recycle Bin
      </span>
      {Array.isArray(tasks) && tasks.length > 0 && (
        <div style={{ marginTop: 8, fontSize: "1rem", color: "#bfeefb" }}>
          {tasks.length} task{tasks.length > 1 ? "s" : ""} in bin
        </div>
      )}
    </div>
  );
}

export default RecycleBin;

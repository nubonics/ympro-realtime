import React from "react";
import { useDrop } from "react-dnd";
import { TASK_TYPES } from "../constants/taskTypes";

/**
 * Props:
 * - onDropRecycle: function(task) -- called when a task is dropped on the bin
 */
function RecycleBin({ onDropRecycle, tasks = [] }) {
  // Accept all task types except EMPTY
  const acceptTypes = [
    TASK_TYPES.PULL,
    TASK_TYPES.BRING,
    TASK_TYPES.HOOK,
    TASK_TYPES.HOSTLER,
    TASK_TYPES.WORKBASKET,
  ];

  const [{ isOver, canDrop }, drop] = useDrop({
    accept: acceptTypes,
    canDrop: (item) => item.task.type !== TASK_TYPES.EMPTY,
    drop: (item) => {
      if (onDropRecycle) onDropRecycle(item.task);
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
      {tasks.length > 0 && (
        <div style={{ marginTop: 8, fontSize: "1rem", color: "#bfeefb" }}>
          {tasks.length} task{tasks.length > 1 ? "s" : ""} in bin
        </div>
      )}
    </div>
  );
}

export default RecycleBin;
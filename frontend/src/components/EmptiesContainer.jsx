import React from "react";
import { useDrag } from "react-dnd";
import { TASK_TYPES } from "../constants/taskTypes";
import "./EmptiesContainer.css";

function DraggableEmptyTask({ empty }) {
  const [{ isDragging }, drag] = useDrag({
    type: TASK_TYPES.EMPTY,
    item: { task: empty },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  });
  return (
    <div
      ref={drag}
      className={`task-card empty${isDragging ? " dragging" : ""}`}
      style={{
        opacity: isDragging ? 0.5 : 1,
        minWidth: "90px",
        textAlign: "center",
        fontWeight: 500,
        fontSize: "1.07rem",
        background: "#23252e",
        border: "1px solid #383a45",
        borderRadius: "9px",
        color: "#d5d8e6",
        boxShadow: isDragging
          ? "0 4px 16px 0 rgba(60,80,150,0.14)"
          : "0 1.5px 6px 0 rgba(40,42,54,0.05)",
        marginRight: "0px"
      }}
    >
      {empty.label}
    </div>
  );
}

function EmptiesContainer({ emptyTasks }) {
  return (
    <div className="empties-row-horizontal">
      {emptyTasks.map((empty, i) => (
        <DraggableEmptyTask key={i} empty={empty} />
      ))}
    </div>
  );
}

export default EmptiesContainer;
import React from "react";
import { useDrop } from "react-dnd";
import TaskCard from "./TaskCard";
import { TASK_TYPES } from "../constants/taskTypes";

function splitTasksByType(tasks = []) {
  return {
    HOOK: tasks.filter((t) => (t.type || '').toLowerCase() === TASK_TYPES.HOOK),
    PULL: tasks.filter((t) => (t.type || '').toLowerCase() === TASK_TYPES.PULL),
    BRING: tasks.filter((t) => (t.type || '').toLowerCase() === TASK_TYPES.BRING),
    OTHER: tasks.filter(
      (t) =>
        ![
          TASK_TYPES.HOOK,
          TASK_TYPES.PULL,
          TASK_TYPES.BRING,
        ].includes((t.type || '').toLowerCase())
    ),
  };
}

function Container({
  title,
  tasks,
  colorClass,
  onDropEmpty,
  isHostlerContainer = false,
  onDropHostlerTask,
  isWorkbasket = false,
  topCompact = false,
}) {
  const [{ isOver, canDrop }, drop] = useDrop({
    accept: [TASK_TYPES.PULL, TASK_TYPES.BRING, TASK_TYPES.HOOK].map(t => t.toLowerCase()),
    canDrop: (item) => isHostlerContainer || isWorkbasket,
    drop: (item, monitor) => {
      if (onDropHostlerTask && (isHostlerContainer || isWorkbasket)) {
        // Only reassign if changing hostler/workbasket
        const newHostler = isWorkbasket ? "" : title;
        if (item.task.hostler !== newHostler) {
          onDropHostlerTask(item.task, newHostler);
        }
      }
    },
    collect: (monitor) => ({
      isOver: monitor.isOver(),
      canDrop: monitor.canDrop(),
    }),
  });

  const containerClass = [
    "container",
    colorClass,
    topCompact ? "top-compact" : "",
  ]
    .filter(Boolean)
    .join(" ");

  // Use two-column layout for hostler containers and workbasket
  if (isHostlerContainer || isWorkbasket) {
    const { HOOK, PULL, BRING } = splitTasksByType(tasks);
    const taskCount = tasks.length;

    return (
      <div
        ref={drop}
        className={containerClass}
        style={isOver && canDrop ? { background: "#e3f1ff" } : {}}
      >
        <div className="container-title-center">
          <h3>
            {title}
            <span className="task-count-label"> ({taskCount} task{taskCount === 1 ? "" : "s"})</span>
          </h3>
        </div>
        {/* HOOK tasks row, if any */}
        {HOOK.length > 0 && (
          <div className="hostler-hook-row">
            {HOOK.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                isHostlerTask={isHostlerContainer}
                onDropEmpty={onDropEmpty}
              />
            ))}
          </div>
        )}
        {/* Two columns: PULL and BRING */}
        <div className="hostler-pull-bring-row">
          <div className="hostler-pull-col">
            <div className="hostler-type-label">PULL</div>
            {PULL.length === 0 ? (
              <div className="empty-hostlers no-tasks-centered">No Pulls</div>
            ) : (
              PULL.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  isHostlerTask={isHostlerContainer}
                  onDropEmpty={onDropEmpty}
                />
              ))
            )}
          </div>
          <div className="hostler-bring-col">
            <div className="hostler-type-label">BRING</div>
            {BRING.length === 0 ? (
              <div className="empty-hostlers no-tasks-centered">No Brings</div>
            ) : (
              BRING.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  isHostlerTask={isHostlerContainer}
                  onDropEmpty={onDropEmpty}
                />
              ))
            )}
          </div>
        </div>
      </div>
    );
  }

  // Default: single-column for other containers
  return (
    <div
      ref={null}
      className={containerClass}
      style={isOver && canDrop ? { background: "#e3f1ff" } : {}}
    >
      <h3>{title}</h3>
      {tasks.map((t) => (
        <TaskCard
          key={t.id}
          task={t}
          isHostlerTask={isHostlerContainer}
          onDropEmpty={onDropEmpty}
        />
      ))}
    </div>
  );
}

export default Container;
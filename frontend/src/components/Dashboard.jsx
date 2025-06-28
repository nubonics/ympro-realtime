import React from "react";
import TaskCard from "./TaskCard";

// Helper to split tasks by type
function splitTasksByType(tasks = []) {
  return {
    HOOK: tasks.filter((t) => t.type === "HOOK"),
    PULL: tasks.filter((t) => t.type === "PULL"),
    BRING: tasks.filter((t) => t.type === "BRING"),
    OTHER: tasks.filter((t) => t.type !== "HOOK" && t.type !== "PULL" && t.type !== "BRING"),
  };
}

export default function Dashboard({
  workbasket,
  hostlerList,
  emptiesList,
  onTaskDrop,
  onTaskRemove,
  onDropEmpty,
  onCreateTask,
}) {
  return (
    <div className="dashboard-container">
      {/* --- TOP ROW: Workbasket | Recycle Bin | Create Task --- */}
      <div className="row first-row">
        {/* Workbasket */}
        <div className="column workbasket-column">
          <div className="workbasket-card">
            <h3>Workbasket</h3>
            <div className="workbasket-content">
              {workbasket.length === 0 ? (
                <div className="no-workbasket-tasks">No tasks</div>
              ) : (
                workbasket.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onRemove={onTaskRemove}
                    isDraggable
                  />
                ))
              )}
            </div>
          </div>
        </div>
        {/* Recycle Bin */}
        <div className="column recycle-bin-column">
          <div className="card">
            <h3>Recycle Bin</h3>
            <div style={{ minHeight: 60, textAlign: "center", opacity: 0.55, paddingTop: 28 }}>
              Drop here to delete
            </div>
          </div>
        </div>
        {/* Create Task */}
        <div className="column create-task-column">
          <div className="card create-task-card">
            <h3>Create Task</h3>
            <div style={{ opacity: 0.65, fontSize: 13 }}>
              [Create Task Form]
            </div>
          </div>
        </div>
      </div>

      {/* --- BOTTOM ROW: Hostlers | Empties --- */}
      <div className="row second-row">
        {/* Hostlers */}
        <div className="column hostlers-column">
          <div className="hostler-container">
            {hostlerList.length === 0 ? (
              <div className="empty-hostlers">No hostlers</div>
            ) : (
              hostlerList.map((hostler) => {
                // Split this hostler's tasks
                const { HOOK, PULL, BRING } = splitTasksByType(hostler.tasks);

                return (
                  <div className="hostler-card" key={hostler.id}>
                    <span className="task-count">{hostler.tasks.length}</span>
                    <h2>{hostler.name}</h2>
                    <div className="hostler-task-list">

                      {/* HOOKS (row above) */}
                      {HOOK.length > 0 && (
                        <div className="hostler-hook-row">
                          {HOOK.map((task) => (
                            <TaskCard
                              key={task.id}
                              task={task}
                              onRemove={onTaskRemove}
                              onDropEmpty={onDropEmpty}
                              isHostlerTask
                              isDraggable
                            />
                          ))}
                        </div>
                      )}

                      {/* PULL + BRING columns */}
                      <div className="hostler-pull-bring-row">
                        {/* PULL on left */}
                        <div className="hostler-pull-col">
                          <div className="hostler-type-label">PULL</div>
                          {PULL.length === 0 ? (
                            <div className="empty-hostlers" style={{ fontSize: "1em" }}>No pulls</div>
                          ) : (
                            PULL.map((task) => (
                              <TaskCard
                                key={task.id}
                                task={task}
                                onRemove={onTaskRemove}
                                onDropEmpty={onDropEmpty}
                                isHostlerTask
                                isDraggable
                              />
                            ))
                          )}
                        </div>
                        {/* BRING on right */}
                        <div className="hostler-bring-col">
                          <div className="hostler-type-label">BRING</div>
                          {BRING.length === 0 ? (
                            <div className="empty-hostlers" style={{ fontSize: "1em" }}>No brings</div>
                          ) : (
                            BRING.map((task) => (
                              <TaskCard
                                key={task.id}
                                task={task}
                                onRemove={onTaskRemove}
                                onDropEmpty={onDropEmpty}
                                isHostlerTask
                                isDraggable
                              />
                            ))
                          )}
                        </div>
                      </div>

                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
        {/* Empties */}
        <div className="column empties-column">
          <div className="card empties">
            <h3>Empties</h3>
            <div className="empties-vertical">
              {emptiesList.map((empty) => (
                <div key={empty.id} className="empty-box">
                  {empty.label}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
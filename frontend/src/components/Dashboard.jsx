// src/pages/Dashboard.jsx (wrap with ToastProvider; keeps your centered "No pulls/brings")
import React from "react";
import TaskCard from "../components/TaskCard";
import { ToastProvider } from "../components/ui/ToastProvider";

function splitTasksByType(tasks = []) {
  const arr = Array.isArray(tasks) ? tasks : [];
  const typeOf = (t) => String(t?.type || "").toLowerCase();
  return {
    HOOK: arr.filter((t) => typeOf(t) === "hook"),
    PULL: arr.filter((t) => typeOf(t) === "pull"),
    BRING: arr.filter((t) => typeOf(t) === "bring"),
    OTHER: arr.filter((t) => !["hook", "pull", "bring"].includes(typeOf(t))),
  };
}

const EmptyColMsg = ({ text, minHeight = 100 }) => (
  <div style={{ display:"flex",alignItems:"center",justifyContent:"center",minHeight,width:"100%",textAlign:"center",opacity:.65 }}>
    <span style={{ fontSize: "1em" }}>{text}</span>
  </div>
);

export default function Dashboard({
  workbasket = [],
  hostlerList = [],
  emptiesList = [],
  onTaskDrop = () => {},
  onTaskRemove = () => {},
  onDropEmpty = () => {},
  onCreateTask = () => {},
}) {
  const safeWorkbasket = Array.isArray(workbasket) ? workbasket : [];
  const safeHostlers = Array.isArray(hostlerList) ? hostlerList : [];
  const safeEmpties = Array.isArray(emptiesList) ? emptiesList : [];

  return (
    <ToastProvider>
      <div className="dashboard-container">
        <div className="row first-row">
          <div className="column workbasket-column">
            <div className="workbasket-card">
              <h3>Workbasket</h3>
              <div className="workbasket-content">
                {safeWorkbasket.length === 0 ? (
                  <div className="no-workbasket-tasks" style={{ textAlign: "center", opacity: 0.65, padding: 12 }}>
                    No tasks
                  </div>
                ) : (
                  safeWorkbasket.map((task) => (
                    <TaskCard
                      key={task?.id ?? `${task?.type ?? "task"}-${task?.door ?? ""}-${task?.trailer ?? ""}`}
                      task={task}
                      onRemove={onTaskRemove}
                      isDraggable
                    />
                  ))
                )}
              </div>
            </div>
          </div>

          <div className="column recycle-bin-column">
            <div className="card">
              <h3>Recycle Bin</h3>
              <div style={{ minHeight: 60, textAlign: "center", opacity: 0.55, paddingTop: 28 }}>
                Drop here to delete
              </div>
            </div>
          </div>

          <div className="column create-task-column">
            <div className="card create-task-card">
              <h3>Create Task</h3>
              <div style={{ opacity: 0.65, fontSize: 13 }}>[Create Task Form]</div>
            </div>
          </div>
        </div>

        <div className="row second-row">
          <div className="column hostlers-column">
            <div className="hostler-container">
              {safeHostlers.length === 0 ? (
                <div className="empty-hostlers" style={{ textAlign: "center", opacity: 0.65, padding: 12 }}>
                  No hostlers
                </div>
              ) : (
                safeHostlers.map((hostler) => {
                  const tasksArr = Array.isArray(hostler?.tasks) ? hostler.tasks : [];
                  const { HOOK, PULL, BRING } = splitTasksByType(tasksArr);
                  return (
                    <div className="hostler-card" key={hostler?.id ?? hostler?.name ?? Math.random()}>
                      <span className="task-count">{tasksArr.length}</span>
                      <h2>{hostler?.name ?? "Unknown"}</h2>
                      <div className="hostler-task-list">
                        {HOOK.length > 0 && (
                          <div className="hostler-hook-row">
                            {HOOK.map((task) => (
                              <TaskCard
                                key={task?.id ?? `${task?.type ?? "HOOK"}-${task?.door ?? ""}-${task?.trailer ?? ""}`}
                                task={task}
                                onRemove={onTaskRemove}
                                onDropEmpty={onDropEmpty}
                                isHostlerTask
                                isDraggable
                              />
                            ))}
                          </div>
                        )}

                        <div className="hostler-pull-bring-row">
                          <div className="hostler-pull-col">
                            <div className="hostler-type-label">PULL</div>
                            {PULL.length === 0 ? (
                              <EmptyColMsg text="No pulls" />
                            ) : (
                              PULL.map((task) => (
                                <TaskCard
                                  key={task?.id ?? `${task?.type ?? "PULL"}-${task?.door ?? ""}-${task?.trailer ?? ""}`}
                                  task={task}
                                  onRemove={onTaskRemove}
                                  onDropEmpty={onDropEmpty}
                                  isHostlerTask
                                  isDraggable
                                />
                              ))
                            )}
                          </div>

                          <div className="hostler-bring-col">
                            <div className="hostler-type-label">BRING</div>
                            {BRING.length === 0 ? (
                              <EmptyColMsg text="No brings" />
                            ) : (
                              BRING.map((task) => (
                                <TaskCard
                                  key={task?.id ?? `${task?.type ?? "BRING"}-${task?.door ?? ""}-${task?.trailer ?? ""}`}
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

          <div className="column empties-column">
            <div className="card empties">
              <h3>Empties</h3>
              <div className="empties-vertical">
                {safeEmpties.map((empty, idx) => (
                  <div key={empty?.id ?? empty?.label ?? idx} className="empty-box">
                    {empty?.label ?? "EMPTY"}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </ToastProvider>
  );
}

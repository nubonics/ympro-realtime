import React, { useState, useEffect, useRef } from "react";
import Sidebar from "./components/Sidebar";
import Container from "./components/Container";
import EmptiesContainer from "./components/EmptiesContainer";
import RecycleBin from "./components/RecycleBin";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { TASK_TYPES } from "./constants/taskTypes";
import "./styles.css";
import { buildTasksWS } from "./lib/ws";
import { mapTasksFromApi } from "./utils/mapFromApi";

const API_URL = import.meta.env.VITE_API_URL; // e.g. http://localhost:8000/api

const EMPTY_TASKS = [
  { label: "MTY PUP", type: TASK_TYPES.EMPTY },
  { label: "MTY LBX", type: TASK_TYPES.EMPTY },
  { label: "MTY 48 LG", type: TASK_TYPES.EMPTY },
  { label: "MTY RAIL", type: TASK_TYPES.EMPTY },
  { label: "MTY TP", type: TASK_TYPES.EMPTY },
];

function groupTasksByHostler(tasks) {
  const byHost = {};
  (Array.isArray(tasks) ? tasks : []).forEach((t) => {
    const h = t?.hostler || "Unassigned";
    (byHost[h] ||= []).push(t);
  });
  return Object.entries(byHost)
    .filter(([n]) => n !== "Unassigned")
    .map(([name, tasks]) => ({ name, tasks }));
}

export default function App() {
  const [allTasks, setAllTasks] = useState([]);
  const [recycleBin] = useState([]);
  const wsRef = useRef(null);
  const rollbackRef = useRef(null);

  useEffect(() => {
    let retry = 0;
    let alive = true;

    const connect = () => {
      const ws = new WebSocket(buildTasksWS());
      wsRef.current = ws;

      ws.onopen = () => {
        retry = 0;
        console.log("WS open");
      };

      ws.onmessage = (ev) => {
        try {
          const data = JSON.parse(ev.data);
          if (data && typeof data === "object" && data.type === "ping") return;
          if (Array.isArray(data)) {
            setAllTasks(mapTasksFromApi(data));
            return;
          }
          if (data && Array.isArray(data.tasks)) {
            setAllTasks(mapTasksFromApi(data.tasks));
            return;
          }
        } catch {}
      };

      ws.onerror = () => console.warn("WS error");

      ws.onclose = () => {
        if (!alive) return;
        const delay = Math.min(30000, 1000 * 2 ** retry++);
        console.warn("WS closed, reconnecting in", delay, "ms");
        setTimeout(connect, delay);
      };
    };

    connect();
    return () => {
      alive = false;
      try { wsRef.current?.close(); } catch {}
    };
  }, []);

  const workbasket = (allTasks || []).filter((t) => !t?.hostler);
  const hostlerGroups = groupTasksByHostler(allTasks || []);

  const handleDropEmpty = async () => {};
  const handleDropHostlerTask = async () => {};
  const handleDropToWorkbasket = async () => {};

  // drag-to-delete: optimistic remove, POST to backend, rollback on failure
  const handleDropRecycle = async (task) => {
    const id = task?.id ?? task?.case_id;
    if (!id) return;

    setAllTasks((prev) => {
      rollbackRef.current = prev;
      return prev.filter((t) => (t.id ?? t.case_id) !== id);
    });

    try {
      const res = await fetch(`${API_URL}/delete-task`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ case_id: id }),
      });
      if (!res.ok) throw new Error(`Delete failed: ${res.status}`);
      // backend should broadcast a fresh snapshot over WS; optimistic state already applied
    } catch (e) {
      // rollback if delete failed
      if (rollbackRef.current) setAllTasks(rollbackRef.current);
      console.error(e);
    } finally {
      rollbackRef.current = null;
    }
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="layout-root">
        <Sidebar />
        <main className="main-board">
          <div className="empties-recycle-row">
            <EmptiesContainer emptyTasks={EMPTY_TASKS} />
            <div className="recycle-bin-top">
              <RecycleBin onDropRecycle={handleDropRecycle} tasks={recycleBin} />
            </div>
          </div>
          <div className="board">
            <Container
              title="Workbasket"
              tasks={workbasket}
              colorClass="workbasket-container"
              onDropHostlerTask={handleDropToWorkbasket}
              onDropEmpty={handleDropEmpty}
              isWorkbasket
            />
            {hostlerGroups.map(({ name, tasks }) => (
              <Container
                key={name}
                title={name}
                tasks={tasks}
                colorClass="hostler-container"
                isHostlerContainer
                onDropEmpty={handleDropEmpty}
                onDropHostlerTask={handleDropHostlerTask}
              />
            ))}
          </div>
        </main>
      </div>
    </DndProvider>
  );
}

import React, { useState, useEffect, useRef } from "react";
import { toast } from "react-toastify";
import Sidebar from "./components/Sidebar";
import Container from "./components/Container";
import EmptiesContainer from "./components/EmptiesContainer";
import RecycleBin from "./components/RecycleBin";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { TASK_TYPES } from "./constants/taskTypes";
import { validateTask } from "./utils/api";
import "./styles.css";

// Environment variables for Vite
const USE_WS = import.meta.env.VITE_USE_WS === "true";
const API_URL = import.meta.env.VITE_API_URL;

const EMPTY_TASKS = [
  { label: "MTY PUP", type: TASK_TYPES.EMPTY },
  { label: "MTY LBX", type: TASK_TYPES.EMPTY },
  { label: "MTY 48 LG", type: TASK_TYPES.EMPTY },
  { label: "MTY RAIL", type: TASK_TYPES.EMPTY },
  { label: "MTY TP", type: TASK_TYPES.EMPTY },
];

function groupTasksByHostler(tasks) {
  const hostlerMap = {};
  tasks.forEach(task => {
    const hostler = task.hostler || "Unassigned";
    if (!hostlerMap[hostler]) hostlerMap[hostler] = [];
    hostlerMap[hostler].push(task);
  });
  return Object.entries(hostlerMap)
    .filter(([name]) => name !== "Unassigned")
    .map(([name, tasks]) => ({ name, tasks }));
}

function App() {
  const [allTasks, setAllTasks] = useState([]);
  const [recycleBin, setRecycleBin] = useState([]);
  const wsRef = useRef(null);

  // WebSocket connection if enabled
  useEffect(() => {
    if (!USE_WS) return;

    let ws;
    try {
      ws = new window.WebSocket("ws://localhost:8052/ws/tasks");
      wsRef.current = ws;
      ws.onopen = () => {
        console.log("WebSocket connected");
      };
      ws.onmessage = (event) => {
        console.log("WS message received", event.data); // for debugging!
        try {
          const data = JSON.parse(event.data);
          if (Array.isArray(data)) setAllTasks(data);
        } catch (err) {
          console.error("WS message parse error:", err);
        }
      };
      ws.onerror = (err) => {
        console.error("WebSocket error:", err);
      };
      ws.onclose = (event) => {
        console.warn("WebSocket closed:", event);
      };
    } catch (err) {
      console.error("WebSocket connection failed:", err);
    }
    return () => { if (ws) ws.close(); };
  }, []);

  // HTTP polling for tasks as fallback (when WS not enabled)
  useEffect(() => {
    if (USE_WS) return; // Skip polling if using WS

    let intervalId;
    const fetchTasks = async () => {
      try {
        const res = await fetch(`${API_URL}/external-tasks`);
        const data = await res.json();
        setAllTasks(Array.isArray(data) ? data : (Array.isArray(data.tasks) ? data.tasks : []));
      } catch (err) {
        console.error("Polling error:", err);
      }
    };
    fetchTasks();
    intervalId = setInterval(fetchTasks, 5000);

    return () => clearInterval(intervalId);
  }, []);

  const workbasket = allTasks.filter(t => !t.hostler);
  const hostlerGroups = groupTasksByHostler(allTasks);

    const handleDropEmpty = async (emptyTask, pullTask) => {
      const isWorkbasketPull = !pullTask.hostler;

      const bringTask = {
        type: "bring",
        id: `bring-${Date.now()}`,
        door: pullTask.door,
        trailer: emptyTask.label,
        zoneType: pullTask.zoneType,
        zoneLocation: pullTask.zoneLocation,
        note: `From pull of ${pullTask.trailer}`,
        priority: "normal",
        hostler: isWorkbasketPull ? undefined : pullTask.hostler,
      };

      try {
        const res = await fetch(`${API_URL}/create-task`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(bringTask),
        });
        if (!res.ok) {
          const errorData = await res.json();
          alert(errorData.message || "Not allowed by rules.");
        }
      } catch (err) {
        alert("An error occurred: " + (err.message || err));
      }
    };

  // ---- Handler: Move a task to a different hostler ----
  const handleDropHostlerTask = async (task, newHostler) => {
    await fetch(`${API_URL}/update-task-hostler`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: task.id, hostler: newHostler }),
    });
  };

  // ---- Handler: Move a task to the workbasket (unassign hostler) ----
  const handleDropToWorkbasket = async (task) => {
    await fetch(`${API_URL}/update-task-hostler`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: task.id, hostler: "" })
    });
  };

  // ---- Handler: Delete task ----
  const handleDropRecycle = async (task) => {
    setAllTasks(tasks => tasks.filter(t => t.id !== task.id));
    toast.success("Task deleted!");
    await fetch(`${API_URL}/delete-task`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: task.id }),
    });
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="layout-root">
        <Sidebar />
        <main className="main-board">
          {/* Empties and recycle bin row */}
          <div className="empties-recycle-row">
            <EmptiesContainer emptyTasks={EMPTY_TASKS} />
            <div className="recycle-bin-top">
              <RecycleBin onDropRecycle={handleDropRecycle} tasks={recycleBin} />
            </div>
          </div>
          <div className="board">
            {/* WORKBASKET ALWAYS FIRST/LEFT */}
            <Container
              title="Workbasket"
              tasks={workbasket}
              colorClass="workbasket-container"
              onDropHostlerTask={handleDropToWorkbasket}
              onDropEmpty={handleDropEmpty}
              isWorkbasket
            />
            {/* HOSTLERS FILL OUT TO THE RIGHT */}
            {hostlerGroups.map(({ name, tasks }) => (
              <Container
                key={name}
                title={name}
                tasks={tasks}
                colorClass="hostler-container"
                isHostlerContainer={true}
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

export default App;
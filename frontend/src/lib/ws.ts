// frontend/src/lib/ws.ts
export function buildTasksWS(): string {
  const base =
    import.meta.env.VITE_WS_URL ||
    ((location.protocol === "https:" ? "wss://" : "ws://") + location.hostname + ":8000");
  const token = import.meta.env.VITE_WS_TOKEN;
  return `${base}/ws/tasks${token ? `?token=${encodeURIComponent(token)}` : ""}`;
}

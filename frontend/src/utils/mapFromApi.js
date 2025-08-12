// frontend/src/utils/mapFromApi.js
export function mapTasksFromApi(arr) {
  const list = Array.isArray(arr) ? arr : [];
  return list.map((t) => ({
    id: String(t?.case_id ?? ""),
    type: String(t?.yard_task_type ?? "").toLowerCase(),
    door: t?.door ?? null,
    trailer: t?.trailer ?? "",
    zoneType: t?.zoneType ?? "",
    zoneLocation: t?.zoneLocation ?? "",
    note: t?.note ?? "",
    priority: String(t?.priority ?? "normal").toLowerCase(),
    hostler: t?.assigned_to ? String(t.assigned_to) : "",
    _raw: t,
  }));
}

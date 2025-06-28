// Utility for frontend to validate tasks using backend rules

export async function validateTask(task) {
  const resp = await fetch("/api/validate-task", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task),
  });
  if (!resp.ok) {
    const data = await resp.json();
    return { allowed: false, reason: data.reason || "Validation error" };
  }
  return await resp.json();
}
// Example API file; update baseURL as needed for your FastAPI backend

import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8052/api", // Change this to your FastAPI endpoint
});

// Example functions:
// export const fetchHostlerTasks = () => API.get("/hostler-tasks");
// export const updateHostlerTasks = (data) => API.post("/hostler-tasks", data);

export default API;
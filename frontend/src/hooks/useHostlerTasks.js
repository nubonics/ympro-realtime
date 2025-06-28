import { useEffect, useRef } from "react";
import axios from "axios";

// Define syncHostlerTasks here, or import it if it's in another file
function syncHostlerTasks(localTasks, externalTasks) {
  // ...your logic here...
  return externalTasks; // simplified for demo, use your real merging/filtering logic
}

export default function useHostlerTasks(localTasks, setLocalTasks) {
  const intervalRef = useRef();

  useEffect(() => {
    const poll = async () => {
      try {
        const res = await axios.get("/api/external-tasks");
        console.log("Fetched external tasks:", res.data);
        const externalTasks =
          Array.isArray(res.data)
            ? res.data
            : Array.isArray(res.data.tasks)
              ? res.data.tasks
              : [];
        setLocalTasks((prev) => syncHostlerTasks(prev, externalTasks));
      } catch (err) {
        console.error("Polling error:", err);
      }
    };

    poll();
    intervalRef.current = setInterval(poll, 5000);

    return () => clearInterval(intervalRef.current);
  }, [setLocalTasks]);
}
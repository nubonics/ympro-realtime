# ympro-realtime Backend

This backend is responsible for **real-time task management and orchestration** for the YMPro (Yard Management) system. It is primarily written in Python, with supporting code in JavaScript, CSS, and HTML.

---

## 🧩 **Main Components**

### 1. **Poller**
- **Purpose:** Periodically polls an external API to fetch the latest workbasket tasks and hostler statuses.
- **Features:**
  - Polls at a configurable interval (via Redis or env).
  - Fetches workbasket tasks and per-hostler tasks.
  - Fetches and caches detailed task info.
  - Applies business rules and validation.
  - Automatically attempts to patch or delete invalid tasks via remote API.
  - Aggregates a unified view of all tasks and hostlers.
  - Stores the latest result in Redis, only if there are changes.
  - Triggers downstream handlers (e.g., WebSocket push, notifications, etc).
  - Audit logs all critical actions.

### 2. **API Layer**
- **Purpose:** Handles all interactions with the external YMPro system.
- **Features:**
  - Provides async methods for fetching, patching, and deleting tasks.
  - Centralizes error handling and logging for remote calls.

### 3. **Caching**
- **Purpose:** Reduces redundant API calls and speeds up polling by caching task details in Redis.
- **Features:**
  - Task details are cached after first fetch.
  - Cache is updated on patch and cleared on delete.

### 4. **Audit Logging**
- **Purpose:** Tracks all patches and deletions for traceability.
- **Features:**
  - Logs every patch, deletion, and error to a file with timestamps and reasons.

### 5. **Business Rules & Validation**
- **Purpose:** Ensures only valid, actionable tasks are kept.
- **Features:**
  - Modular rules for task validation.
  - Fixable tasks are patched, unfixable ones are deleted.

---

## 🚦 **Current TODO / Roadmap**

- [ ] **WebSocket Updates:** Integrate with frontend via WebSockets for live updates.
- [ ] **Admin/Dev API:** Expose endpoints for debugging, manual task management, health checks.
- [ ] **Metrics & Monitoring:** Add Prometheus/Grafana integration for performance and health.
- [ ] **Testing:** Expand unit/integration test coverage, especially for API and polling logic.
- [ ] **Error Recovery:** More robust retry logic and backoff for external API failures.
- [ ] **Task Type Support:** Extend support for new task types as YMPro evolves.
- [ ] **Documentation:** Improve and expand developer docs, including setup and API contracts.
- [ ] **CI/CD Integration:** Automate tests and deployments.

---

## 🛠️ **Tech Stack**

- **Python** (backend core, polling, business logic)
- **Redis** (caching, state propagation)
- **JavaScript/HTML/CSS** (frontend, not covered here)

---

## 🗂️ **Code Structure**

```
poller/
├── poller.py        # Main orchestration loop
├── api.py           # External API interactions
├── cache.py         # Redis caching helpers
├── audit.py         # Audit logging
├── utils.py         # Miscellaneous helpers
├── models.py        # Data models (Task, Hostler, etc)
├── rules/           # Business rules and validation
├── storage.py       # Redis storage/propagation helpers
```

---

## 📚 **How It Works (High Level)**

1. **Polling:** `poller.py` runs a loop that fetches all task data from the external API.
2. **Validation:** Each task is validated and, if possible, auto-fixed or deleted.
3. **Aggregation:** Valid tasks are split into workbasket and hostler buckets.
4. **Caching:** Task details are cached for performance.
5. **Update Propagation:** If any change is detected, the result is stored in Redis and downstream handlers are notified.
6. **Audit Trail:** All mutations are logged for traceability.

---

## 👩‍💻 **How to Contribute / Work on Next**

- Use this README to track backend responsibilities and next steps.
- **Update the TODO section** as you complete features or find new requirements.
- Consider writing/updating docstrings and comments as you refactor modules.
- Ping @nubonics for architecture or roadmap discussions!

---
# YMPro Frontend

Frontend for FastAPI backend with drag-and-drop containers.

## Features

- Hostler card, Workbasket, Recycle Bin, and Empties containers
- Drag-and-drop tasks between containers (with business logic enforced)
- Unlimited supply of [MTY LBX, MTY PUP] in Empties
- Built with React, Vite, react-dnd

## Getting Started

### 1. Install dependencies

```sh
npm install
```

### 2. Run the development server

```sh
npm run dev
```

App runs by default at [http://localhost:5173](http://localhost:5173).

### 3. Connect to FastAPI

- Update `src/api/backend.js` with your FastAPI backend URL.
- Replace static initial data in `src/App.jsx` with API calls.

## File structure

- `src/components/` — React components
- `src/api/` — API helpers
- `src/styles.css` — Basic styles

## Customization

- Add more containers or task types as needed.
- Connect to your backend for dynamic data.

---

**MIT License**
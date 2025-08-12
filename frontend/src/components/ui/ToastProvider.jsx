// src/components/ui/ToastProvider.jsx
import React, { createContext, useCallback, useContext, useMemo, useState, useEffect } from "react";
import "./toast.css";

const ToastCtx = createContext({ push: () => {} });

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const push = useCallback((message, type = "success", ttl = 2200) => {
    const id = Math.random().toString(36).slice(2);
    setToasts(t => [...t, { id, message, type }]);
    setTimeout(() => setToasts(t => t.filter(x => x.id !== id)), ttl);
  }, []);

  const value = useMemo(() => ({ push }), [push]);

  useEffect(() => {
    const onCopy = e => {
      // optional: intercept Cmd/Ctrl+C on focused elements if you want global feedback
    };
    window.addEventListener("copy", onCopy);
    return () => window.removeEventListener("copy", onCopy);
  }, []);

  return (
    <ToastCtx.Provider value={value}>
      {children}
      <div className="toast-container" aria-live="polite" aria-atomic="true">
        {toasts.map(t => (
          <div key={t.id} className={`toast ${t.type === "error" ? "toast-error" : "toast-success"}`}>
            {t.message}
          </div>
        ))}
      </div>
    </ToastCtx.Provider>
  );
}

export function useToast() {
  return useContext(ToastCtx);
}

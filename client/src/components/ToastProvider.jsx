import { createContext, useContext, useMemo, useState, useCallback, useEffect } from "react";

const ToastCtx = createContext({ notify: () => {} });

export function useToast() {
  return useContext(ToastCtx);
}

export default function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const notify = useCallback((msg, type = "info", ttl = 3500) => {
    const id = crypto.randomUUID?.() || String(Date.now());
    setToasts((t) => [...t, { id, msg, type }]);
    setTimeout(() => setToasts((t) => t.filter(x => x.id !== id)), ttl);
  }, []);

  const value = useMemo(() => ({ notify }), [notify]);

  return (
    <ToastCtx.Provider value={value}>
      {children}
      <div style={{
        position:"fixed", right:16, bottom:16, display:"grid", gap:8, zIndex:1000
      }}>
        {toasts.map(t => (
          <div key={t.id} style={{
            padding:"10px 12px", borderRadius:10,
            background: t.type==="error" ? "#ffe8e8" : t.type==="success" ? "#e8ffe9" : "#eef2ff",
            color: t.type==="error" ? "#b00020" : t.type==="success" ? "#0a7c2f" : "#1c2b8f",
            minWidth: 220, boxShadow:"0 6px 20px rgba(0,0,0,.08)"
          }}>
            {t.msg}
          </div>
        ))}
      </div>
    </ToastCtx.Provider>
  );
}

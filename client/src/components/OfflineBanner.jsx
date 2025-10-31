import { useEffect, useState } from "react";

export default function OfflineBanner() {
  const [online, setOnline] = useState(navigator.onLine);
  useEffect(() => {
    const on = () => setOnline(true);
    const off = () => setOnline(false);
    window.addEventListener("online", on);
    window.addEventListener("offline", off);
    return () => { window.removeEventListener("online", on); window.removeEventListener("offline", off); };
  }, []);
  if (online) return null;
  return (
    <div style={{ background:"#fff3cd", color:"#7a5b00", padding:"8px 0", textAlign:"center" }}>
      You’re offline. Some actions may fail.
    </div>
  );
}

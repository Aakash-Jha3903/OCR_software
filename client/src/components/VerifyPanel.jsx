// src/components/VerifyPanel.jsx
import { useState } from "react";

export default function VerifyPanel({ onVerify, loading }) {
  const [threshold, setThreshold] = useState(80);

  return (
    <div className="card" style={{ marginTop: 16 }}>
      <div style={{ display:"flex", alignItems:"flex-end", gap:12 }}>
        <div style={{ width:160 }}>
          <label className="label">Signature Threshold</label>
          <input
            type="number"
            min={1}
            max={100}
            className="input"
            value={threshold}
            onChange={(e) => setThreshold(e.target.value)}
          />
        </div>
        <button
          className="btn"
          disabled={loading}
          onClick={() => onVerify?.(Number(threshold))}
        >
          {loading ? "Verifying..." : "Verify Cheque"}
        </button>
      </div>
      <div style={{ fontSize:12, color:"#666", marginTop:8 }}>
        Tip: Try 70–90 depending on your signature quality.
      </div>
    </div>
  );
}

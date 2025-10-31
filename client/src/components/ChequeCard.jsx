// src/components/ChequeCard.jsx
import { Link } from "react-router-dom";
import StatTag from "./StatTag";

export default function ChequeCard({ cheque }) {
  const img = cheque?.image?.startsWith("http")
    ? cheque.image
    : `${import.meta.env.VITE_API_BASE}${cheque.image}`;

  return (
    <div className="card">
      <div className="row" style={{ alignItems:"center" }}>
        <img
          src={img}
          alt="cheque"
          style={{ width: 160, height: 100, objectFit: "cover", borderRadius: 8 }}
        />
        <div style={{ flex: 1 }}>
          <div style={{ display:"flex", alignItems:"center", gap:8 }}>
            <strong>Cheque #{cheque.id}</strong>
            <StatTag status={cheque.status} />
          </div>
          <div style={{ color:"#666", marginTop:4 }}>
            ₹ {cheque.amount_digits ?? "—"} • {cheque.payee || "—"}
          </div>
        </div>
        <Link to={`/cheques/${cheque.id}`} className="btn outline">View</Link>
      </div>
    </div>
  );
}

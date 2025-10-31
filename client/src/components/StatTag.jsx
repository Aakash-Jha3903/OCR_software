// src/components/StatTag.jsx
export default function StatTag({ status }) {
  if (!status) return null;
  const s = status.toUpperCase();
  const cls =
    s.includes("SUCCESS") || s.includes("MATCH") ? "success" :
    s.includes("FAIL") || s.includes("MISMATCH") ? "fail" :
    "warn";
  return <span className={`badge ${cls}`}>{status}</span>;
}

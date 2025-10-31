export default function AuditTimeline({ items = [] }) {
  if (!items.length) return (
    <div className="card"><em>No audit entries.</em></div>
  );

  return (
    <div className="card">
      <h3 style={{ marginTop: 0 }}>Audit Timeline</h3>
      <ul style={{ listStyle:"none", padding:0, margin:0 }}>
        {items.map((a) => (
          <li key={a.id} style={{ padding:"8px 0", borderBottom:"1px solid #f2f2f2" }}>
            <div><strong>{a.old_status || "—"}</strong> → <strong>{a.new_status}</strong></div>
            {a.message ? <div style={{ color:"#666", fontSize:13 }}>{a.message}</div> : null}
            <div style={{ color:"#999", fontSize:12, marginTop:2 }}>
              {new Date(a.created_at).toLocaleString()}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

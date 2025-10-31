export default function FilterBar({
  values, onChange,
  statusOptions = [], decisionOptions = []
}) {
  function set(k, v) { onChange({ ...values, [k]: v }); }
  return (
    <div className="card" style={{ marginBottom: 16 }}>
      <div className="row" style={{ alignItems:"flex-end" }}>
        {statusOptions.length > 0 && (
          <div style={{ width:220 }}>
            <label className="label">Status</label>
            <select className="select" value={values.status || ""} onChange={(e)=>set("status", e.target.value)}>
              <option value="">All</option>
              {statusOptions.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
        )}

        {decisionOptions.length > 0 && (
          <div style={{ width:220 }}>
            <label className="label">Decision</label>
            <select className="select" value={values.decision || ""} onChange={(e)=>set("decision", e.target.value)}>
              <option value="">All</option>
              {decisionOptions.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
        )}

        <div style={{ width:200 }}>
          <label className="label">Payee</label>
          <input className="input" value={values.payee || ""} onChange={(e)=>set("payee", e.target.value)} />
        </div>
        <div style={{ width:160 }}>
          <label className="label">MICR</label>
          <input className="input" value={values.micr || ""} onChange={(e)=>set("micr", e.target.value)} />
        </div>
        <div style={{ width:140 }}>
          <label className="label">Min Amount</label>
          <input className="input" type="number" value={values.min_amount || ""} onChange={(e)=>set("min_amount", e.target.value)} />
        </div>
        <div style={{ width:140 }}>
          <label className="label">Max Amount</label>
          <input className="input" type="number" value={values.max_amount || ""} onChange={(e)=>set("max_amount", e.target.value)} />
        </div>

        <div style={{ marginLeft:"auto", display:"flex", gap:8 }}>
          <button className="btn outline" onClick={()=>onChange({})}>Clear</button>
        </div>
      </div>
    </div>
  );
}

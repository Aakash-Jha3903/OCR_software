import { useEffect, useState } from "react";
import { listVerifications } from "../services/cheques";
import { Link } from "react-router-dom";
import { useToast } from "../components/ToastProvider";
import Skeleton from "../components/Skeleton";
import FilterBar from "../components/FilterBar";

const DECISIONS = ["PASS","FAIL","MANUAL"];

export default function VerificationListPage() {
  const [rows, setRows] = useState(null);
  const [filters, setFilters] = useState({});
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(0);
  const { notify } = useToast();
  const pageSize = 12;

  async function fetchList() {
    try {
      setRows(null);
      const params = { page, page_size: pageSize, ...filters };
      const data = await listVerifications(params);
      setRows(data.results || []);
      setCount(data.count || 0);
    } catch (e) {
      notify(e.message, "error");
      setRows([]);
      setCount(0);
    }
  }

  useEffect(() => { fetchList(); /* eslint-disable */ }, [JSON.stringify(filters), page]);

  return (
    <div className="container">
      <h2>Verifications</h2>

      <FilterBar
        values={filters}
        onChange={(vals)=>{ setFilters(vals); setPage(1); }}
        decisionOptions={DECISIONS}
      />

      {rows === null ? (
        <div className="card">
          {Array.from({length:6}).map((_,i)=>(
            <div key={i} style={{ padding:"8px 0", borderBottom:"1px solid #f2f2f2" }}>
              <Skeleton h={14} />
            </div>
          ))}
        </div>
      ) : (
        <>
          <div className="card">
            <table width="100%" cellPadding="8" style={{ borderCollapse:"collapse" }}>
              <thead>
                <tr style={{ textAlign:"left", borderBottom:"1px solid #eee" }}>
                  <th>ID</th><th>Cheque</th><th>Decision</th>
                  <th>Similarity</th><th>Threshold</th><th>Message</th><th>View</th>
                </tr>
              </thead>
              <tbody>
                {rows.map(r => (
                  <tr key={r.id} style={{ borderBottom:"1px solid #f2f2f2" }}>
                    <td>{r.id}</td>
                    <td>#{r.cheque?.id} • {r.cheque?.status}</td>
                    <td>{r.decision}</td>
                    <td>{r.sign_similarity ?? "—"}%</td>
                    <td>{r.sign_threshold}</td>
                    <td>{r.message ?? "—"}</td>
                    <td><Link to={`/cheques/${r.cheque?.id}`} className="btn outline">Open</Link></td>
                  </tr>
                ))}
                {rows.length === 0 && (
                  <tr><td colSpan={7}><em>No verifications found.</em></td></tr>
                )}
              </tbody>
            </table>
          </div>

          <div style={{ display:"flex", justifyContent:"space-between", marginTop:16 }}>
            <div>Total: {count}</div>
            <div style={{ display:"flex", gap:8 }}>
              <button className="btn outline" disabled={page<=1} onClick={()=>setPage(p=>p-1)}>Prev</button>
              <button className="btn" disabled={(page * pageSize) >= count} onClick={()=>setPage(p=>p+1)}>Next</button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

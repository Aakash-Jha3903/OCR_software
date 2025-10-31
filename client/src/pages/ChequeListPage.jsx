import { useEffect, useState } from "react";
import { listCheques } from "../services/cheques";
import ChequeCard from "../components/ChequeCard";
import { useToast } from "../components/ToastProvider";
import Skeleton from "../components/Skeleton";
import FilterBar from "../components/FilterBar";

const STATUS = [ "UPLOADED","OCR_COMPLETE","ACCOUNT_FOUND","FIELD_MISMATCH",
  "SIGN_PENDING","SIGN_MATCH","SIGN_MISMATCH","DEBIT_SUCCESS","DEBIT_FAILED" ];

export default function ChequeListPage() {
  const [rows, setRows] = useState(null); // null -> loading
  const [filters, setFilters] = useState({});
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(0);
  const { notify } = useToast();
  const pageSize = 12;

  async function fetchList() {
    try {
      setRows(null);
      const params = { page, page_size: pageSize, ...filters };
      const data = await listCheques(params);
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
      <h2>Cheques</h2>

      <FilterBar
        values={filters}
        onChange={(vals)=>{ setFilters(vals); setPage(1); }}
        statusOptions={STATUS}
      />

      {rows === null ? (
        <div className="row">
          {Array.from({length:6}).map((_,i)=>(
            <div key={i} className="card" style={{ width: "calc(33% - 10px)" }}>
              <Skeleton h={100} />
              <Skeleton h={14} style={{ marginTop:12, width:"60%" }} />
              <Skeleton h={12} style={{ marginTop:8, width:"40%" }} />
            </div>
          ))}
        </div>
      ) : (
        <>
          <div className="row">
            {rows.map((c)=> <ChequeCard key={c.id} cheque={c} />)}
            {rows.length === 0 && <div className="card" style={{ width:"100%" }}>No cheques found.</div>}
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

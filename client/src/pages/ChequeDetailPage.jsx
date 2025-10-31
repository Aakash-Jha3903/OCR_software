import { useEffect, useState, useMemo } from "react";
import { getCheque, verifyCheque } from "../services/cheques";
import { useParams } from "react-router-dom";
import StatTag from "../components/StatTag";
import VerifyPanel from "../components/VerifyPanel";
import { useToast } from "../components/ToastProvider";
import Skeleton from "../components/Skeleton";
import Spinner from "../components/Spinner";
import { getChequeAudits } from "../services/cheques";
import AuditTimeline from "../components/AuditTimeline";

export default function ChequeDetailPage() {
  const { id } = useParams();

  const [cheque, setCheque] = useState(null);
  const [verif, setVerif] = useState(null);
  const [loading, setLoading] = useState(true);
  const [verifying, setVerifying] = useState(false);
  const [err, setErr] = useState("");
  const { notify } = useToast();

  const img = useMemo(() => {
    if (!cheque?.image) return null;
    return cheque.image.startsWith("http")
      ? cheque.image
      : `${import.meta.env.VITE_API_BASE}${cheque.image}`;
  }, [cheque]);

  async function fetchCheque() {
    setErr("");
    setLoading(true);
    try {
      const c = await getCheque(id);
      setCheque(c);
    } catch (e) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchCheque(); /* eslint-disable */ }, [id]);

  async function doVerify(threshold) {
    setVerifying(true);
    setErr("");
    try {
      const v = await verifyCheque(id, threshold);
      setVerif(v);
      notify(`Verified: ${v.decision}`, v.decision === "PASS" ? "success" : "info");
      await fetchCheque();
    } catch (e) {
      setErr(e.message);
      notify(e.message, "error");
    } finally {
      setVerifying(false);
    }
  }
  const [audits, setAudits] = useState([]);
  async function fetchAudits() {
    try {
      const list = await getChequeAudits(id);
      setAudits(list || []);
    } catch (e) {
      // silent fail – audits are optional
    }
  }

  useEffect(() => {
    fetchCheque();
    fetchAudits();
    // eslint-disable-next-line
  }, [id]);

  async function doVerify(threshold) {
    setVerifying(true);
    setErr("");
    try {
      const v = await verifyCheque(id, threshold);
      setVerif(v);
      notify(`Verified: ${v.decision}`, v.decision === "PASS" ? "success" : "info");
      await fetchCheque();
      await fetchAudits(); // <-- refresh timeline
    } catch (e) {
      setErr(e.message);
      notify(e.message, "error");
    } finally {
      setVerifying(false);
    }
  }

  return (
    <div className="container">
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2 style={{ margin: 0 }}>Cheque #{id}</h2>
        {cheque?.status && <StatTag status={cheque.status} />}
      </div>

      {loading ? (
        <div className="grid-2" style={{ marginTop: 12 }}>
          <div className="card"><Skeleton h={240} r={12} /></div>
          <div>
            <div className="card" style={{ marginBottom: 16 }}><Skeleton h={80} /></div>
            <div className="card"><Skeleton h={160} /></div>
          </div>
        </div>
      ) : err ? (
        <div className="card" style={{ marginTop: 12 }}>
          <div className="badge fail">{err}</div>
          <div style={{ marginTop: 12 }}>
            <button className="btn" onClick={fetchCheque}>Retry</button>
          </div>
        </div>
      ) : cheque ? (
        <div className="grid-2" style={{ marginTop: 12 }}>
          <div className="card">
            {img && <img src={img} alt="cheque" style={{ width: "100%", borderRadius: 8 }} />}
            <div style={{ marginTop: 12, color: "#666" }}>
              Uploaded: {new Date(cheque.uploaded_at).toLocaleString()}
            </div>
            <div style={{ marginTop: 12 }}>
              <div><strong>Payee:</strong> {cheque.payee || "—"}</div>
              <div><strong>Amount (₹):</strong> {cheque.amount_digits ?? "—"}</div>
              <div><strong>MICR:</strong> {cheque.micr || "—"}</div>
            </div>
          </div>

          <div>
            <VerifyPanel onVerify={doVerify} loading={verifying} />

            {verif && (
              <div className="card" style={{ marginTop: 16 }}>
                <h3 style={{ marginTop: 0 }}>Verification Result</h3>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                  <div><strong>Decision:</strong> {verif.decision}</div>
                  <div><strong>Similarity:</strong> {verif.sign_similarity ?? "—"}%</div>
                  <div><strong>Threshold:</strong> {verif.sign_threshold}</div>
                  <div><strong>Message:</strong> {verif.message || "—"}</div>
                  <div><strong>Debit Amount:</strong> {verif.debit_amount ?? "—"}</div>
                  <div><strong>Post Balance:</strong> {verif.debit_post_balance ?? "—"}</div>
                </div>
              </div>
            )}

            {cheque?.ocr_raw && Object.keys(cheque.ocr_raw).length > 0 && (
              <div className="card" style={{ marginTop: 16 }}>
                <h3 style={{ marginTop: 0 }}>OCR (raw)</h3>
                <pre style={{ whiteSpace: "pre-wrap", margin: 0 }}>
                  {JSON.stringify(cheque.ocr_raw, null, 2)}
                </pre>


                {<div style={{ marginTop: 16 }}>
                  <AuditTimeline items={audits} />
                </div>}


              </div>
            )}

            {verifying && (
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 12 }}>
                <Spinner /> <span>Processing cheque…</span>
              </div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
}

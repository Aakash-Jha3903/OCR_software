// src/pages/OnboardingPage.jsx
import { useEffect, useState } from "react";
import { apiGetMe, apiPatchMe, apiUpsertMyBank } from "../services/auth_api";
import { useToast } from "../components/ToastProvider";
import { useNavigate } from "react-router-dom";

export default function OnboardingPage() {
  const { notify } = useToast();
  const nav = useNavigate();

  const [me, setMe] = useState(null);
  const [saving, setSaving] = useState(false);

  // profile fields
  const [fullName, setN] = useState("");
  const [phone, setPhone] = useState("");

  // bank fields
  const [bankId, setBankId] = useState("");
  const [ifsc, setIfsc] = useState("");
  const [micr, setMicr] = useState("");
  const [accountNumber, setAcc] = useState("");
  const [holderName, setHolderName] = useState("");

  const [signatureFile, setSignatureFile] = useState(null);
  const [cancelledFile, setCancelledFile] = useState(null);

  async function loadMe() {
    try {
      const data = await apiGetMe();
      setMe(data);
      setN(data?.full_name || "");
      setPhone(data?.phone || "");
      // if your /me returns bank info, you can prefill here
    } catch (e) {
      notify(e.message, "error");
    }
  }

  useEffect(() => { loadMe(); /* eslint-disable */ }, []);

  async function saveProfile(e) {
    e.preventDefault();
    setSaving(true);
    try {
      await apiPatchMe({ full_name: fullName, phone });
      await apiUpsertMyBank({
        bank_id: bankId || undefined,
        ifsc, micr,
        account_number: accountNumber,
        holder_name: holderName,
        signature_file: signatureFile,
        cancelled_cheque_file: cancelledFile,
      });
      notify("Details saved", "success");
      nav("/upload");
    } catch (e2) {
      notify(e2.message, "error");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="container">
      <h2>Complete your details</h2>
      <form className="card" onSubmit={saveProfile}>
        <h3>Personal</h3>
        <div className="grid-2">
          <div>
            <label className="label">Full Name</label>
            <input className="input" value={fullName} onChange={(e)=>setN(e.target.value)} />
          </div>
          <div>
            <label className="label">Phone</label>
            <input className="input" value={phone} onChange={(e)=>setPhone(e.target.value)} />
          </div>
        </div>

        <h3 style={{ marginTop: 24 }}>Bank details</h3>
        <div className="grid-2">
          <div>
            <label className="label">Bank (ID)</label>
            <input className="input" placeholder="e.g. 1" value={bankId} onChange={(e)=>setBankId(e.target.value)} />
          </div>
          <div>
            <label className="label">IFSC</label>
            <input className="input" value={ifsc} onChange={(e)=>setIfsc(e.target.value)} />
          </div>
          <div>
            <label className="label">MICR</label>
            <input className="input" value={micr} onChange={(e)=>setMicr(e.target.value)} />
          </div>
          <div>
            <label className="label">Account Number</label>
            <input className="input" value={accountNumber} onChange={(e)=>setAcc(e.target.value)} />
          </div>
          <div>
            <label className="label">Account Holder Name</label>
            <input className="input" value={holderName} onChange={(e)=>setHolderName(e.target.value)} />
          </div>
        </div>

        <div className="grid-2" style={{ marginTop: 12 }}>
          <div>
            <label className="label">Upload DB Signature (specimen)</label>
            <input type="file" accept="image/*" onChange={(e)=>setSignatureFile(e.target.files?.[0] || null)} />
          </div>
          <div>
            <label className="label">Upload Cancelled Cheque</label>
            <input type="file" accept="image/*" onChange={(e)=>setCancelledFile(e.target.files?.[0] || null)} />
          </div>
        </div>

        <div style={{ marginTop: 16 }}>
          <button className="btn" disabled={saving}>{saving ? "Saving..." : "Save & Continue"}</button>
        </div>
      </form>
    </div>
  );
}

// src/pages/RegisterPage.jsx
import { useState } from "react";
import { apiRegister } from "../services/auth_api";
import { useToast } from "../components/ToastProvider";
import { useNavigate, Link } from "react-router-dom";

export default function RegisterPage() {
  const [email, setE] = useState("");
  const [password, setP] = useState("");
  const [fullName, setN] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const { notify } = useToast();
  const nav = useNavigate();

  async function onSubmit(e) {
    e.preventDefault();
    try {
      setLoading(true);
      await apiRegister({ email, password, full_name: fullName, phone });
      notify("Registered and logged in", "success");
      nav("/onboarding");
    } catch (e2) {
      notify(e2.message, "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h2>Create your account</h2>
      <form className="card" onSubmit={onSubmit} style={{ maxWidth: 520 }}>
        <div>
          <label className="label">Full Name</label>
          <input className="input" value={fullName} onChange={(e)=>setN(e.target.value)} />
        </div>
        <div style={{ marginTop: 12 }}>
          <label className="label">Email</label>
          <input className="input" type="email" value={email} onChange={(e)=>setE(e.target.value)} />
        </div>
        <div style={{ marginTop: 12 }}>
          <label className="label">Phone</label>
          <input className="input" value={phone} onChange={(e)=>setPhone(e.target.value)} />
        </div>
        <div style={{ marginTop: 12 }}>
          <label className="label">Password</label>
          <input className="input" type="password" value={password} onChange={(e)=>setP(e.target.value)} />
        </div>
        <div style={{ marginTop: 16, display:"flex", gap:8, alignItems:"center" }}>
          <button className="btn" disabled={loading}>{loading ? "..." : "Register"}</button>
          <span style={{ fontSize:13 }}>Already have an account? <Link to="/login">Login</Link></span>
        </div>
      </form>
    </div>
  );
}

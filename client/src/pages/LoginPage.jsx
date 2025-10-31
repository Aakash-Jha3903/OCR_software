import { useState } from "react";
import { apiLogin } from "../services/auth_api";
import { useNavigate, Link } from "react-router-dom";
import { useToast } from "../components/ToastProvider";

export default function LoginPage() {
  const [email, setE] = useState("");
  const [password, setP] = useState("");
  const [loading, setLoading] = useState(false);
  const { notify } = useToast();
  const nav = useNavigate();

  async function onSubmit(e) {
    e.preventDefault();
    try {
      setLoading(true);
      await apiLogin({ email, password });
      notify("Logged in", "success");
      nav("/onboarding");
    } catch (e2) {
      notify(e2.message, "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h2>Login</h2>
      <form className="card" onSubmit={onSubmit} style={{ maxWidth: 420 }}>
        <div>
          <label className="label">Email</label>
          <input className="input" type="email" value={email} onChange={(e)=>setE(e.target.value)} />
        </div>
        <div style={{ marginTop: 12 }}>
          <label className="label">Password</label>
          <input type="password" className="input" value={password} onChange={(e)=>setP(e.target.value)} />
        </div>
        <div style={{ marginTop: 16, display:"flex", gap:8, alignItems:"center" }}>
          <button className="btn" disabled={loading}>{loading ? "..." : "Login"}</button>
          <span style={{ fontSize:13 }}>New here? <Link to="/register">Create account</Link></span>
        </div>
      </form>
    </div>
  );
}

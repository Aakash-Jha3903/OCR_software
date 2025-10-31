// src/components/Navbar.jsx
import { Link, NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={{ borderBottom: "1px solid #eee", background: "#fff" }}>
      <div className="container" style={{ display:"flex", alignItems:"center", gap:16 }}>
        <Link to="/"><strong>ChequeVerifier</strong></Link>
        <div style={{ marginLeft:"auto", display:"flex", gap:12 }}>
          <NavLink to="/cheques" className="btn outline">Cheques</NavLink>
          <NavLink to="/verifications" className="btn outline">Verifications</NavLink>
          <NavLink to="/upload" className="btn">Upload</NavLink>
        </div>
      </div>
    </nav>
  );
}

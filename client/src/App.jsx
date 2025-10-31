// src/App.jsx
import { Outlet } from "react-router-dom";
import Navbar from "./components/Navbar";
import "./styles/globals.css";
import OfflineBanner from "./components/OfflineBanner";

export default function App() {
  return (
    <div style={{ minHeight:"100%", background:"#fafafa" }}>
      <Navbar />
      <OfflineBanner />
      <Outlet />
    </div>
  );
}

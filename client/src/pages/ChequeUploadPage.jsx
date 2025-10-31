import { useState } from "react";
import { uploadCheque } from "../services/cheques";
import FilePicker from "../components/FilePicker";
import { useNavigate } from "react-router-dom";
import { useToast } from "../components/ToastProvider";
import Skeleton from "../components/Skeleton";

export default function ChequeUploadPage() {
  const [file, setFile] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const nav = useNavigate();
  const { notify } = useToast();

  const preview = file ? URL.createObjectURL(file) : null;

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    if (!file) {
      setError("Please select an image.");
      return;
    }
    try {
      setSubmitting(true);
      const created = await uploadCheque(file);
      notify(`Cheque #${created.id} uploaded`, "success");
      nav(`/cheques/${created.id}`);
    } catch (err) {
      setError(err.message);
      notify(err.message, "error");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="container">
      <h2>Upload Cheque</h2>
      <form className="card" onSubmit={onSubmit} style={{ maxWidth: 640 }}>
        <FilePicker onChange={setFile} />
        <div style={{ marginTop: 12 }}>
          {!preview ? <Skeleton h={160} r={12} /> :
            <img src={preview} alt="preview"
                 style={{ width:"100%", maxHeight:300, objectFit:"contain", borderRadius:12 }} />}
        </div>
        {error && <div className="badge fail" style={{ marginTop: 12 }}>{error}</div>}
        <div style={{ marginTop: 16 }}>
          <button className="btn" disabled={!file || submitting}>
            {submitting ? "Uploading..." : "Upload"}
          </button>
        </div>
      </form>
    </div>
  );
}

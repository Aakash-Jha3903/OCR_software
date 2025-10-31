// src/services/cheques.js
import api from "./api";

export async function uploadCheque(file) {
  const form = new FormData();
  form.append("image", file);
  const { data } = await api.post("/api/cheques/", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function getCheque(id) {
  const { data } = await api.get(`/api/cheques/${id}/`);
  return data;
}

export async function verifyCheque(id, signThreshold = 80) {
  const { data } = await api.post(`/api/cheques/${id}/verify/`, {
    sign_threshold: Number(signThreshold),
  });
  return data;
}

export async function reverifyCheque(id, signThreshold = 80) {
  const { data } = await api.post(`/api/cheques/${id}/reverify/`, {
    sign_threshold: Number(signThreshold),
  });
  return data;
}

export async function listCheques(params = {}) {
  const qs = new URLSearchParams(params);
  const { data } = await api.get(`/api/cheques/list/?${qs.toString()}`);
  return data;
}

export async function listVerifications(params = {}) {
  const qs = new URLSearchParams(params);
  const { data } = await api.get(`/api/cheques/verifications/?${qs.toString()}`);
  return data;
}

export async function getVerification(id) {
  const { data } = await api.get(`/api/cheques/verifications/${id}/`);
  return data;
}

// ---- NEW: audits for a cheque ----
// Requires a read-only endpoint: GET /api/cheques/:id/audit/
export async function getChequeAudits(id) {
  const { data } = await api.get(`/api/cheques/${id}/audit/`);
  return data; // [{id, old_status, new_status, message, created_at}]
}

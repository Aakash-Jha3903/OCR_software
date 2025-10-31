// src/services/auth_api.js
import api, { setAuthToken } from "./api";

/** Replace URLs to match your DRF auth endpoints */
const AUTH_ROUTES = {
  register: "/api/auth/register/",
  login: "/api/auth/login/",
  // me: "/api/me/",
  me: "/api/auth/me/",
  // mePatch: "/api/me/",
  mePatch: "/api/auth/me/",
  // meBank: "/api/me/bank/",
  meBank: "/api/auth/me/bank/",
};

export async function apiRegister({ email, password, full_name, phone }) {
  const { data } = await api.post(AUTH_ROUTES.register, {
    email, password, full_name, phone,
  });
  if (data?.token) setAuthToken(data.token);
  return data;
}

export async function apiLogin({ email, password }) {
  const { data } = await api.post(AUTH_ROUTES.login, { email, password });
  if (data?.token) setAuthToken(data.token);
  return data;
}

export async function apiGetMe() {
  const { data } = await api.get(AUTH_ROUTES.me);
  return data;
}

export async function apiPatchMe(payload) {
  const { data } = await api.patch(AUTH_ROUTES.mePatch, payload);
  return data;
}

/** Create/update bank + signature + cancelled cheque for the current user */
export async function apiUpsertMyBank({
  bank_id, bank_name, ifsc, micr,
  account_number, holder_name,
  signature_file, cancelled_cheque_file,
}) {
  const form = new FormData();
  if (bank_id) form.append("bank", bank_id);
  if (bank_name) form.append("bank_name", bank_name);
  if (ifsc) form.append("ifsc", ifsc);
  if (micr) form.append("micr", micr);
  if (account_number) form.append("account_number", account_number);
  if (holder_name) form.append("holder_name", holder_name);
  if (signature_file) form.append("signature_image", signature_file);
  if (cancelled_cheque_file) form.append("cancelled_cheque_image", cancelled_cheque_file);

  const { data } = await api.post(AUTH_ROUTES.meBank, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

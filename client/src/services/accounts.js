// src/services/accounts.js
import api from "./api";

export async function getAccount(id) {
  const { data } = await api.get(`/api/accounts/${id}/`);
  return data;
}

export async function patchBalance(id, { amount, op = "debit" }) {
  const { data } = await api.patch(`/api/accounts/${id}/balance/`, { amount, op });
  return data;
}

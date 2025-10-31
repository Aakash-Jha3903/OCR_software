// src/services/api.js
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000",
  withCredentials: false,
});

// ---- token helpers ----
export function setAuthToken(token) {
  if (token) localStorage.setItem("auth_token", token);
  else localStorage.removeItem("auth_token");
}
export function getAuthToken() {
  return localStorage.getItem("auth_token");
}

// attach Authorization header if token exists
api.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// normalize errors
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const msg =
      err?.response?.data?.detail ||
      err?.response?.data?.message ||
      err.message ||
      "Request failed";
    return Promise.reject(new Error(msg));
  }
);

export default api;

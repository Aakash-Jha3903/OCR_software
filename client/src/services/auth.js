// src/services/auth.js
import { setAuthToken } from "./api";

/**
 * Stub login: accepts any username/password and stores a fake token.
 * Swap this for real JWT later.
 */
export async function login({ username, password }) {
  if (!username || !password) throw new Error("Username & password are required");
  const fakeToken = btoa(`${username}:${password}:${Date.now()}`);
  setAuthToken(fakeToken);
  localStorage.setItem("auth_user", JSON.stringify({ username }));
  return { token: fakeToken, user: { username } };
}

export function logout() {
  setAuthToken(null);
  localStorage.removeItem("auth_user");
}

export function getAuthUser() {
  const raw = localStorage.getItem("auth_user");
  return raw ? JSON.parse(raw) : null;
}

export function isLoggedIn() {
  return !!localStorage.getItem("auth_token");
}

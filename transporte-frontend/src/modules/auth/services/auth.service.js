import api from "../../../services/api.js";

export const authService = {
  login: (credentials) => api.post("/auth/login/", credentials),
  logout: (refreshToken) =>
    api.post("/auth/logout/", { refresh: refreshToken }),
  refreshToken: (refresh) => api.post("/auth/token/refresh/", { refresh }),
  me: () => api.get("/auth/me/"),
  changePassword: (data) => api.post("/auth/change-password/", data),
};

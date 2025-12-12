
// =======================
// API URL BASE
// =======================
const API_URL = "http://localhost:5000/api";

// =======================
// GUARDAR TOKEN
// =======================
function saveToken(token) {
    localStorage.setItem("token", token);
}

// =======================
// OBTENER TOKEN
// =======================
function getToken() {
    return localStorage.getItem("token");
}

// =======================
// ELIMINAR TOKEN (LOGOUT)
// =======================
function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

// =======================
// PROTEGER PÁGINAS
// =======================
function requireAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = "login.html";
    }
}

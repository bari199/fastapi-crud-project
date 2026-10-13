import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Login from "@/pages/Login";
import Register from "@/pages/Register";
import Dashboard from "@/pages/Dashboard";
import RagChat from "@/pages/RagChat";

function ProtectedRoute({ children }) {
  const token = sessionStorage.getItem("access_token");

  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
        <Route
          path="/rag"
          element={
            <ProtectedRoute>
              <RagChat />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

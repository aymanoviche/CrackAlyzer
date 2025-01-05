import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './auth/context/AuthContext';
import { Login } from './auth/components/Login';
import { Signup } from './auth/components/Signup';
import { Dashboard } from './auth/components/Dashboard';
import { PrivateRoute } from './auth/components/PrivateRoute';
import { PasswordAnalyzer } from './auth/components/PasswordAnalyzer';
import { BreachChecker } from './auth/components/BreachChecker';
import { PasswordCracker } from './auth/components/PasswordCracker';
import { MainLayout } from './MainLayout.jsx';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<MainLayout />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/analyze"
            element={
              <PrivateRoute>
                <PasswordAnalyzer />
              </PrivateRoute>
            }
          />
          <Route
            path="/check-breach"
            element={
              <PrivateRoute>
                <BreachChecker/>
              </PrivateRoute>
            }
          />
          <Route
            path="/password-cracker"
            element={
              <PrivateRoute>
                <PasswordCracker />
              </PrivateRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

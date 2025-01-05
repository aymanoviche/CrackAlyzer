import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from './auth/context/AuthContext';
import './styles/MainLayout.css';

export const MainLayout = () => {
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };
  return (
  <div className="layout-container">
    <header className="nav-header">
      <nav className="nav-content">
        <Link to="/" className="brand-logo">
          <img src="../../../media/logo.png" alt="CrackAlyzer Logo" className="nav-logo" />
        </Link>
        <div className="nav-links">
          {!token ? (
            <>
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/signup" className="nav-link nav-link-primary">Signup</Link>
            </>
          ) : (
            <>
              <Link to="/analyze" className="nav-link">Password Analyzer</Link>
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
              <Link to="/password-cracker" className="dashboard-link">Password Cracker</Link>
              <Link to="/check-breach" className="nav-link">Breach Checker</Link>
              <button onClick={handleLogout} className="nav-link nav-link-danger">Logout</button>
            </>
          )}
        </div>
      </nav>
    </header>
      
    <main className="main-content">
      <div className="welcome-container">
        <h1 className="welcome-title">Welcome to CrackAlyzer</h1>
        <p className="welcome-text">Secure your passwords with our advanced tools</p>
        {!token && (
          <Link to="/login" className="login-button">
            Login to Start
          </Link>
        )}
      </div>
    </main>
    </div>
  );
};
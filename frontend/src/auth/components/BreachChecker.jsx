import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

export const BreachChecker = () => {
  const [password, setPassword] = useState('');
  const [result, setResult] = useState(null);
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };
  
  const checkPassword = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/check-breach/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: password }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Check failed:', error);
    }
  };

  return (
    <div className="layout-container">
      <header className="nav-header">
        <nav className="nav-content">
          <Link to="/" className="brand-logo">
            <img src="../../../media/logo.png" alt="CrackAlyzer Logo" className="nav-logo" />
          </Link>
          <div className="nav-links">
            <Link to="/dashboard" className="nav-link">Dashboard</Link>
            <Link to="/analyze" className="nav-link">Password Analyzer</Link>
            <Link to="/password-cracker" className="dashboard-link">Password Cracker</Link>
            <button onClick={handleLogout} className="nav-link nav-link-danger">Logout</button>
          </div>
        </nav>
      </header>

      <main className="main-content">
        <div className="analyzer-container">
          <h1 className="analyzer-title">Password Breach Checker</h1>
          
          <div className="analyzer-card">
            <div className="input-section">
              <input
                type="text"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                className="password-input"
              />
              <button 
                onClick={checkPassword}
                className="analyze-button"
              >
                Check Password
              </button>
            </div>

            {result && (
            <div className="results-section">
              <div className="analysis-details">
                <h3 className="results-title">Breach Check Results</h3>
                <div className={`result-message ${result.count > 0 ? 'leaked' : 'safe'}`}>
                  {result.message}
                </div>
                {result.count > 0 && (
                  <p className="breach-count">
                    This password has appeared in {result.count} data breaches
                  </p>
                )}
              </div>
            </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};
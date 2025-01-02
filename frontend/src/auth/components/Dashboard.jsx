import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useState, useEffect } from 'react';
import '../../styles/MainLayout.css';

export const Dashboard = () => {
  const { user, token, logout } = useAuth();
  const navigate = useNavigate();
  const [analyzeHistory, setAnalyzeHistory] = useState([]);
  const [breachHistory, setBreachHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (token) {
      Promise.all([fetchAnalyzeHistory(), fetchBreachHistory()]);
    }
  }, [token]);

  const fetchAnalyzeHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/analyze/history', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Failed to fetch history');
      
      const data = await response.json();
      setAnalyzeHistory(data.history || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchBreachHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/check-breach/history', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Failed to fetch breach history');
      
      const data = await response.json();
      setBreachHistory(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

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
            <Link to="/check-breach" className="nav-link">Breach Checker</Link>
            <Link to="/analyze" className="nav-link">Password Analyzer</Link>
            <button onClick={handleLogout} className="nav-link nav-link-danger">Logout</button>
          </div>
        </nav>
      </header>

      <main className="main-content">
        <div className="dashboard-grid">
          {/* Left Column - Password Analysis History */}
          <div className="history-section">
            <h2 className="section-title">Password Analysis History</h2>
            <div className="history-content">
              {isLoading ? (
                <div className="loading-state">Loading...</div>
              ) : error ? (
                <div className="error-state">{error}</div>
              ) : analyzeHistory.length > 0 ? (
                analyzeHistory.map((item, index) => (
                  <div key={index} className="history-card">
                    <div className="card-header bg-gray-100">
                      <span className="timestamp text-gray-600">
                        {new Date(item.timestamp).toLocaleString()}
                      </span>
                      <span className={`strength-badge ${
                        item.strength === 'Very Weak' ? 'very-weak' :
                        item.strength === 'Weak' ? 'weak' :
                        item.strength === 'Moderate' ? 'moderate' :
                        item.strength === 'Strong' ? 'strong' : 'very-strong'
                      }`}>
                        Score: {item.score?.toFixed(2) || 'N/A'}
                      </span>
                    </div>
                    <div className="card-content bg-white p-4">
                      <div className="metrics-grid">
                        <div className="metric-item">
                          <span className="metric-label">Length</span>
                          <span className="metric-value">{item.details?.length || 'N/A'}</span>
                        </div>
                        <div className="metric-item">
                          <span className="metric-label">Entropy</span>
                          <span className="metric-value">{item.details?.entropy?.toFixed(1) || 'N/A'}</span>
                        </div>
                      </div>
                      <div className="checks-grid">
                        <div className={`check-item ${item.details?.has_lowercase ? 'passed' : 'failed'}`}>
                          <span>Lowercase</span>
                          <span>{item.details?.has_lowercase ? '✓' : '✗'}</span>
                        </div>
                        <div className={`check-item ${item.details?.has_uppercase ? 'passed' : 'failed'}`}>
                          <span>Uppercase</span>
                          <span>{item.details?.has_uppercase ? '✓' : '✗'}</span>
                        </div>
                        <div className={`check-item ${item.details?.has_digit ? 'passed' : 'failed'}`}>
                          <span>Digits</span>
                          <span>{item.details?.has_digit ? '✓' : '✗'}</span>
                        </div>
                        <div className={`check-item ${item.details?.has_symbol ? 'passed' : 'failed'}`}>
                          <span>Symbols</span>
                          <span>{item.details?.has_symbol ? '✓' : '✗'}</span>
                        </div>
                      </div>
                      {item.suggested_password && (
                        <div className="suggested-password">
                          <span className="suggestion-label">Suggested:</span>
                          <span className="suggestion-value">{item.suggested_password}</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                <p className="no-data">No analysis history available</p>
              )}
            </div>
          </div>

          {/* Right Column - Breach Check History */}
          <div className="history-section">
            <h2 className="section-title">Breach Check History</h2>
            <div className="history-content">
              {isLoading ? (
                <div className="loading-state">Loading...</div>
              ) : error ? (
                <div className="error-state">{error}</div>
              ) : breachHistory.length > 0 ? (
                breachHistory.map((item, index) => (
                  <div key={index} className="history-card">
                    <div className="card-header bg-gray-100">
                      <span className="timestamp text-gray-600">
                        {new Date(item.timestamp).toLocaleString()}
                      </span>
                      <span className={`status-badge ${item.count > 0 ? 'leaked' : 'safe'}`}>
                        {item.status}
                      </span>
                    </div>
                    <div className="card-content bg-white p-4">
                      <div className="password-display">
                        <strong>Password:</strong>
                        <span className="password-text">{item.password || 'N/A'}</span>
                      </div>
                      <p className="breach-message">{item.message}</p>
                      {item.count > 0 && (
                        <p className="breach-count text-red-600">
                          Found in {item.count.toLocaleString()} breaches
                        </p>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                <p className="no-data">No breach check history available</p>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
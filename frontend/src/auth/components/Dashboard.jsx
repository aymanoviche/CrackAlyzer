import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useState, useEffect } from 'react';

export const Dashboard = () => {
  const { user, token, logout } = useAuth();
  const navigate = useNavigate();
  const [analyzeHistory, setAnalyzeHistory] = useState([]);
  const [breachHistory, setBreachHistory] = useState([]);
  const [crackerHistory, setCrackerHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [analyzeError, setAnalyzeError] = useState(null);
  const [breachError, setBreachError] = useState(null);
  const [crackerError, setCrackerError] = useState(null);

  useEffect(() => {
    if (token) {
      Promise.all([
        fetchAnalyzeHistory(),
        fetchBreachHistory(),
        fetchCrackerHistory()
      ]).finally(() => setIsLoading(false));
    }
  }, [token]);

  const fetchAnalyzeHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/analyze/history', {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) throw new Error('Failed to fetch analyze history');
      
      const data = await response.json();
      const historyArray = Array.isArray(data) ? data : 
                          data.history ? data.history : [];
      setAnalyzeHistory(historyArray);
    } catch (error) {
      console.error('Analyze history error:', error);
      setAnalyzeHistory([]);
      setAnalyzeError(error.message);
    }
  };

  const fetchBreachHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/check-breach/history', {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) throw new Error('Failed to fetch breach history');
      
      const data = await response.json();
      const historyArray = Array.isArray(data) ? data : 
                          data.history ? data.history : [];
      setBreachHistory(historyArray);
    } catch (error) {
      console.error('Breach history error:', error);
      setBreachHistory([]);
      setBreachError(error.message);
    }
  };

  const fetchCrackerHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/password-cracker/history', {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) throw new Error('Failed to fetch cracker history');
      
      const data = await response.json();
      const historyArray = Array.isArray(data) ? data : 
                          data.history ? data.history : [];
      setCrackerHistory(historyArray);
    } catch (error) {
      console.error('Cracker history error:', error);
      setCrackerHistory([]);
      setCrackerError(error.message);
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
            <Link to="/analyze" className="nav-link">Password Analyzer</Link>
            <Link to="/check-breach" className="nav-link">Breach Checker</Link>
            <Link to="/password-cracker" className="nav-link">Password Cracker</Link>
            <button onClick={handleLogout} className="nav-link nav-link-danger">Logout</button>
          </div>
        </nav>
      </header>

      <main className="dashboard-content">
        <div className="history-grid">
          <div className="history-section">
            <h2 className="section-title">Password Analysis History</h2>
            <div className="history-content">
              {isLoading ? (
                <div className="loading-state">Loading...</div>
              ) : analyzeError ? (
                <div className="error-state">{analyzeError}</div>
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

          <div className="history-section">
            <h2 className="section-title">Password Cracker History</h2>
            <div className="history-content">
              {isLoading ? (
                <div className="loading-state">Loading...</div>
              ) : crackerError ? (
                <div className="error-state">{crackerError}</div>
              ) : crackerHistory.length === 0 ? (
                <p className="no-data">No cracker history available</p>
              ) : (
                crackerHistory.map((item, index) => (
                  <div key={index} className="history-card">
                    <div className="card-header bg-gray-100">
                      <span className="timestamp text-gray-600">
                        {new Date(item.timestamp).toLocaleString()}
                      </span>
                      <span className="hash-type-badge">{item.hash_type}</span>
                    </div>
                    <div className="card-content bg-white p-4">
                      <div className="hash-display">
                        <strong>Hash:</strong>
                        <span className="hash-text">{item.hash_string}</span>
                      </div>
                      <div className="decrypted-display">
                        <strong>Decrypted:</strong>
                        <span className="decrypted-text">{item.decrypted_string}</span>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="history-section">
            <h2 className="section-title">Breach Check History</h2>
            <div className="history-content">
              {isLoading ? (
                <div className="loading-state">Loading...</div>
              ) : breachError ? (
                <div className="error-state">{breachError}</div>
              ) : breachHistory.length === 0 ? (
                <p className="no-data">No breach history available</p>
              ) : (
                breachHistory.map((item, index) => (
                  <div key={index} className="history-card">
                    <div className="card-header bg-gray-100">
                      <span className="timestamp text-gray-600">
                        {new Date(item.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <div className="card-content bg-white p-4">
                      <div className="breach-count">
                        Found in {item.count} breaches
                      </div>
                      <div className="breach-message">
                        {item.message}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
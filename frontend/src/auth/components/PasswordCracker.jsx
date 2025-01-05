import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

export const PasswordCracker = () => {
  const [hash, setHash] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!hash.trim()) {
      setError('Please enter a hash to crack');
      return;
    }

    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:8000/password-cracker/${hash}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to crack hash');
      }

      const data = await response.json();
      setResult(data);
      setError(null);
    } catch (error) {
      setError(error.message);
      setResult(null);
    } finally {
      setIsLoading(false);
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
            <Link to="/check-breach" className="nav-link">Breach Checker</Link>
            <button onClick={handleLogout} className="nav-link nav-link-danger">Logout</button>
          </div>
        </nav>
      </header>

      <main className="main-content">
        <div className="analyzer-container">
          <h1 className="analyzer-title">Password Cracker</h1>
          
          <div className="analyzer-card">
            <div className="input-section">
              <input
                type="text"
                value={hash}
                onChange={(e) => setHash(e.target.value)}
                placeholder="Enter hash to crack (MD5, SHA1, Base64)"
                className="password-input"
                disabled={isLoading}
              />
              <button 
                onClick={handleSubmit}
                className="analyze-button"
                disabled={isLoading}
              >
                {isLoading ? 'Cracking...' : 'Crack Hash'}
              </button>
            </div>

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            {result && (
              <div className="results-section">
                <div className="analysis-details">
                  <h3 className="results-title">Cracking Results</h3>
                  <div className="result-content">
                    <div className="result-row">
                      <span className="result-label">Hash Type:</span>
                      <span className="result-value">
                        {result.md5_hash ? 'MD5' : result.sha1_hash ? 'SHA1' : 'Base64'}
                      </span>
                    </div>
                    <div className="result-row">
                      <span className="result-label">Original Hash:</span>
                      <span className="result-value">{hash}</span>
                    </div>
                    <div className="result-row">
                      <span className="result-label">Decrypted Value:</span>
                      <span className="result-value">{result.decrypted_string}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

export const PasswordAnalyzer = () => {
  const [password, setPassword] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const getBarLevel = (strength) => {
    switch (strength) {
      case 'Very Weak': return 1;
      case 'Weak': return 2;
      case 'Moderate': return 3;
      case 'Strong': return 4;
      case 'Very Strong': return 5;
      default: return 1;
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const getBarClass = (segment, strength) => {
    const level = getBarLevel(strength);
    const baseClass = 'bar-segment';
    if (segment <= level) {
      return `${baseClass} filled level-${level}`;
    }
    return baseClass;
  };

  const analyzePassword = async () => {
    try {
      const response = await fetch('http://localhost:8000/analyze/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      });
      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error('Analysis failed:', error);
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
            <Link to="/check-breach" className="nav-link">Breach Checker</Link>
            <Link to="/password-cracker" className="dashboard-link">Password Cracker</Link>
            <button onClick={handleLogout} className="nav-link nav-link-danger">Logout</button>
          </div>
        </nav>
      </header>

      <main className="main-content">
        <div className="analyzer-container">
          <h1 className="analyzer-title">Password Strength Analyzer</h1>
          
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
                onClick={analyzePassword}
                className="analyze-button"
              >
                Analyze Password
              </button>
            </div>

            {analysis && (
              <div className="results-section">
                <div className="strength-indicator">
                  <h3>Strength Score: {analysis.score.toFixed(5)} - {analysis.strength}</h3>
                  <div className="strength-bar">
                    {[1, 2, 3, 4, 5].map((segment) => (
                      <div
                        key={segment}
                        className={getBarClass(segment, analysis.strength)}
                      />
                    ))}
                  </div>
                </div>

                <div className="analysis-details">
                  <h3>Password Analysis</h3>
                  <ul className="details-list">
                    <li className="output-details">
                      <span>Length</span>
                      <span>{analysis.details?.length}</span>
                    </li>
                    <li className="output-details">
                      <span>Has Lowercase</span>
                      <span>{analysis.details?.has_lowercase ? '✓' : '✗'}</span>
                    </li>
                    <li className="output-details">
                      <span>Has Uppercase</span>
                      <span>{analysis.details?.has_uppercase ? '✓' : '✗'}</span>
                    </li>
                    <li className="output-details">
                      <span>Has Numbers</span>
                      <span>{analysis.details?.has_digit ? '✓' : '✗'}</span>
                    </li>
                    <li className="output-details">
                      <span>Has Special Characters</span>
                      <span>{analysis.details?.has_symbol ? '✓' : '✗'}</span>
                    </li>
                  </ul>
                </div>

                {analysis.suggested_password && (
                  <div className="analysis-details">
                    <h3>Suggested Password</h3>
                    <div className="suggestion-wrapper">
                      <div className="suggestion-content">
                        {analysis.suggested_password}
                      </div>
                      <button 
                        className="copy-button"
                        onClick={() => navigator.clipboard.writeText(analysis.suggested_password)}
                        title="Copy password"
                      >
                        📋
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};
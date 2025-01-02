import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import '../../styles/MainLayout.css';
import { useNavigate, Link } from 'react-router-dom';

export const Login = () => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');
  const { login, token, logout } = useAuth();
  const navigate = useNavigate();

  // Add useEffect to handle navigation when token changes
  useEffect(() => {
    if (token) {
      navigate('/');
    }
  }, [token, navigate]);

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors
  
    try {
      await login(credentials);
      // Navigation will be handled by useEffect when token is set
    } catch (err) {
      // Handle 400 Bad Request specifically
      if (err.response?.status === 400) {
        setError('Incorrect username or password');
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
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
            {!token ? (
              <>
                <Link to="/login" className="nav-link">Login</Link>
                <Link to="/signup" className="nav-link nav-link-primary">Signup</Link>
              </>
            ) : (
              <>
                <Link to="/analyze" className="nav-link">Password Analyzer</Link>
                <Link to="/check-breach" className="nav-link">Breach Checker</Link>
                <Link to="/dashboard" className="nav-link">Dashboard</Link>
                <button onClick={handleLogout} className="nav-link nav-link-danger">Logout</button>
              </>
            )}
          </div>
        </nav>
      </header>
      <main className="main-content">
        <div className="form-container">
          <form className="form" onSubmit={handleSubmit}>
            <p className="title">Login</p>
            {error && (
              <div 
                style={{
                  color: '#ff0000',
                  backgroundColor: '#ffebeb',
                  padding: '12px',
                  borderRadius: '4px',
                  marginBottom: '15px',
                  fontSize: '14px',
                  textAlign: 'center',
                  border: '1px solid #ffcdd2',
                  fontWeight: '500',
                  boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)'
                }}
              >
                {error}
              </div>
            )}
            <label>
              <input 
                className="input" 
                type="text" 
                placeholder="" 
                required
                value={credentials.username} 
                onChange={(e) => setCredentials({...credentials, username: e.target.value})}
              />
              <span>Username</span>
            </label>
            <label>
              <input 
                className="input" 
                type="password" 
                placeholder="" 
                required 
                value={credentials.password} 
                onChange={(e) => setCredentials({...credentials, password: e.target.value})}
              />
              <span>Password</span>
            </label>
            <button className="submit">Login</button>
            <p className="signin">Don't have an account? <Link to="/Signup">Sign up now!</Link></p>
          </form>
        </div>
      </main>
    </div>
  );
};
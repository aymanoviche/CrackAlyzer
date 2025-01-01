import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import '../../styles/MainLayout.css';
import { useNavigate, Link } from 'react-router-dom';

export const Login = () => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');
  const { login, token, logout } = useAuth();  // Add token and logout here
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(credentials);
      navigate('/');
    } catch (err) {
      setError('Invalid credentials');
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
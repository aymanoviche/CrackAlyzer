import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import '../../styles/MainLayout.css';

export const Signup = () => {
  const [userData, setUserData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
  });
  const [errors, setErrors] = useState({});
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signup(userData);
      navigate('/login');
    } catch (err) {
      const response = await err.response?.json();
      if (response?.detail) {
        if (typeof response.detail === 'string') {
          setErrors({ general: response.detail });
        } else {
          const newErrors = {};
          response.detail.forEach(error => {
            newErrors[error.loc[1]] = error.msg;
          });
          setErrors(newErrors);
        }
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
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/signup" className="nav-link nav-link-primary">Signup</Link>
          </div>
        </nav>
      </header>
      <main className="main-content">
        <div className="form-container">
          <form className="form" onSubmit={handleSubmit}>
            <p className="title">Signup</p>
            {errors.general && <p className="error-message">{errors.general}</p>}
            <label>
              <input
                className="input"
                type="text"
                placeholder=""
                required
                value={userData.full_name}
                onChange={(e) => setUserData({...userData, full_name: e.target.value})}
              />
              {errors.full_name && <p className="error-message">{errors.full_name}</p>}
              <span>Full Name</span>
            </label>
            <label>
              <input
                className="input"
                type="text"
                placeholder=""
                required
                value={userData.username}
                onChange={(e) => setUserData({...userData, username: e.target.value})}
              />
              {errors.username && <p className="error-message">{errors.username}</p>}
              <span>Username</span>
            </label>
            <label>
              <input
                className="input"
                type="email"
                placeholder=""
                required
                value={userData.email}
                onChange={(e) => setUserData({...userData, email: e.target.value})}
              />
              {errors.email && <p className="error-message">{errors.email}</p>}
              <span>Email</span>
            </label>
            <label>
              <input
                className="input"
                type="password"
                placeholder=""
                required
                value={userData.password}
                onChange={(e) => setUserData({...userData, password: e.target.value})}
              />
              {errors.password && <p className="error-message">{errors.password}</p>}
              <span>Password</span>
            </label>
            <button className="submit">Sign Up</button>
            <p className="signin">Already have an account? <Link to="/login">Login</Link></p>
          </form>
        </div>
      </main>
    </div>
  );
};
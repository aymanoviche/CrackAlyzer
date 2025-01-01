import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../../styles/MainLayout.css';

export const Dashboard = () => {
  const { user, token, logout } = useAuth();
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
            <Link to="/analyze" className="nav-link">Password Analyzer</Link>
            <Link to="/check-breach" className="nav-link">Breach Checker</Link>
            {/* <Link to="/dashboard" className="nav-link">Dashboard</Link> */}
            <button onClick={handleLogout} className="nav-link nav-link-danger">Logout</button>
          </div>
        </nav>
      </header>

      <main className="main-content">
        {user && (
          <div className="user-profile-container">
            <h1 className="profile-title">Welcome, {user.full_name}!</h1>
            <div className="profile-card">
              <div className="profile-header">
                <div className="profile-info">
                  <h2>{user.full_name}</h2>
                  <p className="user-role">Account Member</p>
                </div>
              </div>
              <div className="profile-details">
                <div className="detail-item">
                  <span className="detail-label">Username</span>
                  <span className="detail-value">{user.username}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Email</span>
                  <span className="detail-value">{user.email}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Member Since</span>
                  <span className="detail-value">
                    {new Date(user.created_at).toLocaleDateString()}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Last Updated</span>
                  <span className="detail-value">
                    {new Date(user.updated_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};
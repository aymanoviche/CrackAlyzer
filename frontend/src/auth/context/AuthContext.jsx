import { createContext, useState, useContext, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { authApi } from '../api/auth';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const navigate = useNavigate();
  const location = useLocation();

  const protectedRoutes = ['/dashboard', '/password-analyzer', '/check-breach'];

  useEffect(() => {
    const isProtectedRoute = protectedRoutes.includes(location.pathname);
    
    if (token) {
      localStorage.setItem('token', token);
      fetchUser();
    } else if (isProtectedRoute) {
      navigate('/login');
    }
  }, [token, location.pathname]);

  const fetchUser = async () => {
    try {
      const userData = await authApi.getMe(token);
      setUser(userData);
    } catch (error) {
      logout();
      if (protectedRoutes.includes(location.pathname)) {
        navigate('/login');
      }
    }
  };

  const login = async (credentials) => {
    const data = await authApi.login(credentials);
    setToken(data.access_token);
  };

  const signup = async (userData) => {
    return await authApi.signup(userData);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    if (protectedRoutes.includes(location.pathname)) {
      navigate('/login');
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
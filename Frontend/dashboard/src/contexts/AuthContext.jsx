
import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(undefined);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check for stored user in localStorage
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }
  }, []);

  const login = async (email, password) => {
    // In a real app, this would validate against a backend
    // For demo purposes, we'll accept any valid-looking email with password "password"
    if (email && password === "password") {
      const newUser = {
        id: '1',
        email: email,
        name: email.split('@')[0],
      };
      
      setUser(newUser);
      setIsAuthenticated(true);
      localStorage.setItem('user', JSON.stringify(newUser));
      return;
    }
    
    throw new Error('Invalid credentials');
  };
  
  const signup = async (email, password, name) => {
    // In a real app, this would register with a backend
    // For demo purposes, we'll just simulate account creation
    if (email && password && name) {
      const newUser = {
        id: Date.now().toString(),
        email,
        name,
      };
      
      setUser(newUser);
      setIsAuthenticated(true);
      localStorage.setItem('user', JSON.stringify(newUser));
      return;
    }
    
    throw new Error('Please fill all required fields');
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('user');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, signup, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

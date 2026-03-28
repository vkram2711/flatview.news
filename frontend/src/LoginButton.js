// src/LoginButton.js
import React, { useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { useNavigate } from 'react-router-dom';
import './LoginButton.css'; // Import the CSS file

const LoginButton = () => {
  const {
      isLoading,
      isAuthenticated,
      error,
      user,
      loginWithRedirect,
      logout,
  } = useAuth0();
  const navigate = useNavigate();

  useEffect(() => {
    console.log('isAuthenticated:', isAuthenticated);
    console.log('isLoading:', isLoading);
    console.log('error:', error);
    console.log('user:', user);
  }, [isAuthenticated, isLoading, error, user]);

  const handleAvatarClick = () => {
    navigate('/profile');
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Oops... {error.message}</div>;
  }

  return (
    <>
      {!isAuthenticated ? (
        <button className="login-button" onClick={() => loginWithRedirect()}>Log In</button>
      ) : (
        user && (
          <img
            src={user.picture}
            alt="User Avatar"
            onClick={handleAvatarClick}
            className="user-avatar"
          />
        )
      )}
    </>
  );
};

export default LoginButton;
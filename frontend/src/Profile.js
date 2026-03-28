// src/Profile.js
import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import './Profile.css'; // Import the CSS file

const Profile = () => {
  const { user, logout } = useAuth0();

  const handleLogout = () => {
    logout({ returnTo: window.location.origin });
  };

  const handleManageSubscription = () => {
    window.location.href = '/manage-subscription';
  };

  return (
    <div>
      {user && (
        <>
          <h2>Profile</h2>
          <img src={user.picture} alt="User Avatar" />
          <h3>{user.name}</h3>
          <p>{user.email}</p>
          <button className="logout-button" onClick={handleLogout}>Log Out</button>
          <button onClick={handleManageSubscription}>Manage Subscription</button>
        </>
      )}
    </div>
  );
};

export default Profile;
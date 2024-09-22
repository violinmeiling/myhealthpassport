// src/Navbar.js
import React from 'react';
import './Navbar.css'; // For styling the navbar

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul className="navbar-links">
        <li><a href="clinical-visits">Clinical Visits</a></li>
        <li><a href="medications">Medications</a></li>
        <li><a href="insurance">Insurance</a></li>
        <li><a href="profile">Profile</a></li>
      </ul>
    </nav>
  );
};

export default Navbar;

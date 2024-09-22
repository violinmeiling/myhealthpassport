// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import Navbar from './Navbar';
import Healthpass from './Healthpass';
import ClinicalVisits from './ClinicalVisits';
import Medications from './Medications';
import Insurance from './Insurance';
import Profile from './Profile';
import Login from './Login'; 

function App() {
  return (
    <Router>
      <div className="App">
        <Healthpass /> {}
        <Navbar /> {}

        <div className="tab-content">
          <Routes>
            <Route path="/" element={<Navigate to="/profile" />} />

            <Route path="/clinical-visits" element={<ClinicalVisits />} />
            <Route path="/medications" element={<Medications />} />
            <Route path="/insurance" element={<Insurance />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

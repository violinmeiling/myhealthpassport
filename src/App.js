// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css'; // Optional styling for content
import Navbar from './Navbar'; // Import the Navbar component
import Healthpass from './Healthpass'; // Import the Healthpass component
import ClinicalVisits from './ClinicalVisits'; // Import Clinical Visits component
import Medical from './Medical'; // Import About Page component
import Insurance from './Insurance'; // Import Contact Page component

function App() {
  return (
    <Router>
      <div className="App">
        <Healthpass /> {/* Healthpass Navbar */}
        <Navbar /> {/* Main Navbar */}

        <div className="tabs">
          <Link to="/clinical-visits" className="tab-link">
            <button>Clinical Visits</button>
          </Link>
          <Link to="/medical" className="tab-link">
            <button>Medical</button>
          </Link>
          <Link to="/insurance" className="tab-link">
            <button>Insurance</button>
          </Link>
        </div>

        <div className="tab-content">
          <Routes>
            <Route path="/clinical-visits" element={<ClinicalVisits />} />
            <Route path="/medical" element={<Medical />} />
            <Route path="/insurance" element={<Insurance />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

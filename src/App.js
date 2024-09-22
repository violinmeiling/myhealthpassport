import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Login from './Login'; // Adjust the path as needed
import InsuranceInfo from './InsuranceInfo'; // Adjust the path as needed

const App = () => {
  return (
    <Router>
      <div>
        <nav style={{ marginBottom: '20px' }}>
          <Link to="/">Login</Link> | <Link to="/insurance">Insurance Info</Link>
        </nav>
        
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/insurance" element={<InsuranceInfo />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

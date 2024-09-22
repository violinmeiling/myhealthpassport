// src/ClinicalVisits.js
import React, { useState } from 'react';
import './ClinicalVisits.css';

const ClinicalVisits = () => {
  // Mock data for clinical visits
  const clinicalVisits = [
    { id: 1, date: '9/21/2024', clinic_name: 'Swedish Urgent Care', name: 'Visit 3', description: 'Description for Visit 3', details: 'Details about Visit 3...' },
    { id: 2, date: '9/20/2024', clinic_name: 'ZoomCare', name: 'Visit 2', description: 'Description for Visit 2', details: 'Details about Visit 2...' },
    { id: 3, date: '9/19/2024', clinic_name: 'Overlake Clinic', name: 'Visit 1', description: 'Description for Visit 1', details: 'Details about Visit 1...' },
  ];

  // State for the search query and the selected visit
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedVisit, setSelectedVisit] = useState(null);

  // Function to handle visit selection
  const handleVisitClick = (visit) => {
    setSelectedVisit(visit);
  };

  // Filter clinical visits based on the search query
  const filteredVisits = clinicalVisits.filter((visit) =>
    visit.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="clinical-visits">
      <div className="left-panel">
        {/* Search bar */}
        <input
          type="text"
          placeholder="Search Clinical Visits..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />

        {/* List of clinical visits */}
        <div className="visit-list">
          {filteredVisits.map((visit) => (
            <div key={visit.id} className="visit-box" onClick={() => handleVisitClick(visit)}>
              <h3>{visit.date + " - " + visit.clinic_name}</h3>
              <p>{visit.description}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="right-panel">
        {/* Display selected visit details */}
        {selectedVisit ? (
          <div className="visit-details">
            <h2>{selectedVisit.name}</h2>
            <p>{selectedVisit.details}</p>
          </div>
        ) : (
          <div className="visit-placeholder">Select a visit to see details.</div>
        )}
      </div>
    </div>
  );
};

export default ClinicalVisits;

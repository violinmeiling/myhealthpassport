// src/Medications.js
import React, { useState } from 'react';
import './Medications.css'; // Optional: Style the tabs


// Mock data for medication
const medication = [
  { id: 1, name: 'Tylenol', intended_use: 'Pain reliever', dosage: "1 pill", frequency: 3, duration: 7},
  { id: 2, name: 'ibuprofen', intended_use: 'Pain reliever', dosage: "1 pill", frequency: 3, duration: 7},
  { id: 3, name: 'Benadryl', intended_use: 'Allergy medicine', dosage: "1 pill", frequency: 3, duration: 7},
];

const Medical = () => {

  // State to manage the active tab ('medication' or 'calendar')
  const [activeTab, setActiveTab] = useState('medication');

  // Function to render content based on the active tab
  const renderContent = () => {
    switch (activeTab) {
      case 'medication':
        return <AllMedication />;
      case 'calendar':
        return <CalendarView />;
      default:
        return <AllMedication />;
    }
  };

  return (
    <div id="medical-page">
      {/* Tabs for switching views */}
      <div className="tabs">
        <button
          className={activeTab === 'medication' ? 'active' : ''}
          onClick={() => setActiveTab('medication')}
        >
          All Medication
        </button>
        <button
          className={activeTab === 'calendar' ? 'active' : ''}
          onClick={() => setActiveTab('calendar')}
        >
          Calendar
        </button>
      </div>

      {/* Content that changes based on selected tab */}
      <div className="tab-content">
        {renderContent()}
      </div>
    </div>
  );
};


// Template for All Medication view
const AllMedication = () => {
  const [selectedMedication, setSelectedMedication] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  // Function to handle medication selection
  const handleMedicationClick = (medication) => {
    setSelectedMedication(medication);
  };

  // Filter medication based on the search query
  const filteredMedication = medication.filter((med) =>
    med.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="medication-view">
      <div className="left-panel">
        {/* Search bar */}
        <input
          type="text"
          placeholder="Search Medication..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
  
        {/* List of Medication */}
        <div className="medication-list">
          {filteredMedication.map((medication) => (
            <div key={medication.id} className="medication-box" onClick={() => handleMedicationClick(medication)}>
              <h3>{medication.name}</h3>
            </div>
          ))}
        </div>
      </div>
  
      <div className="right-panel">
        {/* Display selected medication details */}
        {selectedMedication ? (
          <div className="medication-details">
            <h2>{selectedMedication.name}</h2>
            <p>Intended use: {selectedMedication.intended_use}</p>
            <p>Dosage: {selectedMedication.dosage}</p>
            <p>Frequency: {selectedMedication.frequency} times a day</p>
            <p>Duration: {selectedMedication.duration} days</p>
          </div>
        ) : (
          <div className="medication-placeholder">Select a medication to see details.</div>
        )}
      </div>
    </div>
  );};

// Template for Calendar view
const CalendarView = () => (
  <div className="calendar-view">
    <h2>Calendar</h2>
    <p>This is where you'll display a calendar for medication scheduling.</p>
    {/* Add your calendar view or any related content here */}
  </div>
);

export default Medical;

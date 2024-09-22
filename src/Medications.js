import React, { useState } from 'react';
import Calendar from './Calendar';
import axios from 'axios';
import './Medications.css';

const API_URL = 'http://localhost:5000';

export const medications = async (userid) => {
  try {
    const response = await axios.get(`${API_URL}/getmedications?userid=${userid}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching user data:", error);
  }
};

// Mock data for medication
// const medications = [
//   { id: 1, name: 'Tylenol', intended_use: 'Pain reliever', dosage: "1 pill", frequency: 3, duration: 7 },
//   { id: 2, name: 'Ibuprofen', intended_use: 'Pain reliever', dosage: "1 pill", frequency: 3, duration: 7 },
//   { id: 3, name: 'Benadryl', intended_use: 'Allergy medicine', dosage: "1 pill", frequency: 3, duration: 7 },
// ];

const Medications = () => {
  const [activeTab, setActiveTab] = useState('medication');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedMedication, setSelectedMedication] = useState(null);

  const renderContent = () => {
    switch (activeTab) {
      case 'medication':
        return <AllMedication 
          searchQuery={searchQuery} 
          setSearchQuery={setSearchQuery} 
          handleMedicationClick={handleMedicationClick} 
          selectedMedication={selectedMedication}
          medications={medications} 
        />;
      case 'calendar':
        return <CalendarView 
          handleMedicationClick={handleMedicationClick} 
          medications={medications} 
        />;
      default:
        return <AllMedication 
          searchQuery={searchQuery} 
          setSearchQuery={setSearchQuery} 
          handleMedicationClick={handleMedicationClick} 
          medications={medications} 
        />;
    }
  };

  const handleMedicationClick = (medication) => {
    setActiveTab('medication');
    setSelectedMedication(medication);
  };

  return (
    <div id="medical-page">
      <img src="/medicine.png" alt="Insurance" style={{ width: '600px', height: 'auto' }} />

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
      <div className="tab-content-med">{renderContent()}</div>
    </div>
  );
};

const AllMedication = ({ searchQuery, setSearchQuery, selectedMedication, handleMedicationClick, medications }) => {
  // Filter medication based on the search query
  const filteredMedication = medications.filter((med) =>
    med.medication_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="medication-view">
      <div className="left-panel">
        <input
          type="text"
          placeholder="Search Medication..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />

        <div className="medication-list">
          {filteredMedication.map((medication) => (
            <div key={medication.medication_id} className="medication-box" onClick={() => handleMedicationClick(medication)}>
              <h3>{medication.medication_name}</h3>
            </div>
          ))}
        </div>
      </div>

      <div className="right-panel">
        {/* Display selected medication details */}
        {selectedMedication ? (
          <div className="medication-details">
            <h2>{selectedMedication.medication_name}</h2>
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
  );
};

const CalendarView = ({ handleMedicationClick, medications }) => (
  <div className="calendar-view">
    <Calendar medications={medications} onMedicationClick={handleMedicationClick} />
  </div>
);

export default Medications;

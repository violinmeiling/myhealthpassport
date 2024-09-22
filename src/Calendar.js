import React from 'react';
import './Calendar.css';

const Calendar = ({ medications, onMedicationClick }) => {
  // Generate the calendar for the next 7 days
  const days = Array.from({ length: 7 }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() + i);
    return date.toLocaleDateString();
  });

  // Define times for each hour of the day (12 AM to 11 PM)
  const times = Array.from({ length: 24 }, (_, i) => {
    const hour = i % 12 || 12;
    const period = i < 12 ? 'AM' : 'PM';
    return `${hour} ${period}`;
  });

  // Check if medications is defined and not empty
  if (!medications || medications.length === 0) {
    return <div>No medications available.</div>;
  }

  // Create a map for each day to hold medications at each time
  const schedule = {};
  days.forEach(day => {
    schedule[day] = Array.from({ length: 24 }, () => []);
  });

  // Fill the schedule based on medication frequency
  medications.forEach(medication => {
    const timesToTake = Array.from({ length: medication.frequency }, (_, index) => {
      return getTimeSlot(index);
    });
    
    days.forEach(day => {
      timesToTake.forEach(time => {
        schedule[day][time].push(medication);
      });
    });
  });

  return (
    <div className="weekly-calendar">
      <h2>Weekly Schedule</h2>
      <table className="calendar-table">
        <thead>
          <tr>
            <th>Time</th>
            {days.map(day => (
              <th key={day}>{day}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {times.map((time, timeIndex) => (
            <tr key={timeIndex}>
              <td>{time}</td>
              {days.map((day, dayIndex) => (
                <td key={dayIndex} className="medication-cell">
                  {schedule[day][timeIndex].map((medication, medIndex) => (
                    <div 
                      key={medIndex} 
                      className="medication-schedule"
                      onClick={() => onMedicationClick(medication)}
                    >
                      {medication.name} ({medication.dosage})
                    </div>
                  ))}
                  {/* Keep the height of the cell consistent */}
                  {schedule[day][timeIndex].length === 0 && (
                    <div className="empty-cell"></div>
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// Function to get the time slot index based on the index (customize as needed)
const getTimeSlot = (index) => {
  // Example times; adjust based on your desired schedule
  const times = [8, 13, 20]; // Corresponding to 8 AM, 1 PM, and 8 PM
  return times[index] || 0; // Fallback for additional times, defaults to 12 AM
};

export default Calendar;

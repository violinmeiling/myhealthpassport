import React, { useState } from 'react';

const healthcareProviders = [
  {
    name: "HealthSecure Insurance",
    policies: "Health Insurance, Dental Insurance, Vision Insurance",
    coverage: "Covers hospitalization, outpatient services, preventive care, dental check-ups, and vision exams.",
    contact: "1-800-555-0199",
    website: "www.healthsecure.com",
    locations: "Available in all 50 states.",
    ratings: "4.7/5 based on customer reviews.",
    specialties: "Specializes in family health plans and preventive care."
  },
  {
    name: "LifeGuard Health Plans",
    policies: "Individual Health Plans, Family Plans",
    coverage: "Comprehensive coverage for hospitalization, surgeries, and preventive care services.",
    contact: "1-800-555-0177",
    website: "www.lifeguard.com",
    locations: "Nationwide coverage with local agents.",
    ratings: "4.5/5 based on customer satisfaction surveys.",
    specialties: "Tailored health insurance plans for individuals and families."
  },
  {
    name: "CareFirst Health Insurance",
    policies: "Medicare Advantage, Medicaid",
    coverage: "Covers hospital stays, doctor visits, prescription drugs, and preventive services.",
    contact: "1-800-555-0222",
    website: "www.carefirst.com",
    locations: "Available in over 30 states.",
    ratings: "4.6/5 based on claims experience.",
    specialties: "Focuses on affordable plans for seniors and low-income families."
  },
  {
    name: "WellnessGuard Insurance",
    policies: "Short-Term Health Plans, Long-Term Care Insurance",
    coverage: "Covers unexpected medical expenses and long-term care needs.",
    contact: "1-800-555-0311",
    website: "www.wellnessguard.com",
    locations: "Available in major metropolitan areas.",
    ratings: "4.4/5 based on customer feedback.",
    specialties: "Offers flexible plans for temporary and long-term health needs."
  },
  {
    name: "TravelWell Health Insurance",
    policies: "Travel Medical Insurance, Trip Cancellation",
    coverage: "Provides emergency medical coverage, trip interruption, and evacuation services.",
    contact: "1-800-555-0432",
    website: "www.travelwell.com",
    locations: "Coverage available worldwide.",
    ratings: "4.9/5 based on user experiences.",
    specialties: "Ideal for frequent travelers and expatriates."
  },
];


const Insurance = () => {
  const [location, setLocation] = useState('');
  const [expandedIndex, setExpandedIndex] = useState(null);

  const handleLocationChange = (e) => {
    setLocation(e.target.value);
  };

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'left', alignItems: 'center', height: '100vh', flexDirection: 'column' }}>
      <img src="/insurance.png" alt="Insurance" style={{ width: '1200px', height: 'auto', marginBottom: '20px' }} />
      
      <input
        type="text"
        placeholder="Enter your location"
        value={location}
        onChange={handleLocationChange}
        style={{ marginBottom: '20px', padding: '10px', width: '300px' }}
      />

      <h3>Insurance Companies in {location}</h3>
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        {healthcareProviders.map((company, index) => (
          <li key={index} style={{ marginBottom: '15px' }}>
            <div
              style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}
              onClick={() => toggleExpand(index)}
            >
              <span style={{ marginRight: '10px' }}>
                {expandedIndex === index ? '▼' : '▶'} {/* Triangle toggle */}
              </span>
              <strong>{company.name}</strong>
            </div>
            <div 
              style={{
                maxHeight: expandedIndex === index ? '200px' : '0',
                overflow: 'hidden',
                transition: 'max-height 0.3s ease',
                marginTop: '10px',
                paddingLeft: '20px',
              }}
            >
              <p><strong>Policies:</strong> {company.policies}</p>
              <p><strong>What they cover:</strong> {company.coverage}</p>
              <p><strong>Contact:</strong> {company.contact}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Insurance;

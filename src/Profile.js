import React, { useEffect, useState } from 'react';
import { createClient } from "@propelauth/javascript";

// Initialize PropelAuth client
const authClient = createClient({
  authUrl: "https://96933199.propelauthtest.com",
  enableBackgroundTokenRefresh: true
});

const Profile = () => {
  const [userId, setUserId] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const [profile, setProfile] = useState({
    name: '',
    dob: '',
    height: '',
    weight: '',
    sex: '',
    address: '',
    insurance_provider: '',
    insurance_policy_number: '',
    social_security_number: ''
  });

  const [medications, setMedications] = useState([]);
  const [inputFields, setInputFields] = useState(profile);
  const [medicationInput, setMedicationInput] = useState({
    medname: '',
    intended_use: '',
    dosage: '',
    frequency: '',
    duration: ''
  });

  // Handle input changes to update local input field state
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputFields((prevFields) => ({ ...prevFields, [name]: value }));
  };

  // Fetch profile information based on userId
  useEffect(() => {
    const fetchProfile = async () => {
      if (userId) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/users?userid=${userId}`);
          const data = await response.json();
          setProfile(data);
          setInputFields(data);
        } catch (error) {
          console.error("Error fetching profile data:", error);
        }
      }
    };

    fetchProfile();
    fetchMedications();
  }, [userId]);

  // Fetch medications
  const fetchMedications = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/users?userid=${userId}`);
      const data = await response.json();
      setMedications(data.medications || []);
    } catch (error) {
      console.error("Error fetching medications:", error);
    }
  };

  // Add new medication
  const handleAddMedication = async () => {
    const { medname, intended_use, dosage, frequency, duration } = medicationInput;
    try {
      const response = await fetch(`http://127.0.0.1:5000/addmedication?userid=${userId}&medname=${medname}&use=${intended_use}&dosage=${dosage}&frequency=${frequency}&duration=${duration}`);
      const data = await response.json();
      fetchMedications();  // Refresh the medication list
    } catch (error) {
      console.error("Error adding medication:", error);
    }
  };

  // Delete a medication
  const handleDeleteMedication = async (medId) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/deletemedication?userid=${userId}&medid=${medId}`);
      const data = await response.json();
      fetchMedications();  // Refresh the medication list
    } catch (error) {
      console.error("Error deleting medication:", error);
    }
  };

  // Handle input changes for medications
  const handleMedicationInputChange = (e) => {
    const { name, value } = e.target;
    setMedicationInput((prev) => ({ ...prev, [name]: value }));
  };

  // Update profile
  const handleUpdateProfile = async () => {
    const query = new URLSearchParams({
      userid: userId,
      name: inputFields.name,
      dob: inputFields.dob,
      height: inputFields.height,
      weight: inputFields.weight,
      sex: inputFields.sex,
      address: inputFields.address,
      provider: inputFields.insurance_provider,
      policy: inputFields.insurance_policy_number,
      ssn: inputFields.social_security_number
    }).toString();

    try {
      const response = await fetch(`http://127.0.0.1:5000/updateuser?${query}`);
      const data = await response.json();
      setProfile(data.user);
    } catch (error) {
      console.error("Error updating profile:", error);
    }
  };

  // Fetch authentication info and set the userId
  useEffect(() => {
    const fetchAuthInfo = async () => {
      const authInfo = await authClient.getAuthenticationInfoOrNull();
      if (authInfo) {
        setUserId(authInfo.user.userId);
        setIsLoggedIn(true);
        fetchMedications();  // Fetch medications once user is logged in
      } else {
        setIsLoggedIn(false);
      }
    };

    fetchAuthInfo();
  }, []);

  // Render UI based on login status
  if (!isLoggedIn) {
    return (
      <div>
        <p>You are not logged in</p>
        <button onClick={() => authClient.redirectToSignupPage()}>Sign Up</button>
        <button onClick={() => authClient.redirectToLoginPage()}>Login</button>
      </div>
    );
  }

  return (
    <div>
      <p>You are logged in as <span>{userId}</span></p>
      <p>Your profile:</p>
      <ul>
        {/* Profile form fields */}
        <li>
          Name: <span>{profile.name}</span>
          <input
            name="name"
            value={inputFields.name}
            onChange={(e) => setInputFields({ ...inputFields, name: e.target.value })}
          />
        </li>
        <li>
          DOB: <span>{profile.dob}</span>
          <input
            name="dob"
            value={inputFields.dob}
            onChange={handleInputChange}
          />
        </li>
        <li>
          Height: <span>{profile.height}</span>
          <input
            name="height"
            value={inputFields.height}
            onChange={handleInputChange}
          />
        </li>
        <li>
          Weight: <span>{profile.weight}</span>
          <input
            name="weight"
            value={inputFields.weight}
            onChange={handleInputChange}
          />
        </li>
        <li>
          Sex: <span>{profile.sex}</span>
          <input
            name="sex"
            value={inputFields.sex}
            onChange={handleInputChange}
          />
        </li>
        <li>
          Address: <span>{profile.address}</span>
          <input
            name="address"
            value={inputFields.address}
            onChange={handleInputChange}
          />
        </li>
        <li>
          Insurance Provider: <span>{profile.insurance_provider}</span>
          <input
            name="insurance_provider"
            value={inputFields.insurance_provider}
            onChange={handleInputChange}
          />
        </li>
        <li>
          Insurance Policy Number: <span>{profile.insurance_policy_number}</span>
          <input
            name="insurance_policy_number"
            value={inputFields.insurance_policy_number}
            onChange={handleInputChange}
          />
        </li>
        <li>
          Social Security Number: <span>{profile.social_security_number}</span>
          <input
            name="social_security_number"
            value={inputFields.social_security_number}
            onChange={handleInputChange}
          />
        </li>
      </ul>
      <button onClick={handleUpdateProfile}>Update Profile</button>

      {/* Medications Section */}
      <h3>Your Medications</h3>
      <ul id="medlist">
        {medications.map((med) => (
          <li key={med.medication_id}>
            {med.medication_name} - {med.dosage} - {med.frequency}x/day - {med.duration} days
            <button onClick={() => handleDeleteMedication(med.medication_id)}>Delete</button>
          </li>
        ))}
      </ul>

      <h4>Add Medication</h4>
      <input
        type="text"
        name="medname"
        placeholder="Medication Name"
        value={medicationInput.medname}
        onChange={handleMedicationInputChange}
      />
      <input
        type="text"
        name="intended_use"
        placeholder="Intended Use"
        value={medicationInput.intended_use}
        onChange={handleMedicationInputChange}
      />
      <input
        type="text"
        name="dosage"
        placeholder="Dosage"
        value={medicationInput.dosage}
        onChange={handleMedicationInputChange}
      />
      <input
        type="text"
        name="frequency"
        placeholder="Frequency"
        value={medicationInput.frequency}
        onChange={handleMedicationInputChange}
      />
      <input
        type="text"
        name="duration"
        placeholder="Duration"
        value={medicationInput.duration}
        onChange={handleMedicationInputChange}
      />
      <button onClick={handleAddMedication}>Add Medication</button>

      <button onClick={() => authClient.logout()}>Logout</button>
    </div>
  );
};

export default Profile;

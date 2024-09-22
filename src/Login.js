import React, { useState } from 'react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();

    // Simple form validation (you can replace this with real validation logic)
    if (email === '' || password === '') {
      setError('Both fields are required');
      return;
    }

    // You can replace this with real authentication logic (e.g., API call)
    if (email === 'test@example.com' && password === 'password') {
      alert('Login successful!');
    } else {
      setError('Invalid credentials');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', flexDirection: 'column' }}>
      {/* Add the image here */}
      <img src="/welcome.png"  alt="Logo" style={{ width: '1000px', height: 'auto', marginBottom: '20px' }} />
      
      <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
        <h2>Login</h2>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ marginBottom: '10px', padding: '10px' }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ marginBottom: '10px', padding: '10px' }}
        />
        <button type="submit" style={{ padding: '10px', cursor: 'pointer' }}>Login</button>
      </form>
    </div>
  );
};

export default Login;

import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setData(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }
  
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      const response = await axios.post('http://139.5.190.208:5050/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
  
      console.log("API Response:", response.data);
      setData(response.data);
      setError(null);
    } catch (err) {
      console.error("Error Response:", err.response || err.message); // Log the error
      setError(err.response?.data?.error || 'An error occurred while processing the file.');
    }
  };
  

  return (
    <div style={{ padding: '20px' }}>
      <h1>PDF Data Extraction</h1>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload and Extract</button>

      {error && <div style={{ color: 'red', marginTop: '20px' }}>{error}</div>}

      {data && (
        <div style={{ marginTop: '20px' }}>
          <h3>Extracted Details:</h3>
          <p><strong>Name:</strong> {data.Name}</p>
          <p><strong>Phone:</strong> {data.Phone}</p>
          <p><strong>Address:</strong> {data.Address}</p>
        </div>
      )}
    </div>
  );
}

export default App;

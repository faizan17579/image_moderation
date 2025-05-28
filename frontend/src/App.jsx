import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [token, setToken] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!token || !file) {
      setError('Please provide a token and select an image.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:7000/moderate', formData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data.result);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Error moderating image');
      setResult(null);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <h1 className="text-3xl font-bold mb-4">Image Moderation</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-md bg-white p-6 rounded shadow">
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Bearer Token</label>
          <input
            type="text"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="Enter your token"
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Upload Image</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full p-2 border rounded"
          />
        </div>
        <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
          Moderate Image
        </button>
      </form>
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {result && (
        <div className="mt-4 p-4 bg-white rounded shadow w-full max-w-md">
          <h2 className="text-xl font-semibold">Moderation Result</h2>
          <p>Safe: {result.is_safe ? 'Yes' : 'No'}</p>
          <h3 className="mt-2 font-medium">Categories:</h3>
          <ul>
            {Object.entries(result.categories).map(([key, value]) => (
              <li key={key}>{key}: {(value * 100).toFixed(2)}%</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default App;
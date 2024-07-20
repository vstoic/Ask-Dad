// src/components/LangGraphQuery.jsx

import React, { useState } from 'react';
import axios from 'axios';

const LangGraphQuery = () => {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await axios.post('http://localhost:8000/api/query/', { query: input });
      setResponse(result.data);
      setError('');
    } catch (err) {
      setError('An error occurred while fetching the response');
      setResponse('');
      console.error('Error:', err);
    }
  };

  return (
    <div>
      <h1>Ask Dad</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter your query"
        />
        <button type="submit">Submit</button>
      </form>
      {response && (
        <div>
          <h2>Response:</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
      {error && <div style={{ color: 'skyblue' }}>{error}</div>}
    </div>
  );
};

export default LangGraphQuery;

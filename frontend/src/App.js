import React, { useState, useEffect } from 'react';
import ResumeUpload from './components/ResumeUpload';
import JobSearch from './components/JobSearch';
import './App.css';

function App() {
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    const storedSessionId = localStorage.getItem('session_id');
    if (storedSessionId) {
      setSessionId(storedSessionId);
    }
  }, []);

  const handleUploadSuccess = (newSessionId) => {
    setSessionId(newSessionId);
  };

  const handleReset = () => {
    localStorage.removeItem('session_id');
    setSessionId(null);
  };

  return (
    <div className="App">
      <header className="header">
        <h1>💼 HireKarle</h1>
        <p className="tagline">AI-Powered Job Matcher</p>
        {sessionId && (
          <button className="reset-btn" onClick={handleReset}>
            Upload New Resume
          </button>
        )}
      </header>

      <main className="main-content">
        {!sessionId ? (
          <ResumeUpload onUploadSuccess={handleUploadSuccess} />
        ) : (
          <JobSearch sessionId={sessionId} />
        )}
      </main>

      <footer className="footer">
        <p>HireKarle - Where your resume meets reality</p>
      </footer>
    </div>
  );
}

export default App;

import React, { useState } from 'react';
import { searchJobs } from '../services/api';

const JobSearch = ({ sessionId }) => {
  const [jobTitle, setJobTitle] = useState('');
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [totalJobs, setTotalJobs] = useState(0);

  const handleSearch = async () => {
    if (!jobTitle.trim()) {
      setError('Please enter a job title');
      return;
    }

    setLoading(true);
    setError('');
    setJobs([]);
    setTotalJobs(0);

    try {
      const response = await searchJobs(sessionId, jobTitle);
      setJobs(response.jobs);
      setTotalJobs(response.total);
      
      if (response.total === 0) {
        setError('No jobs found. Try a different title.');
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to search jobs';
      setError(errorMessage);
      
      if (err.response?.status === 404) {
        localStorage.removeItem('session_id');
        setTimeout(() => window.location.reload(), 2000);
      }
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="search-container">
      <h2>Find Your Perfect Job</h2>
      
      <div className="search-box">
        <input
          type="text"
          placeholder="Enter job title (e.g., Software Engineer)"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && !loading && jobTitle.trim() && handleSearch()}
          disabled={loading}
        />
        <button onClick={handleSearch} disabled={loading || !jobTitle.trim()}>
          {loading ? 'Searching...' : 'Search Jobs'}
        </button>
      </div>

      {error && <p className="error">{error}</p>}
      
      {totalJobs > 0 && (
        <p style={{ textAlign: 'center', color: '#666', marginTop: '1rem' }}>
          Found {totalJobs} matching job{totalJobs !== 1 ? 's' : ''}
        </p>
      )}

      <div className="jobs-grid">
        {jobs.map((job, index) => (
          <div key={index} className="job-card">
            <div className="job-header">
              <h3>{job.title}</h3>
              <span 
                className="score-badge" 
                style={{ backgroundColor: getScoreColor(job.score) }}
              >
                {job.score}%
              </span>
            </div>
            
            <p className="company">{job.company}</p>
            <p className="location">{job.location}</p>
            <p className="source">Source: {job.source}</p>
            {job.description && (
              <p className="description">{job.description}</p>
            )}
            <p className="rationale">{job.rationale}</p>
            
            <a 
              href={job.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="apply-btn"
            >
              Apply Now →
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default JobSearch;

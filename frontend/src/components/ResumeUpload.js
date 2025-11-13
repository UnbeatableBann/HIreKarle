import React, { useState } from 'react';
import { uploadResume } from '../services/api';

const ResumeUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const validExtensions = ['.pdf', '.doc', '.docx', '.txt'];
      const fileExtension = selectedFile.name.toLowerCase().substring(selectedFile.name.lastIndexOf('.'));
      
      if (!validExtensions.includes(fileExtension)) {
        setError('Only PDF, DOCX, or TXT files supported');
        setFile(null);
        return;
      }
      
      setFile(selectedFile);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await uploadResume(file);
      localStorage.setItem('session_id', response.session_id);
      onUploadSuccess(response.session_id);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to upload resume';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Your Resume</h2>
      <p>Supported formats: PDF, DOCX, TXT</p>
      
      <input
        type="file"
        accept=".pdf,.doc,.docx,.txt"
        onChange={handleFileChange}
        disabled={loading}
      />
      
      {file && <p className="file-name">Selected: {file.name}</p>}
      
      <button onClick={handleUpload} disabled={loading || !file}>
        {loading ? 'Uploading...' : 'Upload Resume'}
      </button>
      
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default ResumeUpload;

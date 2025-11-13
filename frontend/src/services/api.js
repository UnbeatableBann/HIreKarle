import axios from 'axios';

const API_BASE_URL = `${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api`;

export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE_URL}/upload-resume`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  
  return response.data;
};

export const searchJobs = async (sessionId, jobTitle) => {
  const response = await axios.post(`${API_BASE_URL}/search-jobs`, {
    session_id: sessionId,
    job_title: jobTitle
  });
  
  return response.data;
};

export const healthCheck = async () => {
  const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/`);
  return response.data;
};

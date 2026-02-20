import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Detection endpoints
export const detectFace = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  const response = await api.post('/detect/face', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const detectText = async (text) => {
  const response = await api.post('/detect/text', { text });
  return response.data;
};

export const detectMultimodal = async (imageFile, text) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('text', text);
  const response = await api.post('/detect/multimodal', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const detectBatch = async (imageFiles) => {
  const formData = new FormData();
  imageFiles.forEach(file => formData.append('images', file));
  const response = await api.post('/detect/batch', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

// Analytics endpoints
export const getEmotionDistribution = async (days = 30) => {
  const response = await api.get(`/analytics/emotions?days=${days}`);
  return response.data;
};

export const getAccuracyTrend = async (days = 7) => {
  const response = await api.get(`/analytics/accuracy?days=${days}`);
  return response.data;
};

export const getConfidenceTrend = async (days = 7) => {
  const response = await api.get(`/analytics/confidence?days=${days}`);
  return response.data;
};

export const getDetectionsPerDay = async (days = 7) => {
  const response = await api.get(`/analytics/detections-per-day?days=${days}`);
  return response.data;
};

export const getModeUsage = async (days = 30) => {
  const response = await api.get(`/analytics/mode-usage?days=${days}`);
  return response.data;
};

export const getAnalyticsSummary = async () => {
  const response = await api.get('/analytics/summary');
  return response.data;
};

export const getAnalytics = async (timeRange = '7d') => {
  const response = await api.get(`/analytics?time_range=${timeRange}`);
  return response.data;
};

// RL endpoints
export const getQTable = async () => {
  const response = await api.get('/rl/qtable');
  return response.data;
};

export const submitFeedback = async (feedbackData) => {
  const response = await api.post('/rl/feedback', feedbackData);
  return response.data;
};

export const getTrainingHistory = async (limit = 100) => {
  const response = await api.get(`/rl/training-history?limit=${limit}`);
  return response.data;
};

export const getRewardTrend = async (episodes = 50) => {
  const response = await api.get(`/rl/reward-trend?episodes=${episodes}`);
  return response.data;
};

// History endpoints
export const getHistory = async (params = {}) => {
  const response = await api.get('/history', { params });
  return response.data;
};

export const getHistoryCount = async (params = {}) => {
  const response = await api.get('/history/count', { params });
  return response.data;
};

export const clearHistory = async () => {
  const response = await api.delete('/history/clear');
  return response.data;
};

export default api;

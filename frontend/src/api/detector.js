const API_BASE = 'http://localhost:8000';

export async function analyzeText(text, algorithm = 'kmp') {
  const response = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, algorithm })
  });
  if (!response.ok) throw new Error('Analysis failed');
  return response.json();
}

export async function analyzeBatch(texts, algorithm = 'kmp') {
  const response = await fetch(`${API_BASE}/analyze/batch?algorithm=${algorithm}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(texts)
  });
  if (!response.ok) throw new Error('Batch analysis failed');
  return response.json();
}

export async function getPatterns() {
  const response = await fetch(`${API_BASE}/patterns`);
  if (!response.ok) throw new Error('Failed to fetch patterns');
  return response.json();
}

export async function compareAlgorithms(text) {
  const response = await fetch(`${API_BASE}/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, algorithm: 'kmp' })
  });
  if (!response.ok) throw new Error('Comparison failed');
  return response.json();
}

export async function checkHealth() {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) throw new Error('API not healthy');
  return response.json();
}

// ==================== Pattern CRUD ====================

export async function createPattern(pattern) {
  const response = await fetch(`${API_BASE}/patterns`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(pattern)
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create pattern');
  }
  return response.json();
}

export async function updatePattern(index, pattern) {
  const response = await fetch(`${API_BASE}/patterns/${index}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(pattern)
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update pattern');
  }
  return response.json();
}

export async function deletePattern(index) {
  const response = await fetch(`${API_BASE}/patterns/${index}`, {
    method: 'DELETE'
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete pattern');
  }
  return response.json();
}

export async function saveAllPatterns() {
  const response = await fetch(`${API_BASE}/patterns/save`, {
    method: 'POST'
  });
  if (!response.ok) throw new Error('Failed to save patterns');
  return response.json();
}

// ==================== Setup Config ====================

export async function getSetupConfig() {
  const response = await fetch(`${API_BASE}/setup/config`);
  if (!response.ok) throw new Error('Failed to get setup config');
  return response.json();
}

export async function saveSetupConfig(config) {
  const response = await fetch(`${API_BASE}/setup/config`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config)
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to save config');
  }
  return response.json();
}


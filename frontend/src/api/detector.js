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

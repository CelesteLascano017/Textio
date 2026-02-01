import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Results.css';

export default function Results() {
  const navigate = useNavigate();
  const [analyses, setAnalyses] = useState([]);

  useEffect(() => {
    // Load analyses from localStorage
    const stored = localStorage.getItem('lastAnalysis');
    if (stored) {
      const analysis = JSON.parse(stored);
      setAnalyses([analysis]);
    }
  }, []);

  const getSeverityTitle = (result) => {
    if (!result.has_complaints) return 'Sin reclamos';
    const { high, medium, low } = result.alert_levels;
    if (high > 0) return 'Reclamo crítico';
    if (medium > 0) return 'Reclamo';
    if (low > 0) return 'Queja leve';
    return 'Sin clasificar';
  };

  const getSeverityClass = (result) => {
    if (!result.has_complaints) return 'severity-none';
    const { high, medium } = result.alert_levels;
    if (high > 0) return 'severity-critical';
    if (medium > 0) return 'severity-medium';
    return 'severity-low';
  };

  const viewAnalysis = (analysis) => {
    localStorage.setItem('currentAnalysis', JSON.stringify(analysis));
    navigate('/analysis');
  };

  if (analyses.length === 0) {
    return (
      <div className="results-page">
        <div className="results-container">
          <h1 className="results-title">Results</h1>
          <div className="no-results">
            <p>No analyses yet. Go to Setup to analyze some text.</p>
            <button className="btn btn-primary" onClick={() => navigate('/')}>
              Go to Setup
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="results-page">
      <div className="results-container">
        <h1 className="results-title">Results</h1>
        
        <div className="results-list">
          {analyses.map((analysis, index) => (
            <div 
              key={index} 
              className="result-card"
              onClick={() => viewAnalysis(analysis)}
            >
              <div className="result-header">
                <h3 className="result-name">{analysis.name}</h3>
                <span className="result-algorithm">({analysis.algorithm.toUpperCase()})</span>
              </div>
              <p className="result-preview">
                {analysis.result.original_text.slice(0, 150)}
                {analysis.result.original_text.length > 150 ? '...' : ''}
              </p>
              <div className={`result-severity ${getSeverityClass(analysis.result)}`}>
                {getSeverityTitle(analysis.result)}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

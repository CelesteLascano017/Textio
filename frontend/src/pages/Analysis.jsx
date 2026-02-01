import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import HighlightedText from '../components/HighlightedText';
import PatternsList from '../components/PatternsList';
import './Analysis.css';

export default function Analysis() {
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    const stored = localStorage.getItem('currentAnalysis');
    if (stored) {
      setAnalysis(JSON.parse(stored));
    }
  }, []);

  const getSeverityTitle = (result) => {
    if (!result.has_complaints) return 'Sin reclamos';
    const { high, medium, low } = result.alert_levels;
    if (high > 0) return 'Reclamo crítico';
    if (medium > 0) return 'Reclamo';
    if (low > 0) return 'Reclamo leve';
    return 'Sin clasificar';
  };

  const getSeverityClass = (result) => {
    if (!result.has_complaints) return 'severity-none';
    const { high, medium } = result.alert_levels;
    if (high > 0) return 'severity-critical';
    if (medium > 0) return 'severity-medium';
    return 'severity-low';
  };

  if (!analysis) {
    return (
      <div className="analysis-page">
        <div className="analysis-container">
          <p>No analysis selected. Go to Results to view an analysis.</p>
          <button className="btn btn-primary" onClick={() => navigate('/results')}>
            Go to Results
          </button>
        </div>
      </div>
    );
  }

  const { result } = analysis;

  return (
    <div className="analysis-page">
      <div className="analysis-container">
        <h1 className={`severity-title ${getSeverityClass(result)}`}>
          {getSeverityTitle(result)}
        </h1>

        <div className="analysis-content">
          <div className="analysis-text-panel">
            <HighlightedText 
              text={result.normalized_text} 
              detections={result.detections} 
            />
          </div>
          
          <PatternsList detections={result.detections} />
        </div>

        <div className="analysis-meta">
          <span className="meta-item">
            <strong>Algorithm:</strong> {analysis.algorithm.toUpperCase()}
          </span>
          <span className="meta-item">
            <strong>Patterns found:</strong> {result.patterns_found} / {result.total_patterns_checked}
          </span>
          <span className="meta-item">
            <strong>Time:</strong> {result.performance.total_execution_time_ms.toFixed(4)} ms
          </span>
        </div>

        <div className="analysis-actions">
          <button className="btn btn-secondary" onClick={() => navigate('/results')}>
            ← Back to Results
          </button>
          <button className="btn btn-primary" onClick={() => navigate('/')}>
            New Analysis
          </button>
        </div>
      </div>
    </div>
  );
}

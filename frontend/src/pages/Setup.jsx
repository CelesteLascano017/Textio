import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyzeText, getPatterns, getSetupConfig, saveSetupConfig } from '../api/detector';
import './Setup.css';

export default function Setup() {
  const navigate = useNavigate();
  const [textName, setTextName] = useState('');
  const [patternGroup, setPatternGroup] = useState('Claims');
  const [text, setText] = useState('');
  const [algorithm, setAlgorithm] = useState('kmp');
  const [loading, setLoading] = useState(false);
  const [patterns, setPatterns] = useState([]);
  const [configLoading, setConfigLoading] = useState(true);
  const [saveStatus, setSaveStatus] = useState('');

  // Load saved configuration and patterns on mount
  useEffect(() => {
    const loadData = async () => {
      try {
        const [patternsData, configData] = await Promise.all([
          getPatterns(),
          getSetupConfig()
        ]);
        setPatterns(patternsData.patterns || []);
        if (configData) {
          setTextName(configData.text_name || '');
          setPatternGroup(configData.pattern_group || 'Claims');
          setAlgorithm(configData.algorithm || 'kmp');
        }
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setConfigLoading(false);
      }
    };
    loadData();
  }, []);

  // Auto-save config when values change (debounced)
  useEffect(() => {
    if (configLoading) return;
    
    const saveConfig = async () => {
      try {
        await saveSetupConfig({
          text_name: textName,
          pattern_group: patternGroup,
          algorithm: algorithm
        });
        setSaveStatus('Configuración guardada');
        setTimeout(() => setSaveStatus(''), 2000);
      } catch (error) {
        console.error('Error saving config:', error);
      }
    };

    const timeoutId = setTimeout(saveConfig, 500);
    return () => clearTimeout(timeoutId);
  }, [textName, patternGroup, algorithm, configLoading]);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setText(event.target.result);
      };
      reader.readAsText(file);
    }
  };

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const result = await analyzeText(text, algorithm);
      // Store result and navigate to results
      localStorage.setItem('lastAnalysis', JSON.stringify({
        name: textName || 'Untitled',
        algorithm,
        result,
        timestamp: Date.now()
      }));
      navigate('/results');
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Error analyzing text. Make sure the API is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  const handleAdapt = () => {
    navigate('/patterns');
  };

  if (configLoading) {
    return (
      <div className="setup-page">
        <div className="setup-container">
          <div className="loading-state">Loading configuration...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="setup-page">
      <div className="setup-container">
        <div className="setup-header">
          <h1 className="setup-title">Automatic Patterns Detection</h1>
          <p className="setup-description">
            Textio detects user-defined patterns in text or individual words, using efficient
            algorithms like Knuth–Morris–Pratt and Boyer–Moore.
          </p>
          {saveStatus && <span className="save-status">{saveStatus}</span>}
        </div>

        <div className="setup-form">
          <div className="form-row">
            <input
              type="text"
              className="form-input"
              placeholder="Text name"
              value={textName}
              onChange={(e) => setTextName(e.target.value)}
            />
            <select
              className="form-select"
              value={patternGroup}
              onChange={(e) => setPatternGroup(e.target.value)}
            >
              <option value="Claims">Claims</option>
              <option value="Complaints">Complaints</option>
              <option value="Custom">Custom</option>
            </select>
          </div>

          <div className="text-area-container">
            <textarea
              className="form-textarea"
              placeholder="Insert text here or add a file..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <label className="upload-btn">
              <span className="upload-icon">↑</span>
              <span>Upload File</span>
              <input type="file" accept=".txt,.csv" onChange={handleFileUpload} hidden />
            </label>
          </div>

          <div className="form-actions">
            <select
              className="form-select algorithm-select"
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value)}
            >
              <option value="kmp">KMP</option>
              <option value="boyer_moore">Boyer-Moore</option>
            </select>
            <button className="btn btn-secondary " onClick={handleAdapt}>
              Setup
            </button>
            <button 
              className="btn btn-go" 
              onClick={handleAnalyze}
              disabled={loading || !text.trim()}
            >
              {loading ? 'Analyzing...' : 'GO!'}
            </button>
          </div>
        </div>

        <div className="patterns-info">
          <p className="patterns-count">
            <strong>{patterns.length}</strong> patterns loaded
          </p>
        </div>
      </div>
    </div>
  );
}

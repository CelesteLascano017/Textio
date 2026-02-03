import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPatterns, createPattern, updatePattern, deletePattern } from '../api/detector';
import './PatternConfig.css';

const categoryOptions = [
  'Queja leve',
  'Reclamo',
  'Reclamo crítico',
  'Riesgo legal'
];

const alertOptions = ['Bajo', 'Medio', 'Alto'];

// Map UI values to backend values
const alertToBackend = { 'Alto': 'high', 'Medio': 'medium', 'Bajo': 'low' };
const alertToUI = { 'high': 'Alto', 'medium': 'Medio', 'low': 'Bajo' };

const categoryToBackend = {
  'Queja leve': 'problema_general',
  'Reclamo': 'reclamo',
  'Reclamo crítico': 'reclamo_critico',
  'Riesgo legal': 'riesgo_legal'
};

export default function PatternConfig() {
  const navigate = useNavigate();
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');
  const [hasChanges, setHasChanges] = useState(false);

  useEffect(() => {
    loadPatterns();
  }, []);

  const loadPatterns = async () => {
    try {
      const data = await getPatterns();
      // Transform API data to UI format with index
      const transformed = (data.patterns || []).map((p, index) => ({
        index,
        pattern: p.pattern,
        category: mapCategoryToUI(p.category),
        alertLevel: alertToUI[p.alert_level] || 'Bajo',
        original: { ...p, index }
      }));
      setPatterns(transformed);
      setHasChanges(false);
    } catch (error) {
      console.error('Failed to load patterns:', error);
      setSaveMessage('Error loading patterns');
    } finally {
      setLoading(false);
    }
  };

  const mapCategoryToUI = (category) => {
    const map = {
      'producto_defectuoso': 'Queja leve',
      'problema_general': 'Queja leve',
      'producto_no_funcional': 'Reclamo',
      'producto_danado': 'Reclamo crítico',
      'producto_incompleto': 'Queja leve',
      'demora_entrega': 'Queja leve',
      'entrega_faltante': 'Reclamo crítico',
      'entrega_perdida': 'Reclamo crítico',
      'daño': 'Reclamo',
      'problema_calidad': 'Queja leve',
      'insatisfaccion': 'Queja leve',
      'muy_malo': 'Reclamo',
      'malo': 'Queja leve',
      'fraude': 'Riesgo legal',
      'engano': 'Riesgo legal',
      'reclamo': 'Reclamo',
      'reclamo_critico': 'Reclamo crítico',
      'riesgo_legal': 'Riesgo legal'
    };
    return map[category] || 'Queja leve';
  };

  const updatePatternField = (index, field, value) => {
    const updated = [...patterns];
    updated[index][field] = value;
    setPatterns(updated);
    setHasChanges(true);
  };

  const addNewPattern = () => {
    setPatterns([...patterns, { 
      index: -1, // New pattern marker
      pattern: '', 
      category: 'Queja leve', 
      alertLevel: 'Bajo',
      isNew: true
    }]);
    setEditMode(true);
    setHasChanges(true);
  };

  const removePattern = async (index) => {
    const patternToRemove = patterns[index];
    
    if (patternToRemove.isNew) {
      // Just remove from local state
      setPatterns(patterns.filter((_, i) => i !== index));
    } else {
      // Delete from backend
      setSaving(true);
      try {
        await deletePattern(patternToRemove.original.index);
        await loadPatterns(); // Reload to get fresh indices
        setSaveMessage('Pattern deleted successfully');
        setTimeout(() => setSaveMessage(''), 3000);
      } catch (error) {
        console.error('Failed to delete pattern:', error);
        setSaveMessage('Error deleting pattern');
      } finally {
        setSaving(false);
      }
    }
  };

  const saveChanges = async () => {
    setSaving(true);
    setSaveMessage('');
    
    try {
      for (let i = 0; i < patterns.length; i++) {
        const p = patterns[i];
        const patternData = {
          pattern: p.pattern,
          category: categoryToBackend[p.category] || 'problema_general',
          alert_level: alertToBackend[p.alertLevel] || 'low',
          alert_message: `Patrón "${p.pattern}" detectado`
        };
        
        if (p.isNew && p.pattern.trim()) {
          // Create new pattern
          await createPattern(patternData);
        } else if (!p.isNew && p.original && p.pattern.trim()) {
          // Check if pattern, category, or alert_level changed
          const originalCategory = categoryToBackend[mapCategoryToUI(p.original.category)];
          const newCategory = categoryToBackend[p.category];
          const hasChanged = 
            p.pattern !== p.original.pattern ||
            alertToBackend[p.alertLevel] !== p.original.alert_level ||
            newCategory !== p.original.category;
          
          if (hasChanged) {
            await updatePattern(p.original.index, patternData);
          }
        }
      }
      
      await loadPatterns(); // Reload to get fresh data
      setSaveMessage('Changes saved successfully!');
      setHasChanges(false);
      setTimeout(() => setSaveMessage(''), 3000);
    } catch (error) {
      console.error('Failed to save patterns:', error);
      setSaveMessage(`Error: ${error.message}`);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="pattern-config-page">
        <div className="pattern-config-container">
          <p className="loading-text">Loading patterns...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="pattern-config-page">
      <div className="pattern-config-container">
        <div className="pattern-config-header">
          <h1 className="pattern-config-title">Configurable list of patterns</h1>
          <p className="pattern-config-description">
            Configure exactly which patterns Textio detects in text. Add new
            patterns, assign categories and alert levels, or edit existing patterns.
          </p>
          {saveMessage && (
            <div className={`save-message ${saveMessage.includes('Error') ? 'error' : 'success'}`}>
              {saveMessage}
            </div>
          )}
        </div>

        <div className="pattern-config-content">
          <div className="pattern-group-header">
            <span className="pattern-group-name">Claims ({patterns.length})</span>
            <div className="pattern-group-actions">
              <button 
                className="btn btn-secondary"
                onClick={addNewPattern}
              >
                + ADD
              </button>
              <button 
                className={`btn ${editMode ? 'btn-accent' : 'btn-secondary'}`}
                onClick={() => setEditMode(!editMode)}
              >
                {editMode ? 'VIEW' : 'EDIT'}
              </button>
              {hasChanges && (
                <button 
                  className="btn btn-save"
                  onClick={saveChanges}
                  disabled={saving}
                >
                  {saving ? 'Saving...' : 'SAVE'}
                </button>
              )}
            </div>
          </div>

          <div className="pattern-table">
            <div className="pattern-table-header">
              <span className="col-pattern">Patterns</span>
              <span className="col-category">Category</span>
              <span className="col-alert">Alert Level</span>
              {editMode && <span className="col-actions">Actions</span>}
            </div>

            <div className="pattern-table-body">
              {patterns.map((p, index) => (
                <div key={index} className={`pattern-table-row ${p.isNew ? 'new-pattern' : ''}`}>
                  <span className="col-pattern">
                    {editMode ? (
                      <input
                        type="text"
                        value={p.pattern}
                        onChange={(e) => updatePatternField(index, 'pattern', e.target.value)}
                        className="pattern-input"
                        placeholder="Enter pattern..."
                      />
                    ) : (
                      p.pattern
                    )}
                  </span>
                  <span className="col-category">
                    {editMode ? (
                      <select
                        value={p.category}
                        onChange={(e) => updatePatternField(index, 'category', e.target.value)}
                        className="pattern-select"
                      >
                        {categoryOptions.map(opt => (
                          <option key={opt} value={opt}>{opt}</option>
                        ))}
                      </select>
                    ) : (
                      <span className="category-tag">{p.category}</span>
                    )}
                  </span>
                  <span className="col-alert">
                    {editMode ? (
                      <select
                        value={p.alertLevel}
                        onChange={(e) => updatePatternField(index, 'alertLevel', e.target.value)}
                        className="pattern-select"
                      >
                        {alertOptions.map(opt => (
                          <option key={opt} value={opt}>{opt}</option>
                        ))}
                      </select>
                    ) : (
                      <span className={`alert-tag alert-${p.alertLevel.toLowerCase()}`}>
                        {p.alertLevel}
                      </span>
                    )}
                  </span>
                  {editMode && (
                    <span className="col-actions">
                      <button 
                        className="btn-delete"
                        onClick={() => removePattern(index)}
                        title="Delete pattern"
                      >
                        ✕
                      </button>
                    </span>
                  )}
                </div>
              ))}
              {patterns.length === 0 && (
                <div className="no-patterns">
                  No patterns configured. Click ADD to create one.
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="pattern-config-actions">
          <button className="btn btn-secondary" onClick={() => navigate('/')}>
            ← Back to Setup
          </button>
        </div>
      </div>
    </div>
  );
}

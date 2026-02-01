import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPatterns } from '../api/detector';
import './PatternConfig.css';

const categoryOptions = [
  'Queja leve',
  'Reclamo',
  'Reclamo crítico',
  'Riesgo legal'
];

const alertOptions = ['Bajo', 'Medio', 'Alto'];

export default function PatternConfig() {
  const navigate = useNavigate();
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    loadPatterns();
  }, []);

  const loadPatterns = async () => {
    try {
      const data = await getPatterns();
      // Transform API data to UI format
      const transformed = (data.patterns || []).map(p => ({
        pattern: p.pattern,
        category: mapCategoryToUI(p.category),
        alertLevel: mapAlertToUI(p.alert_level)
      }));
      setPatterns(transformed);
    } catch (error) {
      console.error('Failed to load patterns:', error);
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
      'engano': 'Riesgo legal'
    };
    return map[category] || 'Queja leve';
  };

  const mapAlertToUI = (level) => {
    const map = { 'high': 'Alto', 'medium': 'Medio', 'low': 'Bajo' };
    return map[level] || 'Bajo';
  };

  const updatePattern = (index, field, value) => {
    const updated = [...patterns];
    updated[index][field] = value;
    setPatterns(updated);
  };

  const addPattern = () => {
    setPatterns([...patterns, { pattern: '', category: 'Queja leve', alertLevel: 'Bajo' }]);
    setEditMode(true);
  };

  if (loading) {
    return (
      <div className="pattern-config-page">
        <div className="pattern-config-container">
          <p>Loading patterns...</p>
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
            Glyph lets you configure exactly which patterns it detects in text. You can add new
            patterns, assign them a category and alert level, and fine-tune their parameters,
            or easily edit existing patterns to match your needs
          </p>
        </div>

        <div className="pattern-config-content">
          <div className="pattern-group-header">
            <span className="pattern-group-name">Claims</span>
            <div className="pattern-group-actions">
              <button 
                className={`btn ${!editMode ? 'btn-primary' : 'btn-secondary'}`}
                onClick={addPattern}
              >
                ADD
              </button>
              <button 
                className={`btn ${editMode ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setEditMode(!editMode)}
              >
                EDIT
              </button>
            </div>
          </div>

          <div className="pattern-table">
            <div className="pattern-table-header">
              <span className="col-pattern">Patterns</span>
              <span className="col-category">Category</span>
              <span className="col-alert">Alert Level</span>
            </div>

            <div className="pattern-table-body">
              {patterns.map((p, index) => (
                <div key={index} className="pattern-table-row">
                  <span className="col-pattern">
                    {editMode ? (
                      <input
                        type="text"
                        value={p.pattern}
                        onChange={(e) => updatePattern(index, 'pattern', e.target.value)}
                        className="pattern-input"
                      />
                    ) : (
                      p.pattern
                    )}
                  </span>
                  <span className="col-category">
                    {editMode ? (
                      <select
                        value={p.category}
                        onChange={(e) => updatePattern(index, 'category', e.target.value)}
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
                        onChange={(e) => updatePattern(index, 'alertLevel', e.target.value)}
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
                </div>
              ))}
              {editMode && (
                <div className="pattern-table-row add-row" onClick={addPattern}>
                  <span className="col-pattern">Add ↩</span>
                  <span className="col-category">Add ↩</span>
                  <span className="col-alert">Add ↩</span>
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

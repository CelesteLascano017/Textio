import './PatternsList.css';

// Map alert_level from API to display label
const getAlertLabel = (alertLevel) => {
  const labels = {
    'high': 'Alto',
    'medium': 'Medio',
    'low': 'Bajo'
  };
  return labels[alertLevel] || 'Bajo';
};

// Get CSS class for alert level styling
const getAlertClass = (alertLevel) => {
  const classes = {
    'high': 'alert-high',
    'medium': 'alert-medium',
    'low': 'alert-low'
  };
  return classes[alertLevel] || 'alert-low';
};

// Get category display name
const getCategoryLabel = (category) => {
  const labels = {
    'producto_defectuoso': 'Producto Defectuoso',
    'problema_general': 'Problema General',
    'producto_no_funcional': 'Producto No Funcional',
    'producto_danado': 'Producto Dañado',
    'producto_incompleto': 'Producto Incompleto',
    'demora_entrega': 'Demora en Entrega',
    'entrega_faltante': 'Entrega Faltante',
    'entrega_perdida': 'Entrega Perdida',
    'daño': 'Daño',
    'problema_calidad': 'Problema de Calidad',
    'insatisfaccion': 'Insatisfacción',
    'muy_malo': 'Muy Malo',
    'malo': 'Malo',
    'decepcion': 'Decepción',
    'devolucion': 'Devolución',
    'cambio_producto': 'Cambio de Producto',
    'desconfianza': 'Desconfianza',
    'fraude': 'Fraude',
    'engano': 'Engaño',
    'confuso': 'Confuso',
    'solicitud_ayuda': 'Solicitud de Ayuda',
    'reclamo': 'Reclamo',
    'reclamo_critico': 'Reclamo Crítico',
    'riesgo_legal': 'Riesgo Legal',
    'test_category': 'Test'
  };
  return labels[category] || category;
};

export default function PatternsList({ detections = [] }) {
  if (detections.length === 0) {
    return (
      <div className="patterns-list">
        <h4 className="patterns-title">Patterns found</h4>
        <p className="patterns-empty">No patterns detected</p>
      </div>
    );
  }

  return (
    <div className="patterns-list">
      <h4 className="patterns-title">Patterns found</h4>
      <ul className="patterns-items">
        {detections.map((detection, index) => (
          <li key={index} className="pattern-row">
            <span className="pattern-name">{detection.alert_message || detection.pattern}</span>
            <span className="pattern-arrow">→</span>
            <span className="pattern-category">{getCategoryLabel(detection.category)}</span>
            <span className={`pattern-alert ${getAlertClass(detection.alert_level)}`}>
              {getAlertLabel(detection.alert_level)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

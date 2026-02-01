import './PatternsList.css';

const getCategoryLabel = (category) => {
  const labels = {
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
    'decepcion': 'Queja leve',
    'devolucion': 'Reclamo',
    'cambio_producto': 'Queja leve',
    'desconfianza': 'Queja leve',
    'fraude': 'Riesgo legal',
    'engano': 'Riesgo legal',
    'confuso': 'Queja leve',
    'solicitud_ayuda': 'Queja leve'
  };
  return labels[category] || 'Queja leve';
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
            <span className={`pattern-category cat-${getCategoryLabel(detection.category).toLowerCase().replace(' ', '-')}`}>
              {getCategoryLabel(detection.category)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

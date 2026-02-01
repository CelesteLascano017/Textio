import './HighlightedText.css';

export default function HighlightedText({ text, detections = [] }) {
  if (!text || detections.length === 0) {
    return <span>{text}</span>;
  }

  // Get all pattern positions
  const highlights = [];
  detections.forEach(detection => {
    detection.positions.forEach(pos => {
      highlights.push({
        start: pos,
        end: pos + detection.pattern.length,
        pattern: detection.pattern
      });
    });
  });

  // Sort by position
  highlights.sort((a, b) => a.start - b.start);

  // Build highlighted text
  const parts = [];
  let lastIndex = 0;

  highlights.forEach((hl, i) => {
    // Add text before this highlight
    if (hl.start > lastIndex) {
      parts.push(
        <span key={`text-${i}`}>{text.slice(lastIndex, hl.start)}</span>
      );
    }
    // Add highlighted part
    parts.push(
      <span key={`hl-${i}`} className="highlight-pattern">
        {text.slice(hl.start, hl.end)}
      </span>
    );
    lastIndex = hl.end;
  });

  // Add remaining text
  if (lastIndex < text.length) {
    parts.push(<span key="text-end">{text.slice(lastIndex)}</span>);
  }

  return <span className="highlighted-text">{parts}</span>;
}

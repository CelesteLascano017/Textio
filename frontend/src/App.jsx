import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Setup from './pages/Setup';
import Results from './pages/Results';
import Analysis from './pages/Analysis';
import PatternConfig from './pages/PatternConfig';

function App() {
  return (
    <BrowserRouter>
      <Header />
      <main className="page">
        <Routes>
          <Route path="/" element={<Setup />} />
          <Route path="/results" element={<Results />} />
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/patterns" element={<PatternConfig />} />
          <Route path="/account" element={<div className="container"><h1>Account</h1><p style={{color: 'var(--color-text-secondary)'}}>Coming soon...</p></div>} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;

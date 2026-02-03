import { NavLink } from 'react-router-dom';
import './Header.css';

export default function Header() {
  return (
    <header className="header">
      <div className="header-container">
        <NavLink to="/" className="logo">
          <span className="logo-icon">★</span>
          <span className="logo-text">Textio</span>
        </NavLink>
        
        <nav className="nav">
          <NavLink to="/patterns" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Setup
          </NavLink>
          <NavLink to="/results" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Results
          </NavLink>
          <NavLink to="/account" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Account
          </NavLink>
        </nav>
      </div>
    </header>
  );
}

import { LogoIcon } from "../icons/Icons.jsx";

function Header({ onReset }) {
  return (
    <div className="header" onClick={onReset}>
      <div className="header-logo">
        <LogoIcon />
      </div>
      <div className="header-text">
        <h2>Obiadowo</h2>
      </div>
      <button className="header-button" onClick={onReset}>
        Nowy czat
      </button>
    </div>
  );
}

export default Header;

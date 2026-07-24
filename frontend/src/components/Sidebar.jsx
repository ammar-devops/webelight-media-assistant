import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <h2 className="sidebar-logo">AI Media</h2>

      <NavLink to="/">Dashboard</NavLink>

      <NavLink to="/history">History</NavLink>

      <NavLink to="/settings">Settings</NavLink>

      <NavLink to="/about">About</NavLink>
    </aside>
  );
}

export default Sidebar;

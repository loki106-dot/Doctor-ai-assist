export default function RoleSelect({ onSelect }) {
  return (
    <div className="card">
      <h2>Select Role</h2>
      <button onClick={() => onSelect("patient")}>Patient</button>
      <button onClick={() => onSelect("doctor")}>Doctor</button>
    </div>
  );
}

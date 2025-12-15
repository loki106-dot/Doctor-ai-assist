import { useState } from "react";
import RoleSelect from "./components/RoleSelect";
import ChatBox from "./components/ChatBox";
import "./styles.css";

const patients = ["Patient1", "Patient2", "Patient3"];
const doctors = ["Ahuja", "Ram", "Bala"];

function App() {
  const [role, setRole] = useState(null);
  const [identity, setIdentity] = useState(null);
  const [selectedDoctor, setSelectedDoctor] = useState(null);

  // ---------------- ROLE SELECT ----------------
  if (!role) {
    return <RoleSelect onSelect={setRole} />;
  }

  // ---------------- PATIENT FLOW ----------------
  if (role === "patient") {
    if (!identity) {
      return (
        <div className="card">
          <h2>Select Patient</h2>
          {patients.map(name => (
            <button key={name} onClick={() => setIdentity(name)}>
              {name}
            </button>
          ))}
          <button onClick={() => setRole(null)}>⬅ Back</button>
        </div>
      );
    }

    if (!selectedDoctor) {
      return (
        <div className="card">
          <h2>Select Doctor</h2>
          {doctors.map(name => (
            <button key={name} onClick={() => setSelectedDoctor(name)}>
              Dr. {name}
            </button>
          ))}
          <button onClick={() => setIdentity(null)}>⬅ Back</button>
        </div>
      );
    }
  }

  // ---------------- DOCTOR FLOW ----------------
  if (role === "doctor" && !identity) {
    return (
      <div className="card">
        <h2>Select Doctor</h2>
        {doctors.map(name => (
          <button key={name} onClick={() => setIdentity(name)}>
            Dr. {name}
          </button>
        ))}
        <button onClick={() => setRole(null)}>⬅ Back</button>
      </div>
    );
  }

  // ---------------- CHAT ----------------
  return (
    <>
      <ChatBox
        role={role}
        identity={identity}
        selectedDoctor={selectedDoctor}
      />

      <button
        className="logout"
        onClick={() => {
          setIdentity(null);
          setSelectedDoctor(null);
          setRole(null);
        }}
      >
        Logout
      </button>
    </>
  );
}

export default App;

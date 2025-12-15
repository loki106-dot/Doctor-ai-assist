import { useState } from "react";
import { sendChat } from "../api";
import MessageBubble from "./MessageBubble";

export default function ChatBox({ role, identity }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const send = async (customMessage = null) => {
    const content = customMessage ?? input;
    if (!content.trim()) return;

    const newMessages = [...messages, { role: "user", content }];
    setMessages(newMessages);
    setInput("");

    const payload = {
      user_role: role,
      messages: newMessages,
      ...(role === "patient"
        ? { patient_name: identity }
        : { doctor_name: identity })
    };

    const res = await sendChat(payload);

    setMessages([
      ...newMessages,
      { role: "assistant", content: res.reply }
    ]);
  };

  return (
    <div className="chat">
      <h3>{role.toUpperCase()} – {identity}</h3>

      {/* 🔹 Doctor Dashboard Button */}
      {role === "doctor" && (
        <div style={{ marginBottom: "10px" }}>
          <button
            onClick={() => send("Give me today’s report")}
            style={{
              background: "#4CAF50",
              color: "white",
              padding: "8px 12px",
              borderRadius: "5px",
              border: "none",
              cursor: "pointer"
            }}
          >
            📊 Generate Today’s Report
          </button>
        </div>
      )}

      <div className="messages">
        {messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} content={m.content} />
        ))}
      </div>

      <div className="input-row">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type here..."
        />
        <button onClick={() => send()}>Send</button>
      </div>
    </div>
  );
}

export default function MessageBubble({ role, content }) {
  return (
    <div className={`bubble ${role}`}>
      <b>{role}:</b> {content}
    </div>
  );
}

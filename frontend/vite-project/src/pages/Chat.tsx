import { useState } from "react";
import { askCareer } from "../Services/ChatService";

function Chat() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!message.trim()) return;

    setLoading(true);

    try {
      const response = await askCareer({
        message,
        session_id: "default",
      });

      setReply(response.response);
    } catch (error) {
      console.error(error);
      alert("Failed to get response");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Career Chatbot</h2>

      <textarea
        rows={4}
        cols={50}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask a career question..."
      />

      <br />
      <br />

      <button onClick={handleSend} disabled={loading}>
        {loading ? "Thinking..." : "Send"}
      </button>

      <br />
      <br />

      <h3>Response</h3>
      <p>{reply}</p>
    </div>
  );
}

export default Chat;
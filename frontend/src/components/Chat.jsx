import { useState } from "react";
import api from "../api/api";

function Chat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    const jobId = localStorage.getItem("job_id");

    if (!jobId) return;

    const userMessage = {
      role: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      const { data } = await api.post("/chat", {
        job_id: jobId,
        question,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.answer,
        },
      ]);

      setQuestion("");
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div className="card">
      <h2>AI Chat</h2>

      <div className="chat-box">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={msg.role === "user" ? "user-message" : "bot-message"}
          >
            {msg.text}
          </div>
        ))}

        {loading && <div className="bot-message">Thinking...</div>}
      </div>

      <input
        type="text"
        placeholder="Ask about this media..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askQuestion}>Send</button>
    </div>
  );
}

export default Chat;

import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");
  const chatEndRef = useRef(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadStatus("");
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setUploadStatus("Uploading...");

    try {
      await axios.post("http://localhost:8000/upload", formData);
      setUploadStatus("✅ File uploaded successfully.");
    } catch (error) {
      console.error("Upload error:", error);
      setUploadStatus("❌ Upload failed.");
    }
  };

  const askQuestion = async () => {
    if (!inputValue.trim()) return;

    setMessages((prev) => [...prev, { from: "user", text: inputValue }]);
    setLoading(true);

    const formData = new FormData();
    formData.append("question", inputValue);

    try {
      const res = await axios.post("http://localhost:8000/ask", formData);
      setMessages((prev) => [...prev, { from: "bot", text: res.data.answer }]);
    } catch (error) {
      console.error("Ask error:", error);
      setMessages((prev) => [
        ...prev,
        {
          from: "bot",
          text: `❌ Error: ${
            error.response?.data?.error || error.message || "Unknown error"
          }`,
        },
      ]);
    } finally {
      setInputValue("");
      setLoading(false);
    }
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="app-container">
      <h1>📚 RAG Chatbot</h1>

      <div className="upload-box">
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload & Embed</button>
      </div>
      {uploadStatus && <p className="status">{uploadStatus}</p>}

      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.from}`}>
            {msg.text}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Ask your question..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && askQuestion()}
        />
        <button onClick={askQuestion} disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>
    </div>
  );
}

export default App;

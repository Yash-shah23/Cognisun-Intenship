import React, { useState } from "react";

function Chat() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return alert("Please select a file.");

    setUploading(true);
    setStatus("Uploading and embedding file. Please wait...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error(await res.text());
      setStatus("✅ File uploaded. Embedding in progress...");
    } catch (err) {
      alert("Upload failed: " + err.message);
      setStatus("");
    } finally {
      setUploading(false);
    }
  };

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("question", question);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResponse(data.answer);
    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "auto", padding: "2rem" }}>
      <h2 style={{ textAlign: "center" }}>📄 Document QA Chatbot</h2>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={uploading} style={{ marginLeft: "10px" }}>
        {uploading ? "Uploading..." : "Upload"}
      </button>

      <p style={{ color: "gray" }}>{status}</p>

      <div style={{ marginTop: "30px" }}>
        <input
          type="text"
          placeholder="Ask your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{ width: "70%", padding: "10px" }}
        />
        <button onClick={askQuestion} disabled={loading} style={{ marginLeft: "10px" }}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>

      <div style={{ marginTop: "30px", background: "#f5f5f5", padding: "20px", borderRadius: "10px" }}>
        <strong>Answer:</strong>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default Chat;

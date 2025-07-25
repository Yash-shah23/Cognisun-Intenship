import React, { useState } from "react";
import axios from "axios";

function ChatBox() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [file, setFile] = useState(null);

  const handleSubmit = async () => {
    const res = await axios.post("http://localhost:8000/ask", { question });
    setAnswer(res.data.answer);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    await axios.post("http://localhost:8000/upload", formData);
    alert("File uploaded and processed!");
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload File</button>
      <br /><br />
      <input
        type="text"
        placeholder="Ask in any language"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={handleSubmit}>Ask</button>
      <p><strong>Answer:</strong> {answer}</p>
    </div>
  );
}

export default ChatBox;

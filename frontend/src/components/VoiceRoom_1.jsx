import { useState } from "react";

export default function VoiceRoom() {

  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");
  const [file, setFile] = useState(null);

  const uploadDocument = async () => {

    if (!file) {
      alert("Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData
    });

    alert("Document uploaded successfully");
  };

  const startListening = () => {

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";

    recognition.onresult = async (event) => {

      const text = event.results[0][0].transcript;

      setTranscript(text);

      const res = await fetch(
        `http://127.0.0.1:8000/ask-stream?query=${encodeURIComponent(text)}`
      );

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      let aiText = "";

      while (true) {

        const { done, value } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value);

        aiText += chunk;

        setResponse(aiText);
      }

      speak(aiText);
    };

    recognition.start();
  };

  const speak = (text) => {

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";

    window.speechSynthesis.speak(speech);
  };

  return (
    <div style={{ padding: 40 }}>

      <h2>EchoMind AI Voice Assistant</h2>

      <h3>Upload Knowledge Document</h3>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadDocument}>
        Upload
      </button>

      <hr />

      <button onClick={startListening}>
        🎤 Speak
      </button>

      <h3>User:</h3>
      <p>{transcript}</p>

      <h3>AI:</h3>
      <p>{response}</p>

    </div>
  );
}
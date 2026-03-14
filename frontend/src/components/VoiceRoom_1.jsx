import { useState } from "react";

export default function VoiceRoom() {

  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");
  const [sources, setSources] = useState([]);
  const [latency, setLatency] = useState(null);
  const [trace, setTrace] = useState([]);
  const [file, setFile] = useState(null);

  const uploadDocument = async () => {

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData
    });
  };

  const startListening = () => {

    const recognition = new window.webkitSpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = true;

    recognition.onresult = async (event) => {

      let text = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        text += event.results[i][0].transcript;
      }

      setTranscript(text);

      if (event.results[0].isFinal) {

        const res = await fetch(
          `http://127.0.0.1:8000/ask-stream?query=${encodeURIComponent(text)}`
        );

        const src = res.headers.get("X-Sources");
        const ragLatency = res.headers.get("X-Rag-Latency");
        const traceSteps = res.headers.get("X-Trace");

        if (src) setSources(src.split(","));
        if (ragLatency) setLatency(ragLatency);
        if (traceSteps) setTrace(traceSteps.split("|"));

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

        const speech = new SpeechSynthesisUtterance(aiText);
        speech.lang = "en-US";
        window.speechSynthesis.speak(speech);
      }
    };

    recognition.start();
  };

  return (
    <div className="main-grid">

      <div className="card upload-card">
        <h2>Knowledge Base</h2>

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button onClick={uploadDocument}>
          Upload Document
        </button>
      </div>

      <div className="card voice-card">

        <h2>Voice Interaction</h2>

        <button className="mic-btn" onClick={startListening}>
          🎤 Speak
        </button>

        <div className="panel">
          <h3>User</h3>
          <p>{transcript}</p>
        </div>

        <div className="panel">
          <h3>AI</h3>
          <p>{response}</p>
        </div>

      </div>

      <div className="card rag-card">

        <h2>RAG Insights</h2>

        <div className="panel">
          <h3>Sources</h3>
          <ul>
            {sources.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>

        <div className="panel">
          <h3>Latency</h3>
          <p>{latency} ms</p>
        </div>

        <div className="panel">
          <h3>Agent Trace</h3>
          <ul>
            {trace.map((t, i) => (
              <li key={i}>{t}</li>
            ))}
          </ul>
        </div>

      </div>

    </div>
  );
}
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

        speak(aiText);
      }
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

      <h3>User</h3>
      <p>{transcript}</p>

      <h3>AI</h3>
      <p>{response}</p>

      <h3>Sources Used</h3>
      <ul>
        {sources.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ul>

      <h3>Latency</h3>
      <p>RAG: {latency} ms</p>

      <h3>Agent Trace</h3>
      <ul>
        {trace.map((t, i) => (
          <li key={i}>{t}</li>
        ))}
      </ul>

    </div>
  );
}
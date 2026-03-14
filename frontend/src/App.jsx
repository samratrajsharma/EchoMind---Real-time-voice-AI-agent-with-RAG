import VoiceRoom from "./components/VoiceRoom_1";
import "./index.css";

function App() {
  return (
    <div className="app-container">
      <header className="header">
        <h1>EchoMind</h1>
        <p>AI Voice Knowledge Assistant</p>
      </header>

      <VoiceRoom />
    </div>
  );
}

export default App;
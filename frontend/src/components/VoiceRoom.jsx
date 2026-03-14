import { useEffect, useState } from "react";
import axios from "axios";
import { Room } from "livekit-client";

function VoiceRoom() {
  const [room, setRoom] = useState(null);

  useEffect(() => {
    joinRoom();
  }, []);

  const joinRoom = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/livekit-token"
      );

      const token = res.data.token;

      const newRoom = new Room();

      await newRoom.connect(
        "ws://localhost:7880",
        token
      );

      setRoom(newRoom);

      console.log("Connected to LiveKit room");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h3>Voice Room</h3>
      {room ? (
        <p>Connected to EchoMind voice agent</p>
      ) : (
        <p>Connecting...</p>
      )}
    </div>
  );
}

export default VoiceRoom;
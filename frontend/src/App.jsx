import { useState } from 'react';
import './App.css';
import VideoCall from './VideoCall';

function App() {
  const [inCall, setInCall] = useState(false);
  const [roomID, setRoomID] = useState('');
  const [userName, setUserName] = useState('');
  const [token, setToken] = useState(''); // Store token fetched from backend

  const handleJoin = async () => {
    if (!roomID || !userName) {
      alert("Please enter Room ID and User Name");
      return;
    }

    // Fetch token from backend
    try {
      const response = await fetch(`http://localhost:8000/token?userID=${userName}&roomID=${roomID}`);
      const data = await response.json();
      if (data.token) {
        setToken(data.token);
        setInCall(true);
      } else {
        console.error("No token received", data);
        alert("Failed to get token from backend. Check console.");
        // For testing without backend token logic working yet, uncomment below:
        // setInCall(true); 
      }
    } catch (error) {
      console.error("Error fetching token:", error);
      alert("Backend not reachable");
    }
  };

  return (
    <div className="App">
      {!inCall ? (
        <div className="join-screen">
          <h1>Zego Video Call Experiment</h1>
          <div className="input-group">
            <input
              type="text"
              placeholder="Enter Room ID"
              value={roomID}
              onChange={(e) => setRoomID(e.target.value)}
            />
            <input
              type="text"
              placeholder="Enter User Name"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
            />
            <button onClick={handleJoin}>Join Room</button>
          </div>
        </div>
      ) : (
        <VideoCall
          roomID={roomID}
          userID={userName}
          userName={userName}
          appID={1481566233} // REPLACE WITH YOUR APP ID
          token={token}
        />
      )}
    </div>
  );
}

export default App;

import React, { useEffect, useRef } from 'react';
import { ZegoUIKitPrebuilt } from '@zegocloud/zego-uikit-prebuilt';

export default function VideoCall({ roomID, userID, userName, appID, token }) {
  const containerRef = useRef(null);

  useEffect(() => {
    const myMeeting = async (element) => {
      // Fetch token from production backend
      const response = await fetch(`https://video-calling-mockapp-2.onrender.com/token?userID=${userID}&roomID=${roomID}`);
      const data = await response.json();
      const serverToken = data.token;

      // Generate Kit Token (Production mode)
      const kitToken = ZegoUIKitPrebuilt.generateKitTokenForProduction(
        appID,
        serverToken,
        roomID,
        userID,
        userName
      );

      // Create instance object from Kit Token.
      const zp = ZegoUIKitPrebuilt.create(kitToken);

      // Start the call
      zp.joinRoom({
        container: element,
        sharedLinks: [
          {
            name: 'Personal link',
            url:
              window.location.protocol + '//' +
              window.location.host + window.location.pathname +
              '?roomID=' +
              roomID,
          },
        ],
        scenario: {
          mode: ZegoUIKitPrebuilt.VideoConference, // To implement 1-on-1 calls, modify the parameter here to [ZegoUIKitPrebuilt.OneONOneCall].
        },
      });
    };

    if (containerRef.current) {
      myMeeting(containerRef.current);
    }
  }, [roomID, userID, userName, appID, token]);

  return (
    <div
      className="myCallContainer"
      ref={containerRef}
      style={{ width: '100vw', height: '100vh' }}
    ></div>
  );
}

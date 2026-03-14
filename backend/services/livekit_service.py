from livekit import rtc
from backend.config import LIVEKIT_URL

class LiveKitService:

    def __init__(self):
        self.room = rtc.Room()

    async def connect(self, token):

        await self.room.connect(LIVEKIT_URL, token)

        print("Connected to LiveKit room")

        return self.room

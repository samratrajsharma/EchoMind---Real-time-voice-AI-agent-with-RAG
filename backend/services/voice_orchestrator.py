import requests

from backend.services.stt_service import DeepgramSTT
from backend.services.tts_service import EdgeTTS

class VoiceOrchestrator:
    def __init__(self):
        self.stt  =DeepgramSTT()
        self.tts = EdgeTTS()

    async def process_voice(self, audio_stream):
        transcript = await self.stt.transcribe_stream(audio_stream)

        print('User said:', transcript)

        response = requests.post(
            'http://127.0.0.1:8000/ask',
            params = {'query': transcript}

        )

        answer = response.json()['answer']

        print('AI Response:', answer)

        audio_output = self.tts.speak_stream(answer)

        return audio_output
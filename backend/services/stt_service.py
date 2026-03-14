from deepgram import DeepgramClient, LiveTranscriptionEvents
from backend.config import DEEPGRAM_API_KEY


class DeepgramSTT:

    def __init__(self):
        self.client = DeepgramClient(DEEPGRAM_API_KEY)

    async def transcribe_stream(self, audio_stream, on_transcript):

        dg_connection = self.client.listen.live.v("1")

        async def on_message(self, result, **kwargs):

            sentence = result.channel.alternatives[0].transcript

            if result.is_final and sentence:
                print("FINAL STT:", sentence)
                await on_transcript(sentence)


        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        await dg_connection.start(
            {
                "model": "nova-2",
                "language": "en",
                "smart_format": True,
                "interim_results": True
            }
        )

        async for chunk in audio_stream:
            await dg_connection.send(chunk)

        await dg_connection.finish()
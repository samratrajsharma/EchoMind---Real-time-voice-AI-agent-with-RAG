import edge_tts


class EdgeTTS:

    def __init__(self):
        self.stop_signal = False

    async def speak_stream(self, text_stream, on_audio_chunk):

        async for text_chunk in text_stream:

            if self.stop_signal:
                print("TTS interrupted")
                break

            communicate = edge_tts.Communicate(
                text=text_chunk,
                voice="en-US-AriaNeural"
            )

            async for chunk in communicate.stream():

                if self.stop_signal:
                    print("Stopping audio playback")
                    break

                if chunk["type"] == "audio":
                    await on_audio_chunk(chunk["data"])
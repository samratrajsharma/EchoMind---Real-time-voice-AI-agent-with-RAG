import asyncio
from livekit.agents import JobContext, WorkerOptions, cli
from livekit import rtc
from backend.services.voice_orchestrator import VoiceOrchestrator

orchestrator = VoiceOrchestrator()

async def entrypoint(ctx: JobContext):

    print("EchoMind Agent Started")

    await ctx.connect()

    room = ctx.room

    print("Waiting for participant...")

    participant = await ctx.wait_for_participant()

    print(f"Participant joined: {participant.identity}")

    async def send_audio(chunk):
        print("Audio chunk generated")

    async def audio_stream():

        async for track in participant.audio_tracks():
            async for frame in track:
                yield frame.data

    await orchestrator.handle_voice_session(
        audio_stream(),
        send_audio
    )


if __name__ == "__main__":

    cli.run_app(
        WorkerOptions(
            entrypoint_fnc= entrypoint,
            ws_url= 'YOUR - LIVEKIT_URL',
            api_key = 'devkey',
            api_secret= 'secret'
        )
    )


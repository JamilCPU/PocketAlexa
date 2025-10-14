import asyncio
import websockets
from Utilities.AudioRecorder import AudioRecorder

async def chat():
    async with websockets.connect('ws://localhost:12345') as websocket:
        mode = input("Enter 'audio' or 'text'")
        while True:
            message = ""
            if mode == 'text':
                message = input("Enter message: ")
            else:
                recorder = AudioRecorder()
                print("Press Enter to start recording...")
                input()
                recorder.start_recording()
                print("Recording... Press Enter to stop and send.")
                input()              
                message = recorder.stop_recording()
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Received: {response}")

if __name__ == "__main__":
    asyncio.run(chat())
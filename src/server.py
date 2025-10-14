import asyncio
import websockets
import traceback

from Executor import Executor
from Interpreter import Interpreter
from Utilities.FileLogger import FileLogger

from Utilities.DownloadModel import ModelDownloader

connected_clients = set()

file = FileLogger()
file.setupLogging()

modelDownloader = ModelDownloader()
modelDownloader.routineSetupModel()

async def handle_client(websocket):
    execute = Executor()
    interpret = Interpreter()

    connected_clients.add(websocket)
    try:
        print(websocket)
        async for message in websocket:
            try:
                if isinstance(message, bytes):
                    file.writeToFile("Audio Message received from CLIENT: 'PARSING'")
                    message = interpret.parseSpeech(message)
                file.writeToFile("Message Received from CLIENT: '" + message + "'")
                result = execute.executeCommand(message)
                file.writeToFile("Response from EXECUTOR: '" + message + "'")
                await websocket.send(result)
            except Exception as e:
                file.writeToFile(traceback.format_exc())
                traceback.print_exc()
                system.exit(-1)
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        connected_clients.remove(websocket)

async def main():
    server = await websockets.serve(handle_client, 'localhost', 12345)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
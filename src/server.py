import asyncio
import websockets
import traceback
import threading
import sys

from Executor import Executor
from Interpreter import Interpreter
from Autocorrect import Autocorrect
from Utilities.FileLogger import FileLogger
from Utilities.DownloadModel import ModelDownloader
from UserInterface import UserInterface


connected_clients = set()

def create_handler(execute, interpret, autocorrect, file):
    """Factory function to create a WebSocket handler with dependencies"""
    async def handle_client(websocket):
        connected_clients.add(websocket)
        try:
            print(websocket)
            async for message in websocket:
                try:
                    if isinstance(message, bytes):
                        file.writeToFile("Audio Message received from CLIENT: 'PARSING'")
                        message = interpret.parseSpeech(message)
                    file.writeToFile("Message Received from CLIENT: '" + message + "'")
                    
                    # Apply autocorrect to the message
                    correctedMessage = autocorrect.correctCommand(message)
                    print(correctedMessage)
                    file.writeToFile("Autocorrected Message: '" + correctedMessage['command'] + "'")
                    
                    result = execute.executeCommand(correctedMessage)
                    file.writeToFile("Response from EXECUTOR: '" + result + "'")
                    await websocket.send(result)
                except Exception as e:
                    file.writeToFile(traceback.format_exc())
                    traceback.print_exc()
                    sys.exit(-1)
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            connected_clients.remove(websocket)
    
    return handle_client

async def main(execute, interpret, autocorrect, file):
    """Run the WebSocket server with provided dependencies"""
    handle_client = create_handler(execute, interpret, autocorrect, file)
    server = await websockets.serve(handle_client, 'localhost', 12345)
    print("WebSocket server started on localhost:12345")
    await server.wait_closed()

def start_server(execute, interpret, autocorrect, file):
    """Run the WebSocket server in a background thread"""
    asyncio.run(main(execute, interpret, autocorrect, file))

if __name__ == "__main__":
    # Initialize all application components
    file = FileLogger()
    file.setupLogging()
    
    modelDownloader = ModelDownloader()
    voskSuccess, llmSuccess = modelDownloader.setupAllModels()
    
    execute = Executor()
    interpret = Interpreter()
    autocorrect = Autocorrect()
    
    # Start WebSocket server in background thread
    server_thread = threading.Thread(
        target=start_server, 
        args=(execute, interpret, autocorrect, file),
        daemon=True
    )
    server_thread.start()
    
    # Create and start UI in main thread
    ui = UserInterface(
        executor=execute,
        interpreter=interpret,
        autocorrect=autocorrect,
        file_logger=file,
        app_registry=autocorrect.appRegistry
    )
    ui.run()
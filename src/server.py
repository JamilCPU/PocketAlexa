import asyncio
import websockets

from Executor import Executor
from FileLogger import FileLogger

connected_clients = set()

file = FileLogger()
try:
    file.setupLogging()
except FileExistsError:
    pass

async def handle_client(websocket):
    execute = Executor()


    connected_clients.add(websocket)
    try:
        print(websocket)
        async for message in websocket:
            file.writeToFile("Message Received: " + message)

            try:
                result = execute.executeCommand(message)
                print(result)
                await websocket.send(result)
                print('result: ', result)
            except Exception as e:
                #file.writeToFile(traceback.format_exc())
                traceback.print_exc()
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        # Remove the client from the set of connected clients
        connected_clients.remove(websocket)

# Main function to start the WebSocket server
async def main():
    server = await websockets.serve(handle_client, 'localhost', 12345)
    await server.wait_closed()

# Run the server
if __name__ == "__main__":
    asyncio.run(main())
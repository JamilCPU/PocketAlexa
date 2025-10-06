import asyncio
import websockets

from Executor import Executor
from FileLogger import FileLogger

connected_clients = set()

async def handle_client(websocket):
    execute = Executor()
    file = FileLogger()
    try:
        file.setupLogging()
    except FileExistsError:
        pass

    # Add the new client to the set of connected clients
    connected_clients.add(websocket)
    try:
        print(websocket)
        async for message in websocket:
            # Broadcast the message to all other connected clients
            file.writeToFile("Message Received: " + message)
            execute.executeCommand(message)
    except websockets.exceptions.ConnectionClosed:
        pass
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
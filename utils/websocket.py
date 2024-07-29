import threading
import websockets
import asyncio
import traceback

class WebSocket:

    def __init__(self, ip, port):
        self.websocket_thread = threading.Thread(target=self.threadStartWebsocketServer, daemon=True)
        self.message = None
        self.ip = ip
        self.port = port
        self.client_websockets = []

        self.ping_interval = 20
        self.ping_timeout = 10

        self.stop_event = threading.Event()

    def startWebSocket(self):
        try:
            self.websocket_thread.start()
            while self.websocket_thread.is_alive():
                self.websocket_thread.join(timeout=1)
        except KeyboardInterrupt:
            print("[INFO][Class: WebSocket - startWebSocket] Caught KeyboardInterrupt, shutting down...")
            self.stop_event.set()
            self.websocket_thread.join()
        except Exception as e:
            print(f"[ERROR][Class: WebSocket - startWebSocket]: {e}")
            traceback.print_exc()

    def getOutputMessageClient(self):
        try:
            return self.message
        except Exception as e:
            print(f"[ERROR][Class: WebSocket - getOutputMessageClient]: {e}")
            traceback.print_exc()

    async def handleWebsocketConnection(self, websocket, path):
        
        print(f"[INFO][Class: WebSocket - handleWebsocketConnection] - Client connecting from: {websocket.remote_address}")
        
        identifier = {
            'remote_address': websocket.remote_address,
            'websocket': websocket
        }

        self.client_websockets.append(identifier)

        try:
            while True:

                try:
                    pong_waiter = await websocket.ping()
                    await asyncio.wait_for(pong_waiter, timeout=self.ping_timeout)


                    while True:
                        message = await websocket.recv()

                        print(message)

                    # async for message in websocket:
                    #     self.message = message
                except Exception as e:
                    print(f"[ERROR][Class: WebSocket - handleWebsocketConnection]: {e}")
                    traceback.print_exc()

                await asyncio.sleep(self.ping_interval)
 
        except Exception as e:
            print(f"[ERROR][Class: WebSocket - handleWebsocketConnection]: {e}")
            traceback.print_exc()
        finally:
            print(f"[INFO][Class: WebSocket - handleWebsocketConnection] - Connection closed from: {websocket.remote_address}")
            self.client_websockets.remove(identifier)


    async def sendMessageAsync(self, message, remote_address):
        if len(self.client_websockets) > 0:
            try:
                client_selected = None

                for client in self.client_websockets:
                    if client['remote_address'][0] == remote_address[0]:
                        client_selected = client
                if client_selected:
                    await client_selected['websocket'].send(message)
            except Exception as e:
                print(f"[ERROR][Class: WebSocket - sendMessageAsync]: {e}")
                traceback.print_exc()

    def sendMessageToClient(self, message, remote_address):
        try:
            # asyncio.run(self.sendMessageAsync(message, remote_address))

            self.sendMessageAsync(message, remote_address)
        except Exception as e:
            print(f"[ERROR][Class: WebSocket - sendMessageToClient]: {e}")
            traceback.print_exc()

    def threadStartWebsocketServer(self):
        try:
            asyncio.set_event_loop(asyncio.new_event_loop())
            start_server = websockets.serve(self.handleWebsocketConnection, self.ip, self.port,)

            asyncio.get_event_loop().run_until_complete(start_server)
            asyncio.get_event_loop().run_forever()
        except Exception as e:
            print(f"[ERROR][Class: WebSocket - threadStartWebsocketServer]: {e}")
            traceback.print_exc()
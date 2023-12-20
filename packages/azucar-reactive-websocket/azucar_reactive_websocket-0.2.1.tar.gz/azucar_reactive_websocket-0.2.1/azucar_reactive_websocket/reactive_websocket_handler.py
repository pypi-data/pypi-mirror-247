import asyncio
import websockets
import rx
from rx import operators as ops
from imagen_handler import ImageHandler

class ReactiveWebSocketHandler:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            print(f"Conectado a {self.uri}")
        except Exception as e:
            print(f"Error al conectar a {self.uri}: {e}")

    def create_observable(self):
        return rx.create(self._message_generator)

    async def _message_generator(self, observer, _):
        try:
            async for message in self.websocket:
                observer.on_next(message)
        except websockets.ConnectionClosed:
            observer.on_completed()
        except Exception as e:
            observer.on_error(e)

    def process_message(self, message):
        # Aquí puedes definir cómo procesar cada mensaje
        print(f"Mensaje recibido: {message}")

    async def send_message(self, message):
        await self.websocket.send(message)

    async def send_image(websocket, image_path):
        encoded_image = ImageHandler.encode_image_to_base64(image_path)
        await websocket.send(encoded_image)

    async def close(self):
        await self.websocket.close()

    def start_receiving_messages(self):
        messages_observable = self.create_observable()
        messages_observable.pipe(
            ops.do_action(self.process_message)
        ).subscribe(
            on_error=lambda e: print(f"Error: {e}"),
            on_completed=lambda: print("Conexión WebSocket cerrada.")
        )

    async def run(self):
        await self.connect()
        self.start_receiving_messages()

# Ejemplo de cómo usar la clase
uri = "ws://example.com/websocket"
handler = ReactiveWebSocketHandler(uri)

# Para iniciar la clase y conectarla
asyncio.get_event_loop().run_until_complete(handler.run())

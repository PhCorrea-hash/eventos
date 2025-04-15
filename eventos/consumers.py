import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EventoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # A lógica para quando o WebSocket for aberto
        self.room_name = 'eventos_room'
        self.room_group_name = 'eventos'

        # Adiciona o WebSocket ao grupo de eventos
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # A lógica para quando o WebSocket for fechado
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Lógica para receber dados (se necessário)
        pass

    # Envia a atualização do evento para o WebSocket
    async def send_event_update(self, event_data):
        await self.send(text_data=json.dumps(event_data))

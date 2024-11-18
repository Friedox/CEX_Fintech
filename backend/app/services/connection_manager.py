from typing import List, Dict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.activity_status: Dict[str, Dict[str, bool]] = {}  # Optional for dynamic statuses

    async def connect(self, token_pair: str, websocket: WebSocket):
        await websocket.accept()
        if token_pair not in self.active_connections:
            self.active_connections[token_pair] = []
            self.activity_status[token_pair] = {}  # Optional
        self.active_connections[token_pair].append(websocket)
        print(f"[INFO] Connection established for {token_pair}. Total: {len(self.active_connections[token_pair])}")

    def disconnect(self, token_pair: str, websocket: WebSocket):
        if token_pair in self.active_connections:
            self.active_connections[token_pair].remove(websocket)
            if not self.active_connections[token_pair]:
                del self.active_connections[token_pair]
                del self.activity_status[token_pair]  # Optional cleanup
            print(f"[INFO] Connection closed for {token_pair}. Remaining: {len(self.active_connections.get(token_pair, []))}")

    async def broadcast(self, token_pair: str, message: dict):
        if token_pair in self.active_connections:
            print(f"[INFO] Broadcasting message to {len(self.active_connections[token_pair])} connections for {token_pair}")
            for connection in self.active_connections[token_pair]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"[ERROR] Failed to send message for {token_pair}: {e}")

    async def update_status(self, token_pair: str, user_id: str, is_active: bool):
        if token_pair not in self.activity_status:
            self.activity_status[token_pair] = {}
        self.activity_status[token_pair][user_id] = is_active
        status_message = f"User {user_id} {'active' if is_active else 'inactive'} in {token_pair}."
        await self.broadcast(token_pair, {"type": "status_update", "message": status_message})


manager = ConnectionManager()

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubscriptionKeys(BaseModel):
    p256dh: str
    auth: str

class PushSubscriptionCreate(BaseModel):
    endpoint: str
    keys: SubscriptionKeys
    account: Optional[str] = None
    user_email: Optional[str] = None

class PushSubscriptionResponse(BaseModel):
    id: int
    endpoint: str
    account: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class VapidPublicKeyResponse(BaseModel):
    public_key: str

class NotificationTestRequest(BaseModel):
    title: Optional[str] = "🔔 Teste de Notificação MiteScan"
    body: Optional[str] = "Notificações na área de trabalho funcionando com sucesso!"
    account: Optional[str] = None

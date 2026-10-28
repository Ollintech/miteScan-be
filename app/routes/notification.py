from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from db.database import get_db
from models.push_subscription import PushSubscription
from schemas.notification import (
    PushSubscriptionCreate,
    PushSubscriptionResponse,
    VapidPublicKeyResponse,
    NotificationTestRequest
)
from core.config import settings
from services.notification_service import (
    send_notification_to_subscription,
    send_notification_to_account
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/vapid-public-key", response_model=VapidPublicKeyResponse)
def get_vapid_public_key():
    """
    Retorna a chave pública VAPID para que o frontend/navegador
    possa se inscrever no serviço de Push do sistema operacional.
    """
    if not settings.vapid_public_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chave VAPID pública não configurada no servidor."
        )
    return {"public_key": settings.vapid_public_key}

@router.post("/subscribe", response_model=PushSubscriptionResponse)
def subscribe_device(subscription_data: PushSubscriptionCreate, db: Session = Depends(get_db)):
    """
    Registra ou atualiza a inscrição Push de um computador/navegador.
    """
    existing_sub = db.query(PushSubscription).filter(
        PushSubscription.endpoint == subscription_data.endpoint
    ).first()

    if existing_sub:
        existing_sub.p256dh = subscription_data.keys.p256dh
        existing_sub.auth = subscription_data.keys.auth
        if subscription_data.account:
            existing_sub.account = subscription_data.account
        if subscription_data.user_email:
            existing_sub.user_email = subscription_data.user_email
        db.commit()
        db.refresh(existing_sub)
        return existing_sub

    new_sub = PushSubscription(
        account=subscription_data.account,
        user_email=subscription_data.user_email,
        endpoint=subscription_data.endpoint,
        p256dh=subscription_data.keys.p256dh,
        auth=subscription_data.keys.auth
    )

    try:
        db.add(new_sub)
        db.commit()
        db.refresh(new_sub)
        return new_sub
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar inscrição Push: {str(e)}"
        )

@router.post("/unsubscribe")
def unsubscribe_device(endpoint_data: dict, db: Session = Depends(get_db)):
    """
    Remove uma inscrição Push existente (quando o usuário desativa notificações).
    """
    endpoint = endpoint_data.get("endpoint")
    if not endpoint:
        raise HTTPException(status_code=400, detail="Endpoint é obrigatório.")

    sub = db.query(PushSubscription).filter(PushSubscription.endpoint == endpoint).first()
    if sub:
        db.delete(sub)
        db.commit()
        return {"detail": "Inscrição removida com sucesso."}

    return {"detail": "Inscrição não encontrada ou já removida."}

@router.post("/test")
def send_test_notification(payload: NotificationTestRequest, db: Session = Depends(get_db)):
    """
    Dispara uma notificação de teste diretamente para o computador.
    """
    notification_data = {
        "title": payload.title or "🔔 Teste de Notificação MiteScan",
        "body": payload.body or "Notificação no computador funcionando perfeitamente!",
        "icon": "/logo-mitescan.png",
        "badge": "/logo-mitescan.png",
        "tag": "test-notification",
        "data": {
            "url": "/home"
        }
    }

    sent = send_notification_to_account(account=payload.account, payload=notification_data, db=db)
    return {
        "message": f"Notificação de teste enviada para {sent} dispositivo(s).",
        "sent_count": sent
    }

@router.get("/thresholds")
def get_alert_thresholds():
    """
    Retorna os limites configurados para alerta de temperatura e umidade.
    """
    return {
        "temp_min": settings.temp_min_alert,
        "temp_max": settings.temp_max_alert,
        "humidity_min": settings.humidity_min_alert,
        "humidity_max": settings.humidity_max_alert
    }

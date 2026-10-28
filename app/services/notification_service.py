import json
import logging
import time
from typing import Optional, Dict
from sqlalchemy.orm import Session
from core.config import settings
from models.push_subscription import PushSubscription
from models.hive import Hive

logger = logging.getLogger(__name__)

try:
    from pywebpush import webpush, WebPushException
    HAS_PYWEBPUSH = True
except ImportError:
    webpush = None
    WebPushException = Exception
    HAS_PYWEBPUSH = False
    logger.warning("⚠️ Biblioteca 'pywebpush' não encontrada neste ambiente Python. Execute 'pip install pywebpush' para habilitar notificações push.")

def send_notification_to_subscription(subscription: PushSubscription, payload: dict, db: Optional[Session] = None) -> bool:
    """Envia uma notificação Web Push para uma inscrição específica."""
    if not HAS_PYWEBPUSH:
        logger.warning("pywebpush não está instalado neste interpretador Python. Notificação push ignorada.")
        return False

    if not settings.vapid_private_key or not settings.vapid_public_key:
        logger.warning("VAPID keys não configuradas. Notificação push ignorada.")
        return False

    subscription_info = {
        "endpoint": subscription.endpoint,
        "keys": {
            "p256dh": subscription.p256dh,
            "auth": subscription.auth
        }
    }

    vapid_claims = {
        "sub": settings.vapid_claims_email
    }

    try:
        response = webpush(
            subscription_info=subscription_info,
            data=json.dumps(payload),
            vapid_private_key=settings.vapid_private_key,
            vapid_claims=vapid_claims
        )
        logger.info(f"✅ Web Push enviado com sucesso para endpoint: {subscription.endpoint[:40]}... Status: {response.status_code}")
        return True
    except WebPushException as ex:
        logger.error(f"❌ Falha ao enviar Web Push: {ex}")
        # Se a inscrição expirou (410 Gone ou 404 Not Found), removemos do banco
        if ex.response and ex.response.status_code in (404, 410):
            if db:
                try:
                    logger.info(f"Removendo inscrição expirada do banco: {subscription.id}")
                    db.delete(subscription)
                    db.commit()
                except Exception as db_err:
                    logger.error(f"Erro ao remover inscrição expirada: {db_err}")
        return False
    except Exception as e:
        logger.error(f"❌ Erro inesperado ao enviar Web Push: {e}", exc_info=True)
        return False

def send_notification_to_account(account: Optional[str], payload: dict, db: Session) -> int:
    """Envia uma notificação Web Push para todos os computadores/navegadores inscritos na conta."""
    query = db.query(PushSubscription)
    if account:
        # Busca assinaturas da conta ou assinaturas globais sem conta definida
        query = query.filter((PushSubscription.account == account) | (PushSubscription.account.is_(None)))

    subscriptions = query.all()
    if not subscriptions:
        logger.info(f"Nenhum computador/dispositivo inscrito para a conta '{account}'.")
        return 0

    sent_count = 0
    for sub in subscriptions:
        if send_notification_to_subscription(sub, payload, db=db):
            sent_count += 1

    return sent_count

def check_sensor_and_alert(hive: Hive, temperature: Optional[float], humidity: Optional[float], db: Session) -> Optional[dict]:
    """
    Verifica se a temperatura ou a umidade estão fora dos limites aceitáveis.
    Se estiverem anormais e fora do tempo de cooldown, dispara notificação Web Push.
    """
    if temperature is None and humidity is None:
        return None

    alerts = []
    
    # Validação de Temperatura
    if temperature is not None:
        if temperature > settings.temp_max_alert:
            alerts.append(f"🔥 Temperatura ALTA: {temperature:.1f}°C (Máx ideal: {settings.temp_max_alert}°C)")
        elif temperature < settings.temp_min_alert:
            alerts.append(f"❄️ Temperatura BAIXA: {temperature:.1f}°C (Mín ideal: {settings.temp_min_alert}°C)")

    # Validação de Umidade
    if humidity is not None:
        if humidity > settings.humidity_max_alert:
            alerts.append(f"💧 Umidade ALTA: {humidity:.1f}% (Máx ideal: {settings.humidity_max_alert}%)")
        elif humidity < settings.humidity_min_alert:
            alerts.append(f"🌵 Umidade BAIXA: {humidity:.1f}% (Mín ideal: {settings.humidity_min_alert}%)")

    if not alerts:
        return None  # Tudo normal!

    payload = {
        "title": f"⚠️ Alerta na Colmeia: {hive.name}",
        "body": " | ".join(alerts),
        "icon": "/logo-mitescan.png",
        "badge": "/logo-mitescan.png",
        "tag": f"hive-alert-{hive.id}",
        "data": {
            "hive_id": hive.id,
            "hive_name": hive.name,
            "temperature": temperature,
            "humidity": humidity,
            "url": f"/hives"
        }
    }

    logger.warning(f"🚨 DISPARANDO ALERTA WEB PUSH: {payload['title']} -> {payload['body']}")
    send_notification_to_account(hive.account, payload, db=db)
    return payload

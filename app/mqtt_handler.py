import asyncio
import json
import requests
import logging
import os, multiprocessing
import paho.mqtt.client as mqtt
from core.config import settings

MQTT_BROKER = settings.mqtt_broker
MQTT_PORT = settings.mqtt_port
MQTT_TOPIC_SUBSCRIBE = "colmeia/+"
API_URL = settings.api_sensor_url

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback para quando o cliente se conecta ao broker."""
    if rc == 0:
        logger.info("✅ Conectado ao broker MQTT com sucesso.")
        client.subscribe(MQTT_TOPIC_SUBSCRIBE)
        logger.info(f"   -> Inscrito no tópico: {MQTT_TOPIC_SUBSCRIBE}")
    else:
        logger.error(f"❌ Falha ao conectar ao broker MQTT. Código: {rc}")

def on_message(client, userdata, msg):
    """Callback para quando uma mensagem é recebida."""
    logger.info(f"📩 Mensagem recebida no tópico: {msg.topic}")
    try:
        data = json.loads(msg.payload.decode())

        topic_parts = msg.topic.split('/')
        if len(topic_parts) != 2 or topic_parts[0] != 'colmeia':
            logger.warning(f"  -> Tópico '{msg.topic}' fora do formato esperado 'colmeia/+'. Ignorando.")
            return

        account_name = data.get("conta_usuario")
        hive_name = data.get("nome_colmeia")
        
        api_payload = {
            "account_name": account_name,
            "hive_name": hive_name,
            "temperature": data.get("t"),
            "humidity": data.get("h")
        }
            
        logger.info(f"  -> Payload traduzido: {api_payload}")
        
        response = requests.post(API_URL, json=api_payload)
        response.raise_for_status() 
        logger.info(f"  -> ✅ Dados enviados para API com sucesso. Status: {response.status_code}")
        
    except json.JSONDecodeError:
        logger.error(f"  -> ❌ Erro ao decodificar JSON. Payload recebido: {msg.payload.decode()}", exc_info=True)
    except Exception as e:
        logger.error(f"  -> ❌ Erro ao processar mensagem ou enviar para API: {e}", exc_info=True)
        
def start_mqtt():
    """Inicializa e executa o loop do cliente MQTT."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        logger.info(f"🔌 Conectando ao broker MQTT em {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever() 
    except KeyboardInterrupt:
        logger.info("🛑 Cliente MQTT recebendo sinal de desligamento...")
        client.disconnect()
    except Exception as e:
        logger.critical(f"CRÍTICO: Não foi possível conectar ao broker MQTT. Verifique o endereço e a rede. Erro: {e}", exc_info=True)

async def run_mqtt_in_background():
    process = multiprocessing.Process(target=start_mqtt)
    process.start()
    await asyncio.sleep(1)

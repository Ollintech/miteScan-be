import asyncio
import json
import requests
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
API_URL = os.getenv("API_SENSOR_URL")

def on_connect(client, userdata, flags, rc):
    print("✅ Conectado ao MQTT com código:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        response = requests.post(API_URL, json=data)
        print("📤 Enviado para API. Código:", response.status_code)
    except Exception as e:
        print("❌ Erro ao enviar para API:", e)

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

async def run_mqtt_in_background():
    start_mqtt()
    await asyncio.sleep(0) 


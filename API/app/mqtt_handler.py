import asyncio
import json
import requests
import paho.mqtt.client as mqtt
import os, multiprocessing
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

    try:
        print(f"🔌 Conectando ao broker {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()  # Use loop_forever instead of loop_start for better control
    except Exception as e:
        print(f"❌ Falha ao conectar ao broker MQTT: {e}")

async def run_mqtt_in_background():
    # Run MQTT in a separate thread to avoid blocking
    import threading
    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()
    await asyncio.sleep(0)  # Yield control to allow other tasks to run
    # Run in a separate process to avoid conflicts
    process = multiprocessing.Process(target=start_mqtt)
    process.start()
    await asyncio.sleep(0) 


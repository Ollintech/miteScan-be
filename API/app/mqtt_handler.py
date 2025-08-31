import json
import requests
import paho.mqtt.client as mqtt
import os
import threading
import time
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "mitescan/sensors")
API_URL = os.getenv("API_SENSOR_URL", "http://localhost:8000/sensors/data")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado ao MQTT broker com sucesso!")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Inscrito no tópico: {MQTT_TOPIC}")
    else:
        print(f"❌ Falha na conexão MQTT. Código: {rc}")

def on_message(client, userdata, msg):
    try:
        # Decode message payload
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        
        print(f"📨 Mensagem MQTT recebida no tópico {msg.topic}: {data}")
        
        # Send data to Flask API
        response = requests.post(API_URL, json=data, timeout=10)
        
        if response.status_code == 201:
            print(f"✅ Dados enviados para API com sucesso. Sensor ID: {response.json().get('sensor_id')}")
        else:
            print(f"⚠️ API retornou código {response.status_code}: {response.text}")
            
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {e}")
        print(f"Payload recebido: {msg.payload}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar dados para API: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado ao processar mensagem MQTT: {e}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("⚠️ Desconectado do MQTT broker inesperadamente")
    else:
        print("📴 Desconectado do MQTT broker")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"✅ Inscrição confirmada. QoS: {granted_qos}")

def create_mqtt_client():
    """Cria e configura o cliente MQTT"""
    client = mqtt.Client()
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    
    # Configure connection options
    client.reconnect_delay_set(min_delay=1, max_delay=120)
    
    return client

def start_mqtt_client():
    """Inicia o cliente MQTT com reconexão automática"""
    client = create_mqtt_client()
    
    while True:
        try:
            print(f"🔌 Tentando conectar ao broker MQTT {MQTT_BROKER}:{MQTT_PORT}...")
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            
            # Start the loop
            client.loop_forever()
            
        except Exception as e:
            print(f"❌ Erro na conexão MQTT: {e}")
            print("🔄 Tentando reconectar em 10 segundos...")
            time.sleep(10)

def start_mqtt_thread():
    """Inicia o MQTT em uma thread separada"""
    print("🚀 Iniciando serviço MQTT em thread separada...")
    
    # Verify configuration
    if not MQTT_BROKER:
        print("⚠️ MQTT_BROKER não configurado. Serviço MQTT não será iniciado.")
        return
    
    if not API_URL:
        print("⚠️ API_SENSOR_URL não configurado. Serviço MQTT não será iniciado.")
        return
    
    print(f"📋 Configuração MQTT:")
    print(f"   Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"   Tópico: {MQTT_TOPIC}")
    print(f"   API URL: {API_URL}")
    
    try:
        start_mqtt_client()
    except KeyboardInterrupt:
        print("🛑 Serviço MQTT interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro fatal no serviço MQTT: {e}")

def publish_test_message():
    """Função para testar o envio de mensagens MQTT"""
    client = create_mqtt_client()
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        test_data = {
            "hive_id": 1,
            "temperature": 25.5,
            "humidity": 60.2,
            "sensor_type": "DHT22",
            "status": "active"
        }
        
        client.publish(MQTT_TOPIC, json.dumps(test_data))
        print(f"📤 Mensagem de teste enviada: {test_data}")
        
        client.disconnect()
        
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem de teste: {e}")

if __name__ == "__main__":
    # Para testar o MQTT handler diretamente
    print("🧪 Modo de teste - enviando mensagem de teste...")
    publish_test_message()
    
    print("🔄 Iniciando cliente MQTT...")
    start_mqtt_thread()
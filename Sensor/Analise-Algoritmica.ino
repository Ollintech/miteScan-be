// http://arduino.esp8266.com/stable/package_esp8266com_index.json

#include <ESP8266WiFi.h>
#include <WiFiManager.h>
#include <PubSubClient.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11
#define COLMEIA_ID 1

const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "colmeia/1/dados";

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

unsigned long lastSend = 0;
const long interval = 1800; // 3 minutos

void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT...");
    if (client.connect("ESP8266ClientColmeia1")) {
      Serial.println("conectado.");
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(client.state());
      delay(60000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFiManager wifiManager;
  wifiManager.autoConnect("MiteScanSetup");
  Serial.println("Wi-Fi conectado!");

  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastSend > interval) {
    lastSend = now;

    unsigned long startTime = micros();

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      Serial.println("Erro ao ler sensor.");
      return;
    }

    String payload = "{\"colmeia_id\":" + String(COLMEIA_ID) +
                     ",\"temperature\":" + String(t, 1) +
                     ",\"humidity\":" + String(h, 1) + "}";
    
    unsigned long sensorTime = micros() - startTime;
    Serial.print("Tempo de leitura do sensor (us): ");
    Serial.println(sensorTime);

    startTime = micros();
    client.publish(mqtt_topic, payload.c_str());
    unsigned long mqttTime = micros() - startTime;
    Serial.print("Tempo envio MQTT (us): ");
    Serial.println(mqttTime);

    float activeCurrent_mA = 100.0; // estimativa média
    float voltage = 3.3; // tensão comum
    float activeTime_s = (sensorTime + mqttTime) / 1000000.0;
    float energy_mWh = (activeCurrent_mA * voltage * activeTime_s) / 3600.0;

    Serial.print("Energia estimada (mWh): ");
    Serial.println(energy_mWh, 6);

    
  }

  Serial.print("Memória livre (bytes): ");
  Serial.println(ESP.getFreeHeap());

}

// // Saídas:
// Tempo envio MQTT (us): 1105
// Energia estimada (mWh): 0.000169
// Tempo de leitura do sensor (us): 25545
// Tempo envio MQTT (us): 926
// Energia estimada (mWh): 0.002427
// Tempo de leitura do sensor (us): 736
// Tempo envio MQTT (us): 773
// Energia estimada (mWh): 0.000138
// Tempo de leitura do sensor (us): 25628
// Tempo envio MQTT (us): 950
// Energia estimada (mWh): 0.002436
// Tempo de leitura do sensor (us): 740
// Tempo envio MQTT (us): 1089
// Energia estimada (mWh): 0.000168

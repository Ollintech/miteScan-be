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

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      Serial.println("Erro ao ler sensor.");
      return;
    }

    String payload = "{\"colmeia_id\":" + String(COLMEIA_ID) +
                     ",\"temperature\":" + String(t, 1) +
                     ",\"humidity\":" + String(h, 1) + "}";

    client.publish(mqtt_topic, payload.c_str());
    Serial.println("Dados enviados via MQTT:");
    Serial.println(payload);
  }
}
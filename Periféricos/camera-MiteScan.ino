// Na arduino IDE, acessa "Tools" -> "board" -> "board manager", pesquisa e instala a board "esp32" do expressif. Depois que instalou, acessa "Files" -> "Examples" -> "ESP32" -> "Camera" -> "CameraWebServer", isso vai gerar os arquivos com os códigos da camera.

// Depois que gerou o arquivo, comenta a linha: 
// #define CAMERA_MODEL_ESP_EYE  // Has PSRAM

// e descomenta a linha:
// #define CAMERA_MODEL_AI_THINKER // Has PSRAM

// Altere os "*" para as informações corretas do seu wifi:
// const char *ssid = "**********";
// const char *password = "**********";

// Certifique-se de que o seu computador está conectado na mesma rede que a camera
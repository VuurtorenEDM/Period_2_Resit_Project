#include <Arduino.h>
#include <Adafruit_Sensor.h>
// #include <DHT.h>
// #include <DHT_U.h>
#include <Math.h>
#include <Wire.h>
// WIFI
#include <WiFiS3.h>
#include <WiFiSSLClient.h>

#define TEMP A0 // LM35 pin

// DHT dht(dhtPin, DHT11);    

int hum;
float outsideTemp; 
// insideTemp,

//WIFI
const char ssid[] = "fambergies";  // change your network SSID (name) iotroam ppp
const char pass[] = "Safe@bergies";   // change your network password (use for WPA, or use as key for WEP) dPwcM9DNRY pppppppp

WiFiSSLClient client;

const int port = 443; // HTTPS port
const char HOST_NAME[] = "period-2-resit-project.onrender.com"; // Your server hostname
String HTTP_METHOD = "POST";
String PATH_NAME = "/add";

// Functions
// void readDHT();
void LM35read();
void connectServer();
void sendToServer(String data);
void processData();

void setup() 
{
  Serial.begin(9600);
  // dht.begin();
  // Switch to Internal 1.1V Reference
  analogReference(AR_INTERNAL);

  // //WIFI
  connectServer();
}

void loop() {
  processData();
  delay(2000);
  // readDHT();
  LM35read();
}

void processData(){
  long lastCheckTime = 0;
  int updateInterval = 3000;
  if(millis() - lastCheckTime > updateInterval){
    // readDHT();
    LM35read();
    Serial.println(outsideTemp);
    // Serial.println(insideTemp);
    Serial.println(hum);
    String data = "{  \"id\": 12345,  \"temperature\": 22.5,  \"timestamp\": \"2025-01-31T14:30:00Z\"}";
    sendToServer(data);
    Serial.println("Sent data");
  }
  lastCheckTime = millis();
}

//Reads the DHT11 sensor
// void readDHT(){
//   int testHum = dht.readHumidity();   //rads data from sensor
//   double testInsideTemp = dht.readTemperature() - 2.0;
//   if(!isnan(testHum) && !isnan(testInsideTemp)){  //isnan checks if is not a number(error code for dht is not a number)
//     //valid readings
//     hum = testHum;
//     insideTemp = testInsideTemp;
//   }else{
//     Serial.println("Error");
//   }
//   Serial.println(testHum);
//   Serial.println(testInsideTemp);
// }

void LM35read() 
{
  // read the input on analog pin 0:
  outsideTemp = analogRead(TEMP);
  if (outsideTemp == 0){
    return;
  }
  //Calculate Temperature from TEMP value
  //Note that we use mV for Vref
  //Vin = TEMPresult*Vref/(2^10)
  //Temp(C) = Vin/(10) = TEMPresult*Vref/(1200*10) + 2 
  outsideTemp = outsideTemp*1100/(1200*10.0) + 2.0;
  Serial.println(outsideTemp);
  delay(4000);
}

void connectServer() {
  // Check for WiFi module
  if (WiFi.status() == WL_NO_MODULE) 
  {
    Serial.println("Communication with WiFi module failed!");
    while (true);
  }

  // Connect to WiFi
  Serial.print("Attempting to connect to SSID: ");
  Serial.println(ssid);
  while (WiFi.status() != WL_CONNECTED) 
  {
    WiFi.begin(ssid, pass);
    delay(5000); // Retry every 5 seconds
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void sendToServer(String data) 
{
  // Securely connect to the server
  if (!client.connect(HOST_NAME, port)) 
  {
    Serial.println("Connection to server failed!");
    return;
  }

  // Build HTTPS POST request
  client.println("POST " + String(PATH_NAME) + " HTTP/1.1");
  client.println("Host: " + String(HOST_NAME));
  client.println("Content-Type: application/json"); // Specify JSON format
  client.println("Connection: close");
  client.println("Content-Length: " + String(data.length())); // Specify the body length
  client.println(); // End of headers
  client.println(data); // Send JSON data

  // Read response from server
  while (client.connected()) 
  {
    if (client.available()) 
    {
      // Serial.println("Test Server Response");
      String response = client.readStringUntil('\n');
      Serial.println(response);
    }
  }

  client.stop(); // Close the connection
}
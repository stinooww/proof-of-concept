
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>

const char* ssid     = "TODO";
const char* password = "TODO

const char* host = "api.pushbullet.com";
//https://api.pushbullet.com/v2/pushes
const int httpsPort = 443;

const char* accessToken = "TODO";
const char* fingerprint = "TODO";

void setup() {
  Serial.begin(115200);
  delay(10);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Use WiFiClientSecure class to create TLS connection
  WiFiClientSecure client;
  Serial.print("connecting to ");
  Serial.println(host);
  if (!client.connect(host, httpsPort)) {
    Serial.println("connection failed");
    return;
  }

  if (client.verify(fingerprint, host)) {
    Serial.println("certificate matches");
  } else {
    Serial.println("certificate doesn't match");
  }

  String url = "/v2/pushes";
  Serial.print("requesting URL: "); Serial.println(url);

  client.print(String("POST ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "User-Agent: ESP8266\r\n" +
               "Access-Token: " + accessToken + "\r\n" +
               "Content-length: 114\r\n"
               "Content-Type: application/json\r\n" +
               "Connection: close\r\n\r\n" +
               "{\"body\":\"Space Elevator, Mars Hyperloop, Space Model S (Model Space?)\",\"title\":\"Space Travel Ideas\",\"type\":\"note\"}"
              );


  Serial.println("request sent");
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") {
      Serial.println("headers received");
      break;
    }
  }
  String line = client.readStringUntil('\n');
  //  String line = client.readString(); // this line is good for debugging error messages more then a single line
  if (line.startsWith("{\"active\":true")) {
    Serial.println("esp8266/Arduino CI successfull!");
  } else {
    Serial.println("esp8266/Arduino CI has failed");
  }
  Serial.println("reply was:");
  Serial.println("==========");
  Serial.println(line);
  Serial.println("==========");
  Serial.println("closing connection");
}



void loop() {
  // put your main code here, to run repeatedly:

}

#include <ArduinoWebsockets.h>
#include <WiFi.h>

#include <iostream>
#include <cstdio>
#include <string>
#include <sstream>

const char* ssid = "HostspotSocketIOIMUBNO055"; //Enter SSID
const char* password = "7aecf2d1f18296861f73d63ccb2e1bbb"; //Enter Password
const char* websockets_server_host = "192.168.137.1"; //Enter server adress
const uint16_t websockets_server_port = 5000; // Enter server port

using namespace websockets;

WebsocketsClient client;

int sum = 0;

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  for(int i = 0; i < 10 && WiFi.status() != WL_CONNECTED; i++) {
    Serial.print(".");
    delay(1000);
  }

  if(WiFi.status() != WL_CONNECTED) {
    Serial.println("No Wifi!");
    return;
  }

  client.onMessage(onMessageCallback);
  client.onEvent(onEventsCallback);

  Serial.println("Connected to Wifi, Connecting to server.");
  bool connected = client.connect(websockets_server_host, websockets_server_port, "/");

  if(connected) {
    Serial.println("Connected!");
  } else {
    Serial.println("Not Connected!");
  }
}

void loop() {
    
  if(client.available()) {
    client.poll();
  }

  sum = sum + 1;

  std::string concatenated = std::to_string(sum);

  const char* char_array = concatenated.c_str();

  client.send(char_array);
}

void onMessageCallback(WebsocketsMessage message) {
  Serial.print("Received message: ");
  Serial.println(message.data());
}

void onEventsCallback(WebsocketsEvent event, String data) {
  if (event == WebsocketsEvent::ConnectionOpened) {
    Serial.println("Connection Opened");
  } else if (event == WebsocketsEvent::ConnectionClosed) {
    Serial.println("Connection Closed");
  } else if (event == WebsocketsEvent::GotPing) {
    Serial.println("Got a Ping!");
  } else if (event == WebsocketsEvent::GotPong) {
    Serial.println("Got a Pong!");
  }
}
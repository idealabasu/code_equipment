#include "AD7147.h"
#include <SPI.h>

#define CS  10
#define INTERRUPT 11

AD7147 slider = AD7147();

void setup() {
  Serial.begin(115200);
  SPI.begin();
  while (!Serial);
  Serial.println("AD7147 demo");
  if (!slider.begin(CS, INTERRUPT)) {
    Serial.println("could not communicate with device!!");
    while (1);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  //  if(slider.update()){
  Serial.print("Device id:");
  Serial.println(slider.getDeviceID());
  Serial.print("all sensor:");
  Serial.println(slider.readAllSensors1());
  Serial.print("sider posotion:");
  Serial.println(slider.calculateSiderPosition());
  Serial.print("check status:");
  Serial.println(slider.checkStatus());

  delay(1000);  
}

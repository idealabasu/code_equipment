#include <Wire.h>
#include "si7210.h"




void setup() {
  Serial.begin(9600); // Initialisation Terminal Série
  Wire.begin(); // Initialisation I2C

//  Wire.beginTransmission(0x31);

}

void loop() {
  // put your main code here, to run repeatedly:
//  Wire.beginTransmission(0x31);
//  Wire.write(0xC0);
//  Wire.endTransmission(false);
//  Wire.requestFrom(0x31,1);
//  byte val = Wire.read();
//  Serial.println(val,HEX);
//  Wire.endTransmission(true);

  Wire.beginTransmission(0x31);
  Wire.write(0xC4);
  Wire.write(0x04);
  Wire.endTransmission(true);

  Wire.beginTransmission(0x31);
  Wire.write(0xC1);
  Wire.endTransmission(false);
  Wire.requestFrom(0x31,1);
  byte Dspsigm = Wire.read();
  Wire.endTransmission(true);

  Wire.beginTransmission(0x31);
  Wire.write(0xC2);
  Wire.endTransmission(false);
  Wire.requestFrom(0x31,1);
  byte Dspsigl = Wire.read();
  Wire.endTransmission(true);

  unsigned int rawData = (Dspsigm & 0b01111111)*256+Dspsigl;
  Serial.print(rawData,DEC);
  Serial.print(",");
  float magneticField = (d-16384)*0.00125;
  Serial.println(magneticField);

}

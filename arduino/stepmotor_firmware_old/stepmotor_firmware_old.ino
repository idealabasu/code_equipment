int PUL = 7; //define Pulse pin
int DIR = 6; //define Direction pin
int ENA = 5; //define Enable Pin

int incomingByte = 0;

void setup() {
  pinMode (PUL, OUTPUT);
  pinMode (DIR, OUTPUT);
  pinMode (ENA, OUTPUT);
  Serial.begin(115200);

}

void loop() {

  if (Serial.available() > 0) {
    
    incomingByte = Serial.read();
    //    Serial.println(incomingByte-38,DEC);
    switch (incomingByte) {
      
      case '5': //CW     
        for (int i = 0; i < 16; i++) {
          digitalWrite(DIR, HIGH);
          digitalWrite(ENA, HIGH);
          digitalWrite(PUL, HIGH);
          delay(1);
          digitalWrite(PUL, LOW);
          delay(1);
        }
        Serial.println(5);
        break;
        
      case '7':
        //CCW
        for (int i = 0; i < 16; i++) {
          digitalWrite(DIR, LOW);
          digitalWrite(ENA, HIGH);
          digitalWrite(PUL, HIGH);
          delay(1);
          digitalWrite(PUL, LOW);
          delay(1);
        }
        Serial.println(7);
        break;
        
      case '3': //STOP
        Serial.println("3");
        digitalWrite(DIR, HIGH);
        digitalWrite(ENA, HIGH);
        break;
        
      case '4':
        Serial.println("4");
        digitalWrite(DIR, LOW);
        digitalWrite(ENA, LOW);
        break;
    }
  }

}

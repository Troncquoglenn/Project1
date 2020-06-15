const int ldrPin = A0;

int inputPin = 7;              
int pirState = LOW;             
int val = 0;

String motion = "niks";

void setup() {

Serial.begin(9600);

pinMode(ldrPin, INPUT);
pinMode(inputPin, INPUT);

}

void loop() {

int ldrStatus = analogRead(ldrPin);
val = digitalRead(inputPin); 
  if (val == HIGH) {            
    if (pirState == LOW) {
      motion = "beweging";
      pirState = HIGH;
    }
    
  } else {
    if (pirState == HIGH){
      motion = "niks";
      pirState = LOW;
    }
  }


Serial.println(motion + "-" + String(ldrStatus));

delay(1000);

}

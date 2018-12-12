unsigned long int responseTime = 0;
unsigned long int serialTimer = 0;
bool sens1_IsResponse = false, sens2_IsResponse=false;

void setup() {
  Serial.begin(115200);
  pinMode(14, INPUT);
  pinMode(12, INPUT);

}

void loop() {
  if (millis()-serialTimer > 2000){
    Serial.println("SS");
    serialTimer = millis();
  }
  int s1 = 0, s2 = 0;
  s1 = digitalRead(14);
  s2 = digitalRead(12);
  if(s1 == 0){
    if(sens2_IsResponse){
      sens2_IsResponse = false;
      if(millis() - responseTime > 10){
        Serial.print("T");
        Serial.println(millis() - responseTime);
      }
    } else if (!sens1_IsResponse) {
      responseTime = millis();
      sens1_IsResponse = true;
    }
  }
   if(s2 == 0){
    if(sens1_IsResponse){
      sens1_IsResponse = false;
      if(millis() - responseTime > 10){
        Serial.print("T");
        Serial.println(millis() - responseTime);
      }
    } else if (!sens2_IsResponse) {
      responseTime = millis();
      sens2_IsResponse = true;
    }
  }

  if(millis() - responseTime > 2*1000){
    sens1_IsResponse = false;
    sens2_IsResponse = false;
  }
}

unsigned long int responseTime = 0;
unsigned long int serialTimer = 0;
bool sens1_IsResponse = false, sens2_IsResponse=false;

void setup() {
  Serial.begin(115200);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);

}

void loop() {
  if (millis()-serialTimer > 2000){
    Serial.println("SS");
    serialTimer = millis();
  }
  int s1 = 0, s2 = 0;
  s1 = analogRead(A3);
  s2 = analogRead(A4);
  /*Serial.print(s1);
  Serial.print(" ");
  Serial.println(s2);*/
  if(s1 < 950){
    /*Serial.print("s1 ");
    Serial.println(s1);*/
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
   if(s2 < 950){
    /*Serial.print("s2 ");
    Serial.println(s2);*/
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

#include <Arduino.h>

int S1 = 8;
int S2 = 9;
String inputData = "";

void setup() {
  Serial.begin(115200);

  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
}
bool ReceiveData(){
  while(Serial.available() > 0){
    inputData = Serial.readStringUntil('\n');
    inputData.trim(); //remove white space
    return true;
  }
  return false;
}
/***
PLACE FUNCTIONS BELOW HERE
***/
void moveSolenoids(){
  //first solenoid ON
  digitalWrite(S1, HIGH);
  delay(500);

  //first solenoid OFF
  digitalWrite(S1, LOW);
  delay(3000);

  //second solenoid ON
  digitalWrite(S2, HIGH);
  delay(500);

  //second solenoid OFF
  digitalWrite(S2, LOW);
  delay(3000);
}

void loop() {
  if(ReceiveData()){
    if(inputData[0] == '$'){
      if(inputData[1] == 'S'){ 
        moveSolenoids();
        Serial.println("motion done");
      }else if(inputData[1] == 'W'){ 
        //wait function
      }else if(inputData[1] == 'K'){
        //kill function
      }else if(inputData[1] == 'D'){ 
        //debug function
      }else{
        Serial.println("Input is Not a Command!");
      }
    }else{
      Serial.println("Input Invalid!");
    }
  }
}

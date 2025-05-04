#include <Arduino.h>

String inputData = "";

int solenoidPin = 4;
bool signal = false;


void setup() {
  // put your setup code here, to run once:
  pinMode(solenoidPin, OUTPUT);
  Serial.begin(115200);
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
void loop() {  
  if(ReceiveData()){
    if(inputData[0] == '$'){
      if(inputData[1] == 'S'){ //start (starts the process)
        signal = true;
        Serial.println("magneto picking up");
      }else if(inputData[1] == 'W'){ // wait (standby mode -> idk)
        //wait function
      }else if(inputData[1] == 'K'){ // kill (stop current process)
        signal = false;
        Serial.println("magneto dropping");
      }else if(inputData[1] == 'D'){ // debug function
        //debug function
      }else{
        Serial.println("Input is Not a Command!");
      }
    }else{
      Serial.println("Input Invalid!");
    }
  }

  //solenoid signal send -> needed for solenoid to keep holding while 
  //dexarm moves
  if(signal){
    //when low level sent relay connects to solenoid circuit for seperate 4 relay module
    //when HIGH sent to 4 relay sheild NO to C connection established
    digitalWrite(solenoidPin, HIGH); 
    // digitalWrite(fanSignal, HIGH);
  }else{
    digitalWrite(solenoidPin, LOW);
  }

  //fan signal to turn off and on
  // unsigned long currentMillis = millis();
  // if(currentMillis - fanTime >= 5000){
  //   digitalWrite(fanSignal, LOW);
  // }
}


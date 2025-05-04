#include <Arduino.h>

//works needs capacitor in parallel w/ circuit 
#include <Servo.h> // servo library

Servo myservo; // servo name
int delayTime = 6;
String inputData = "";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  myservo.attach(9);
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
void flipItem(){
  // quick flip nametag  
  for(int i=0; i< 180; i++){
    myservo.write(i);
    delay(delayTime);
  }
}

void loop() {
  if(ReceiveData()){
    if(inputData[0] == '$'){
      if(inputData[1] == 'S'){ 
        flipItem();
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

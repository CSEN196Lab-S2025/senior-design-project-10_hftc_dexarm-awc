#include <Arduino.h>
#include <Servo.h> // servo library

Servo myServo; // servo name

int delayTime = 1500;
//ANGLES CHANGE DEPENDING ON INSTALLATION
int open_pos = 90;
int close_pos = 180;
String inputData = "";
void closeDoor();
void openDoor();


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  // put your setup code here, to run once:
  myServo.attach(9);
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

void closeDoor(){
  myServo.write(close_pos);
  delay(delayTime);
  Serial.println("close position!");
}
void openDoor(){
  myServo.write(open_pos);
  delay(delayTime);
  Serial.println("open position!");
}

void loop() {
  if(ReceiveData()){
    if(inputData[0] == '$'){
      if(inputData[1] == 'S'){ //start (starts the process)
        openDoor();
        Serial.println("motion done");
      }else if(inputData[1] == 'W'){ // wait (standby mode -> idk)
        //wait functionz
      }else if(inputData[1] == 'K'){ // kill (stop current process)
        closeDoor();
        Serial.println("motion done");
      }else if(inputData[1] == 'D'){ // debug function
        //debug function
      }else{
        Serial.println("Input is Not a Command!");
      }
    }else{
      Serial.println("Input Invalid!");
    }
  }
}

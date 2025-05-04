#include <Arduino.h>
#include <Servo.h> // servo library

Servo myServo; // servo name
void HomeServo();

int delayTime = 1500;
int trash_pos = 150;
int flip_pos = 0;
int home_pos = 60;
String inputData = "";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  // put your setup code here, to run once:
  myServo.attach(9);

  HomeServo();
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

void HomeServo(){
  myServo.write(home_pos);
  Serial.println("Homed!");
  delay(delayTime);
}
void goodProduct(){
  HomeServo();

  myServo.write(flip_pos);
  delay(delayTime-800);
  Serial.println("Flip position!");

  HomeServo();
}
void badProduct(){
  HomeServo();

  myServo.write(trash_pos);
  delay(delayTime);
  Serial.println("Trash position!");
  
  HomeServo();
}

void loop() {
  for(int i=0; i < 180; i++){
    myServo.write(i);
    delay(10);
  }
  delay(1000);
  for(int i=180; i > 0; i--){
    myServo.write(i);
    delay(10);
  }
  delay(1000);
}

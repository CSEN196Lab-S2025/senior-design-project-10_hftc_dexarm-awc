#include <Arduino.h>
#include <Wire.h>
#include <vl53l4cd_class.h>
#include <AccelStepper.h>

// #define Serial Serial
#define MEASUREMENTS 10 // Number of measurements to take

AccelStepper stepper(1, 8, 9);// direction Digital 9 (CCW), pulses (or step) Digital 8 (CLK)
const int limitSwitch = 10;
int position_home, position_init, position1, position2;

VL53L4CD sensor_vl53l4cd_sat(&Wire, A1);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(115200);
  while (!Serial); // Wait for Serial port to connect
  Serial.println("Sensor Ready...");

  Wire.begin();

  sensor_vl53l4cd_sat.begin();
  sensor_vl53l4cd_sat.VL53L4CD_Off();
  sensor_vl53l4cd_sat.InitSensor();
  sensor_vl53l4cd_sat.VL53L4CD_SetRangeTiming(200, 0);

  //min MaxSpeed = 200; min Acceleration = 400
  stepper.setMaxSpeed(200); //SPEED = Steps / second
  stepper.setAcceleration(400); //ACCELERATION = Steps /(second)^2
  stepper.enableOutputs(); //enable pins

  //limit switch
  pinMode(limitSwitch, INPUT); // Enable internal pull-up resistor
}
void move(int position){
  stepper.moveTo(position); //full rotation
  stepper.runToPosition();
}
void init_home() { //initialized positions on stepper motor then go to home
  // Move left "forever" until the limit switch is hit
  stepper.moveTo(-3200); // large negative number to go left "indefinitely"

  while (true) {
    if (digitalRead(limitSwitch) == HIGH) {
      // Emergency hard stop
      stepper.setCurrentPosition(0); // Reset position (optional)
      stepper.stop(); // Prepare to stop
      break;
    }
      stepper.run();
  }

  delay(200); // Give motor time to settle

  // int stepperEdge = stepper.currentPosition();

  position_home = stepper.currentPosition() + 20;
  position1 = position_home + 30;
  position2 = position_home + 200;
  position_init = position_home + 100;

  Serial.print("stepper home position: ");
  Serial.println(position_home);

  //move to home position
  stepper.moveTo(position_home);
    while (stepper.distanceToGo() != 0) {
    stepper.run();
  }

  Serial.println("HOME!");
}
void distSensor(){
  float totalDistance = 0;
  int validMeasurements = 0;

  for (int i = 0; i < MEASUREMENTS; ++i) {
    sensor_vl53l4cd_sat.VL53L4CD_StartRanging();
    
    uint8_t NewDataReady = 0;
    VL53L4CD_Result_t results;
    uint8_t status;

    // Wait for new data to be ready
    do {
      status = sensor_vl53l4cd_sat.VL53L4CD_CheckForDataReady(&NewDataReady);
    } while (!NewDataReady);

    digitalWrite(LED_BUILTIN, HIGH); // LED on

    sensor_vl53l4cd_sat.VL53L4CD_GetResult(&results);
    sensor_vl53l4cd_sat.VL53L4CD_ClearInterrupt(); // Clear interrupt for next measurement

    digitalWrite(LED_BUILTIN, LOW); // LED off

    if ((!status) && (NewDataReady != 0) && (results.range_status == 0)) {
      totalDistance += results.distance_mm;
      ++validMeasurements;
    }

    sensor_vl53l4cd_sat.VL53L4CD_StopRanging(); // Stop ranging

    // Wait for a bit to spread the measurements over 1 second
    delay(25); // This delay may need adjustment for precise timing
  }

  if (validMeasurements > 0) {
    float averageDistance = totalDistance / validMeasurements;
    Serial.print("$M");
    Serial.println(averageDistance);
  } else {
    Serial.println("Measurement Error");
  }

  Serial.println("$D"); // Indicate to the PC that the measurements are complete
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    Serial.print("given command: ");
    Serial.println(command);

    if (command == "$M") {
      distSensor();
    }else if(command == "$H"){ //home position
      init_home();
      Serial.println("moved to Home Position");
    }else if(command == "$I"){ //init position -> used for dexarm to have room to init
      move(position_init);
      Serial.println("pre init for dexarm");
    }else if(command == "$P1"){ //position 1 for picking up material
      move(position1);
      Serial.println("moved  to position 1");
    }else if(command == "$P2"){ //position 2 for dropping material on conveyer belt
      move(position2);
      Serial.println("moved to position 2");
    }else{
      Serial.println("invalid input");
    }
  }
}


#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>

Adafruit_MMA8451 mma = Adafruit_MMA8451();
char recievedChar;
boolean newData = false;

void setup(void) {
  Serial.begin(115200);
  

  if (! mma.begin()) {
    Serial.println("Couldnt start");
    while (1);
  }
  
  mma.setRange(MMA8451_RANGE_8_G);
  
}

void loop() {
  // Read the 'raw' data in 14-bit counts
  Serial.flush();
  recvInfo();
  /* Look for prompt to collect current event state */
  sendInfo();
  /* Send a new sensor event */
  
}

void recvInfo() {

  if (Serial.available() > 0) {
    recievedChar = Serial.read();
    newData = true;

  }
}

void sendInfo() {

  int recv = (recievedChar - '0');

    while (newData == true) {
      
      if (recv == 1) {
        sensors_event_t event; 
        mma.getEvent(&event);

        /* Display the results (acceleration is measured in m/s^2) */
        Serial.print(event.acceleration.x); Serial.print(","); Serial.print(event.acceleration.y); Serial.print(","); Serial.print(event.acceleration.z); Serial.print("\n");
      }

    newData = false;
    }
}

#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include <WiFi.h>

#define s0 19
#define s1 18
#define s2 5
#define s3 17
#define s4 16
#define s5 4
#define s6 2
#define s7 15

#define power_line 10

const int selectPins[] = {s0, s1, s2, s3, s4, s5, s6, s7};
const int numSelectPins = sizeof(selectPins) / sizeof(selectPins[0]);

const int pinArm1[] = {14,27,26,25};
const int pinArm2[] = {33,32,35,34};
const int numreadpin = sizeof(pinArm1) / sizeof(pinArm1[0]);

float arm1[10][10];
float arm2[10][10];

Adafruit_ADS1115 ads[3];
uint8_t i2c_addresses[3] = {0x48, 0x49, 0x4A};

void setup() {
  WiFi.mode(WIFI_OFF);
  btStop();
  Serial.begin(115200);
  Wire.begin();
  /*for (int i = 0; i <numreadpin; i++){
    pinMode(pinArm1[i], INPUT_PULLUP);
    pinMode(pinArm2[i], INPUT_PULLUP);
  }*/
  for (int i = 0; i < numSelectPins; i++) {
    pinMode(selectPins[i], OUTPUT);
  }
  for (int i = 0; i < 3; i++){
    if (!ads[i].begin(i2c_addresses[i])) {
      Serial.print("Failed to initialize ADS1115 at 0x");
      Serial.println(i2c_addresses[i], HEX);
    } else {
      Serial.print("ADS1115 at 0x");
      Serial.print(i2c_addresses[i], HEX);
      Serial.println(" initialized.");
      ads[i].setGain(GAIN_ONE);  // Set gain to ±4.096V
      ads[i].setDataRate(RATE_ADS1115_860SPS);  // Max speed
    }
  }
}

/*void loop() {
  for (int i = 0; i < 16; i++) {
    setMuxChannelleft(i);
    setMuxChannelright(i);
    int sensVal = analogRead(33);
    float volt = sensVal * (3.3/4095.0);
    Serial.print(volt);
    Serial.print("\n");
    delay(5);  // Hold each "switch" for 5ms
  }
}*/

void loop() {
  unsigned long Stime = micros();
  for (int i = 0; i < power_line; i++) {
    setMuxChannelleft(i);
    setMuxChannelright(i);
    // Read arm1 channels
    for (int ch = 0; ch < 6; ch++) {
      int16_t raw;
      float value;
      if (ch < 4) {
        // ads[0] channels 0-3
        raw = ads[0].readADC_SingleEnded(ch);
      } 
      else {
        // ads[1] channels 0 and 1 for ch = 4,5
        raw = ads[1].readADC_SingleEnded(ch - 4);
      }
      value = raw * (4.096 / 32767.0);
      if (value < 0) value = 0;
      arm1[i][ch] = value;
    }

    // Read arm2 channels
    for (int ch = 0; ch < 6; ch++) {
      int16_t raw;
      float value;
      if (ch < 4) {
        // ads[2] channels 0-3
        raw = ads[2].readADC_SingleEnded(ch);
      } 
      else {
        // ads[1] channels 2 and 3 for ch = 4,5
        raw = ads[1].readADC_SingleEnded(ch - 2);
      }
      value = raw * (4.096 / 32767.0);
      if (value < 0) value = 0;
      arm2[i][ch] = value;
    }

    for (int j = 0; j < numreadpin; j++) {
      int raw = analogRead(pinArm1[j]);
      float voltage = raw * (3.3 / 4095.0);
      arm1[i][j + 6] = voltage;  // next 4 slots after ADS
    }

    for (int j = 0; j < numreadpin; j++) {
      int raw = analogRead(pinArm2[j]);
      float voltage = raw * (3.3 / 4095.0);
      arm2[i][j + 6] = voltage;
    }
    delayMicroseconds(50);
  }
  printArrays();
  /*unsigned long rTime = micros();
  
  unsigned long endTime = micros();   // End of everything

  Serial.print("Read time (us): ");
  Serial.println(rTime - Stime);

  Serial.print("Print time (us): ");
  Serial.println(endTime - rTime);

  Serial.print("Total loop time (ms): ");
  Serial.println((endTime - Stime) / 1000.0);*/

}

void setMuxChannelleft(int channel) {
  digitalWrite(s0, channel & 1);
  digitalWrite(s1, (channel >> 1) & 1);
  digitalWrite(s2, (channel >> 2) & 1);
  digitalWrite(s3, (channel >> 3) & 1);
}

void setMuxChannelright(int channel) {
  digitalWrite(s4, channel & 1);
  digitalWrite(s5, (channel >> 1) & 1);
  digitalWrite(s6, (channel >> 2) & 1);
  digitalWrite(s7, (channel >> 3) & 1);
}

/*void printArrays() {
  Serial.println("START_ARM1");
  for (int i = 0; i < power_line; i++) {
    for (int j = 0; j < 10; j++) {
      Serial.print(arm1[i][j], 3);
      if (j < 9) Serial.print(",");
    }
    Serial.println();
  }

  Serial.println("START_ARM2");
  for (int i = 0; i < power_line; i++) {
    for (int j = 0; j < 10; j++) {
      Serial.print(arm2[i][j], 3);
      if (j < 9) Serial.print(",");
    }
    Serial.println();
  }
  Serial.println("END");
}*/

void printArrays() {
  Serial.println("START ");
  for (int i = 0; i < power_line; i++) {
    for (int j = 0; j < 10; j++) {
      Serial.print(arm1[i][j], 3);
      Serial.print(",");
    }
  }

  for (int i = 0; i < power_line; i++) {
    for (int j = 0; j < 10; j++) {
      Serial.print(arm2[i][j], 3);
      if (i == power_line - 1 && j == 9){
        Serial.print("\nEND\n");
      }
      else{
        Serial.print(",");
      }
    }
  }
}

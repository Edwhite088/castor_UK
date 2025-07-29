void setup() {
  Serial.begin(9600);
  pinMode(33, INPUT_PULLUP);
  digitalWrite(33, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  int sensVal = analogRead(33);
  float volt = sensVal * (3.3/4095.0);
  Serial.print(volt);
  Serial.print("\n");

}

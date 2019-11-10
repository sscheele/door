int pn_servo = 6;
int pn_servo_enable = 7;
bool should_enable = true;

int delay_len = 1100;

void setup() {
  // put your setup code here, to run once:
  pinMode(pn_servo, OUTPUT);
  pinMode(pn_servo_enable, OUTPUT);
  digitalWrite(pn_servo_enable, LOW);
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (should_enable) {
    digitalWrite(pn_servo_enable, HIGH);
    should_enable = false;
  } else {
    delay_len = 700;
  }
  int t = millis();
  while(millis() < t + 700) {
    digitalWrite(pn_servo, HIGH);
    delayMicroseconds(delay_len);
    digitalWrite(pn_servo, LOW);
    delayMicroseconds(20000 - delay_len);
  }
}

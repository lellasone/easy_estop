/* Serial passthrough drive firmware for the tortoise bot. 
 * 
 * This set of firmware acts as a passthrough for a main drive computer.
 * Messages are sent over serial to set motor angles or request sensor
 * data. 
 * 
 * Maintainer: Jake Ketchum (jketchum@u.northwestern.edu)
 */

#define LED_PIN 0
#define ESTOP_PIN 4

double steering_angle = 0;

void setup() {
  
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  pinMode(ESTOP_PIN, INPUT_PULLUP);
  update_led(1, 0);
  delay(200);
  update_led(0, 0);
  delay(400);
  update_led(1, 0);
  delay(200);
  update_led(0, 0);
}

void loop() {
  // put your main code here, to run repeatedly:
  process_serial();
}

bool get_button(){
  return (digitalRead(ESTOP_PIN));
}

void update_led(byte state, byte value)
/*
 * Write the LED pin. 
 * Args:
 *    state (byte) - contains 0 to dissable, or 1 to enable the LED.
 *    value (byte) - if 0, a digital write is used, if non-zero, an analogue write is used. 
 */
{
  
  if (value == 0)
  {
    digitalWrite(LED_PIN, state);
  }
  else
  {
    analogWrite(LED_PIN, state*value);
  }
}

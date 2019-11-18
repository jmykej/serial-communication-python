#include "HX711.h"

#define DOUT  2
#define CLK  3

int a = 1;

HX711 scale;

float calibration_factor = 3920; //-7050 worked for my 440lb max scale setup

void setup() {
  Serial.begin(115200);
//  Serial.println("HX711 calibration sketch");
//  Serial.println("Remove all weight from scale");
//  Serial.println("After readings begin, place known weight on scale");
//  Serial.println("Press + or a to increase calibration factor");
//  Serial.println("Press - or z to decrease calibration factor");

  scale.begin(DOUT, CLK);
  scale.set_scale();
  delay(100);
  scale.tare(); //Reset the scale to 0
  scale.set_scale(calibration_factor);
//  long zero_factor = scale.read_average(); //Get a baseline reading
//  Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
//  Serial.println(zero_factor);
}

void loop() {

  if(scale.is_ready()){
  
  Serial.println(scale.get_units(), 1);
  
  }



if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == 't' || temp == 'T')
      scale.tare();
  }
}

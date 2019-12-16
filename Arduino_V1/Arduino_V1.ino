#include <Servo.h>

Servo servoTable[6];
int c[3]= {};
unsigned char b[4] = {};


 typedef union{
  byte asBytes[4];
  int asInt;
}Data;

Data servos[3];



void setup() {
  
    servoTable[0].attach(4);
    servoTable[1].attach(5);
    servoTable[2].attach(6);
    servoTable[3].attach(7);
    servoTable[4].attach(8);
    Serial.begin(9600);
    for(int i = 0; i < 5; i++)
    {
      servoTable[i].write(0);
    }
    
}

void loop() {


if(Serial.available() == 12){
 for(int i = 0; i < 3; i++)
 {
  for(int j = 0; j < 4; j++)
  {
    servos[i].asBytes[j] = Serial.read();   
  }
 } 
 for(int i = 0; i < 3; i ++)
 {
  servoTable[i].write(servos[i].asInt);
 }

  
}
}
 




  
 
 
 

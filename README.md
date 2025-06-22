Bobert the Delivery Robot
Bobert is a small mobile robot built with an Arduino Uno, Raspberry Pi Pico W, and various sensors and actuators. He's controlled via Bluetooth from a smartphone, has a lift platform, camera, and expressive LCD eyes.

+ Features
  - Bluetooth control (HC-05 + phone app)

  - Differential drive (2 DC motors with L298N driver)

  - Servo-powered lift platform

  - Pan/tilt camera mount (using micro servos)

  - LCD screen "eyes" for feedback

  - Battery powered (AA pack)

  - Hybrid control system (Arduino + Pico W)

+ Hardware Components
Component	Description
    - Raspberry Pi Pico W	Control logic + Bluetooth handling
  
    - Arduino Uno
  
    - L298N Motor Driver	For driving two DC motors
  
    - DC Motors (x2)	Differential drive
  
    - HC-05 Bluetooth Module	Connects Bobert to your phone
  
    - Micro Servos (SG90, MG90)	For lift and camera
  
    - LCD Screen (I2C or parallel)	Facial expressions or status display
  
    - 18650 Battery Holder	Power source
  
    - Buck Converter (LM2596)	Power regulation (7.4V → 5V)
  

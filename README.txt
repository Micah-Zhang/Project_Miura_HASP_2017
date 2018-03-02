    ____  ____  ____      ____________________   __  _________  ______  ___ 
   / __ \/ __ \/ __ \    / / ____/ ____/_  __/  /  |/  /  _/ / / / __ \/   |
  / /_/ / /_/ / / / /_  / / __/ / /     / /    / /|_/ // // / / / /_/ / /| |
 / ____/ _, _/ /_/ / /_/ / /___/ /___  / /    / /  / // // /_/ / _, _/ ___ |
/_/   /_/ |_|\____/\____/_____/\____/ /_/    /_/  /_/___/\____/_/ |_/_/  |_|
    __  _____   _____ ____     ___   ____ ________ 
   / / / /   | / ___// __ \   |__ \ / __ <  /__  /
  / /_/ / /| | \__ \/ /_/ /   __/ // / / / /  / /
 / __  / ___ |___/ / ____/   / __// /_/ / /  / /
/_/ /_/_/  |_/____/_/       /____/\____/_/  /_/


Welcome to the Colorado Space Grant High Altitude Student Platform (HASP) 2017
flight software!


Mission Objective: Design and test feasibility of expandable and detractable origami space habitat.


Mission Duration: January 2017 - December 2017


Launch Date: September 4th, 2017


Launch Location: Columbia Scientific Balloon Facility, Ft. Sumner, New Mexico


Flight Duration: 20 hours


Programming Language: Python3


Microcontroller: Raspberry Pi 3 Model B


Flight Software Overview:

The role of the flight software is to write code to tell every sensor, camera, and motor exactly what to accomplish, when to accomplish it, and how to relay the data back to the team.

A Raspberry Pi was chosen to be the payload’s main computer for this project because an operating system simplifies file operations, and the Raspberry Pi allows for easy integration with sensors. All flight software was written in Python3 because of the low learning curve, and the existence of legacy code from previous missions.

To simplify the code logic and allow for simultaneous operations, the flight code relies on multithreading. The general design of the flight software employed on this payload consists of single high level “main” thread with 5 children threads. Each of the 5 children threads are specialized and are responsible for the operation of a unique function of the payload. These functions are as follows: downlink, uplink, motor command, sensor operation, and camera operation.


Flight Software Design:

Main Thread - The parent thread: “main” provides the following functionality:
1. Creates queues to allow for communication between threads
2. Creates necessary threading events, which are simple booleans for cross-thread communication
3. Initializes serial bus.
4. Creates children threads.
5. Allows for safe thread shutdown.

Downlink Thread - Handles all serial communication from the payload to the ground station, in a process known as downlink. More specifically, it provides the following functionality:
1. Sorts incoming data packets from the downlink queue and logs according to source
2. Packages incoming data packets with predefined headers and footers
3. Downlinks packaged packets over RS-232 bus

Uplink Thread - Handles all communication from the ground station to the payload. More specifically, it:
1. Receives uplink commands in the form of two-byte messages
2. Parses uplink commands and passes to relevant threads

Motor Thread - The motor thread controls all motor movement. More specifically, it:
1. Initializes the encoder thread, which monitors the motion of the rotary encoder. This device requires almost constant sampling, hence the separate thread
2. Performs top calibration of the payload refers to the payload extending upwards until a the top button is pressed. It then stores the current step count when the top button is pressed as the “maximum step count”.
3. Move the motor in the prescribed cyclical pattern
4. Perform “nudging” of the payload when the ground team sends a command to move up or down

Camera Thread - The camera thread controls the operation of the camera. More specifically, it:
1. Determines the image capture interval based on whether the payload is moving. During motion images are taken in ten second intervals, once per minute while stationary
2. Take an image, cycling through each of the four USB cameras

Sensor Thread - The sensor thread is responsible for all operation of the environmental sensors on the payload. More specifically, it:
1. Operates the temperature sensors.
2. Operates the pressure sensors.
3. Operates the humidity sensor.
4. Collects status updates on the Raspberry Pi, including core temperature, SD card usage, and CPU usage


If you have any questions regarding the flight software, please send your query via email to the following address: micah.zhang@colorado.edu

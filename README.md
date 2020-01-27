# RP3-ARM-AI
Repository for Design Laboratory project concerning Ai object recogniction and servomotor robotic arm

Code team: Magdalena Pikul (pikulm), Jan Magiera (ThrufR)
Project consultant: Sebastian Koryciak

Milestone one:
-- TBI
Milestone two:
-- TBI
Milestone three:
-- TBI 

General idea of this project is to create software for Raspberry PI 3, to utilize digital camera and servomotor based robotic arm. Our goal is to implement AI for proper object recognition and object manipulation (within the limits of arm's field).

## Steps
Firstly we tried to write our program to manage Arduino and the communication with the robots' arm because the given project was not working properly. During this process, we checked if all the components work.

As a result, we get the information, that all of the servos are working. Unfortunately, although the communication with single servos works sometimes, the communication with more servos breaks the connection via USB.
The bigger the information package we send, the faster the connection breaks.

Then following the advice of the project consultant, we tried using the command line interface. Regrettably, the program was keeping on breaking - independently from the Arduinos' content.
The connection with the computer was constantly interrupted and Arduino was resetting.

The next step was to try dealing with RaspberryPi - we hoped, that this might solve problems with USB connection. I haven't helped.

On a RaspberryPi also occurred problem with OpenCV libraries - the image from the camera was constantly lost.
Qt Library also hasn't worked in 100% properly.

In the meantime, we developed the algorithm to recognize text on the image (readme.md in a proper folder). If all issues with hardware would be solved, the next step will be integrating those elements altogether.




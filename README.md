# easy_estop
A simple arduino-based solution for e-stopping ROS projects. The e-stop node actively polls the micro at 50hz, and publishes the result to an e-stop topic, making it easy to impliment a fail-off architecture that will safe the robot if any component of the system goes down. 


The switch is NC and both the micro/topic are polled/published to at 50hz, making it easy to use a fail-off architecture that will robustly handle disconnections and most wiring faults. The code also supports 


What is this for: 
This project is perfect as the primary e-stop on a fairly safe robot, or as the software tier of a proper multi-level emergency stop system. It is also great as a "pause" button for running experiments. Essentially, if you would consider publishing to an e-stop topic from terminal then this is likely a superior solution. 

What is this not for: 
This e-stop works through ROS, and thus is not suitable as the primary e-stop for very fast or high-power platforms which should employ circuit or firmware level emergency stop measures. 

What I designed this for: 
I originally designed this to be the primary e-stop on a medium sized soft robot. In that role it lets me safely stop the platform during outreach, and provides a way to pause the robot if it becomes damaged during training.

**Software Setup**


**Hardware Selection**

The inexpensive component market shifts around over time,
Below are the exact components used in my reference build. Since the inexpensive component market shifts around over time you may need find analogues for the switch, LED carrier, and USB panel mount adapter. I am happy to help with this if you drop an issue. 


**Hardware Setup**

Once 

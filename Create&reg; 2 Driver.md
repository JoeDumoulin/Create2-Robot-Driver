# iRobot Create&reg; 2 Driver
Create2Driver.py is a small program for testing the most awesome Create2 robotics system.  The idea is to provide a simple command line easily run over ssh to perform basic commands.

The Create2 is a powerful robot constructed from refurbished Roomba&reg; systems from iRobot.  You can learn more about them [here](http://www.irobot.com/About-iRobot/STEM/Create-2.aspx).

There are a number of greate project tutorials all over the place.  iRobot hosts some good ones like [this one with a tkinter python app](http://www.irobot.com/~/media/MainSite/PDFs/About/STEM/Create/Python_Tethered_Driving.pdf).  Also [here is one for getting your raspberrypi working with the Create2](http://www.irobot.com/~/media/MainSite/PDFs/About/STEM/Create/RaspberryPi_Tutorial.pdf).

Finally, iRobot supplies [a great reference guide](http://www.irobot.com/~/media/MainSite/PDFs/About/STEM/Create/create_2_Open_Interface_Spec.pdf) which was used to inform the Create2Driver.  

## The Driver
The create 2 driver allows you to display and select a usb serial port to use to communicate with the Create 2.  Then you can send a subset of the allowed commands to the robot.  

The commands supported are of two kinds:

- State changes
- Moving and turning

### State Changes
The state changes supported by the Create2Driver are:

- passive
- safe
- full
- clean
- dock
- reset

these are documentented in the [Open Interface Spec](http://www.irobot.com/~/media/MainSite/PDFs/About/STEM/Create/create_2_Open_Interface_Spec.pdf).  Look there for explanations.  Suffice it to say that these modes are useful for experimenting with other commands on the robot.

### Moving and Turning
The driver includes commands for moving the robot around.  The commands are:

- move ahead n (integer number of centimeters)
- move back n (integer number of centimeters)
- turn right d (integer degrees)
- turn left d (integer degrees)

## Set up 
to run the driver you need a couple of things to be in place:

You need to install the pyserial library.  usually `pip install pyserial` will do the trick.

You need a Create 2 with a serial FTDI USB cable connected to the system issuing the commands.  This can be a computer or, ideally, a raspberry pi or other portable device that can be attached or travel with the robot.  The cable will usually come with the Create 2 robot.  

If you are using a pi or arduino to drive the system, they can be powered by he robot's battery.  see [this raspberry pi tutorial](http://www.irobot.com/~/media/MainSite/PDFs/About/STEM/Create/RaspberryPi_Tutorial.pdf) for more information.  See [this tutorial](http://www.irobot.com/~/media/MainSite/PDFs/About/STEM/Create/Arduino_Tutorial.pdf) for the Arduino.

## Start the Driver Program
You can start the Create 2 driver program by cloning the source from tis github page, performing the set up instructions above, and then running `python Create2Driver.py`.  This wil give you a command prompt.

## Define the Serial Port
After the program is running the first thing you have to do is set the serial port.
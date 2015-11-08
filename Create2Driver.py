# Create2Driver -- read commands to the create 2
#   convert them to op codes,
#   and send them to the create.
#   optionally read returned results.
from glob import *
import serial
import struct
import time
import math
import sys

def make_bytearray(robot_commands):
    return ''.join(chr(int(x)) for x in robot_commands.split())
    
def getserialports():
    if sys.platform == 'darwin':
        return '/dev/tty.*'
    elif sys.platform == 'linux':
        return '/dev/tty[A-Za-z]*'

class Command:
    def __init__(self):
        pass
    
    def check(self, cmdname):
        if (cmdname.strip().split()[0] == self.name): 
            return True
        else : return False
    
    def execute(self, command):
        pass
    
class Quit(Command):
    def __init__(self):
        self.name = 'quit'
    
    def execute(self, command):
        exit()
        
class Set(Command):
    def __init__(self, robot):
        self.name = 'set'
        self.robot = robot
    
    def execute(self, command):
        print 'command %s found' %self.name
        values = command.strip().split()
        if len(values)<=1:
            #display some kind of help message
            return
        if values[1] == 'usbserial':
            # select the usb driver at the number indicated 
            # and try to use it.
            if len(values) < 3:
                print 'which usbserial port number do you want?'
                return
            port = glob(getserialports())[int(values[2])]
            print 'using %s' %port
            self.robot.set_port(port)
        
class Show(Command):
    def __init__(self, robot):
        self.name = 'show'
        self.robot = robot
    
    def execute(self, command):
        print 'command %s found' %self.name
        values = command.strip().split()
        if len(values)<=1:
            #display some kind of help message
            return
        if values[1] == 'usbserial':
            usbserial_drivers = getserialports()
            for i,v in enumerate(glob(usbserial_drivers)):
                print '%d -- %s' %(i,v)
                
class State(Command):
    def __init__(self, robot):
        self.name = 'state'
        self.robot = robot
        self.states = {'passive':'128',
                       'safe':'131',
                       'full':'132',
                       'clean':'135',
                       'dock':'143',
                       'reset':'7'}
        
    def check(self, command):
        if command.strip().split()[0] in self.states.keys():
            return True
        return False
        
    def execute(self, command):
        print 'command %s found' %self.name
        values = command.strip().split()
        self.robot.send_command(make_bytearray(self.states[values[0]]))
        time.sleep(1)        
        
class Move(Command):
    def __init__(self, robot):
        self.name = 'move'
        self.robot = robot
        self.command_list = ['move', 'turn']
        
    def check(self, command):
        if command.strip().split()[0] in self.command_list:
            return True
        return False
        
    def execute(self, command):
        print 'command %s found' %self.name
        values = command.strip().split()
        if len(values) == 3:
            if values[0] == 'move':
                self.move(values[1:])
            elif values[0] == 'turn':
                self.turn(values[1:])
                
    def turn(self, where):
        wait = float(where[1])
        wait = (wait/self.robot.rotation)*35/9
        print 'wait = %f' %wait
        rotation = 0
        if where[0] == 'right':
            rotation = self.robot.rotation
        elif where[0] == 'left':
            rotation = -self.robot.rotation
        # move the robot
        self.move_robot(0,rotation)
        time.sleep(wait)
        self.move_robot(0,0)
        
    def move(self, where):
        wait = float(where[1])
        wait = wait*10/self.robot.velocity
        #set up the command
        velocity = 0
        if where[0] == 'ahead':
            velocity = -self.robot.velocity
        elif where[0] == 'back':
            velocity = self.robot.velocity
        # now move the robot
        self.move_robot(velocity,0)
        time.sleep(wait)
        self.move_robot(0,0)
            
    def move_robot(self, velocity, rotation):
        vr = velocity + rotation/2
        vl = velocity - rotation/2
        cmd = struct.pack(">Bhh", 145, vr, vl)
        self.robot.send_command(cmd)

class Create2:
    def __init__(self):
        self.conn = None
        self.velocity = 200 # mm/s
        self.rotation = 370 # mm/s each wheel (~one second full rotation)
    
    def set_port(self, port):
        try:
            self.conn = serial.Serial(port, baudrate=115200, timeout=1)
            #self.conn.close()
        except (OSError, serial.SerialException):
            print OSError.message
            pass
    
    # send the command through the serial connection.
    #   The byte array is a packed command string to the robot
    def send_command(self, command):
        try:
            if self.conn is not None:
                self.conn.write(command)
            else : print 'no connection!!'
        except serial.SerialException:
            print "Lost connection"
            self.conn = None
            pass
    
create = Create2()
        
commands = [
    Quit(),
    Set(create),
    Show(create),
    State(create),
    Move(create)
]
    
# parse a command and try to execute it
def do(commandtext):
    for command in commands:
        if command.check(commandtext):
            command.execute(commandtext)
            break
    else:
        print '%s is not a known command' %command

import fileinput
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        for line in fileinput.input():
            do(line)
    else:
        while (True):
            commandtext = raw_input('> ')
            if commandtext != None and commandtext != '':
                do(commandtext)


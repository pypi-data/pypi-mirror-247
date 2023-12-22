"""
LICENSE:
===============

    Copyright (c) 2018 Marita Fitzgerald and the Creative Science Foundation. All rights reserved.
    
    Last updated 10/12/2023 Simon Egerton

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


NOTES
===============
Version: 2.0.0


QUICK TUTORIAL:
===============

## view CodeePy Documentation
help(CodeePy)

# get current COM PORTS
CodeePy.get_com_ports()

# create CodeePy Instance and open connection
codee = CodeePy('<Your COM Port>')

# say text
codee.say("Hello")

# set melody tempo & play melody
codee.set_melody_tempo(2)
codee.play_melody("little lamb")

# play tone
codee.play_tone(2000, 300)

# play notes fixed duration
codee.play_notes(["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"], 1)  #C Major Scale
codee.exit()

#play notes with variable duration
codee.play_notes_with_duration(["C4.1", "D4.3", "E4.1", "F4.2", "G4.1", "A4.3", "B4.1", "C5.1"])
codee.exit()

#set left arm 30 degrees
codee.set_left_arm(30)
codee.exit()

#Swing both arms for 5 seconds then stop
#set arms to on
codee.swing_arms(2)
#set delay
time.sleep(5)
#stop arms
codee.stop_arms()
codee.exit()

#Set degrees of both arms
codee.set_arms(0, 0)

#Look around
# set head to look around
codee.look_around(2)
#set delay
time.sleep(3)
#stop head
codee.stop_head()
codee.exit()

# Set head image
codee.display_image("tick")

# Text scroll
codee.display_scroll_text("abcde")
# Allow time for text to scroll
# time.sleep(3)
# Stop Text Scroll
codee.display_stop_scroll_text()

# Display number
codee.display_number(85)

# Clear Display
codee.display_clear()

# Set LED display pixel
codee.display_set_pixel(0, 0, True)

# Changebluetooth name
codee.change_bot_bluetooth_name("happybot")

# Run single line sensor id no 5
codee.read_line_sensor(5)

# Returns the state of all line snesors as a single line position value, and a state integer 
# You can use 5 or inner 3 sensors as int
print(codee.read_line_sensors_position_and_state(5))

# Test Codee's wheel servos
for x in range(10):
    codee.set_left_wheel_velocity(10)
    codee.set_right_wheel_velocity(10)
    time.sleep(0.25)
codee.set_left_wheel_velocity(0)
codee.set_right_wheel_velocity(0)

# Set both wheel speeds
codee.set_wheel_velocities(10,10)

# Read the current ultrasound value 
print(codee.read_ultrasound_distance_cm)

# Read both AUX inputs 
print(codee.read_aux_input(1))
print(codee.read_aux_input(2))

# Close the serial connection & exit cleanly
codee.exit()
"""

import math
import time
from tkinter import CHAR
import pyfirmata2
import serial
import serial.tools.list_ports
from pyfirmata2 import util
from threading import Lock
from textwrap import wrap


class CodeePy:
    global line_sensor_1, line_sensor_2, line_sensor_3, line_sensor_4, line_sensor_5, notedictionary
   
    def __init__(self, port):
        """
        The constructor requires the programmer to pass the port name Codee is connected to either via USB(serial) or Bluetooth
        @param port: portname Codee is connected to.
        """
        self.port = port
        # instantiate codee as Pyfirmata object
        self.codee = pyfirmata2.Arduino(port)
        self.__set_as_nano()
        # connection reset and hello
        self.connect_reset_and_hello()
        # set up AUX inputs
        self.aux_1 = self.codee.get_pin('a:0:i')
        self.aux_2 = self.codee.get_pin('a:1:i')
        # set up line sensors
        self.line_sensor_1 = self.codee.get_pin('a:2:i')
        self.line_sensor_2 = self.codee.get_pin('a:3:i')
        self.line_sensor_3 = self.codee.get_pin('a:4:i')
        self.line_sensor_4 = self.codee.get_pin('a:5:i')
        self.line_sensor_5 = self.codee.get_pin('a:6:i')
        # initialise AUX variables 
        self.aux_1_reading, self.aux_2_reading = 0, 0
        # initilaise line state variables
        self.line_sensor_1_state, self.line_sensor_2_state, self.line_sensor_3_state, self.line_sensor_4_state, self.line_sensor_5_state = 0, 0, 0, 0, 0
        # instantiate handlers for line sensors
        self.line_sensor_1.register_callback(self.line_sensor_1_callback)
        self.line_sensor_2.register_callback(self.line_sensor_2_callback)
        self.line_sensor_3.register_callback(self.line_sensor_3_callback)
        self.line_sensor_4.register_callback(self.line_sensor_4_callback)
        self.line_sensor_5.register_callback(self.line_sensor_5_callback)
        # instantiate handlers for AUX inputs
        self.aux_1.register_callback(self.aux_1_callback)
        self.aux_2.register_callback(self.aux_2_callback)
        # default sampling interval of 19ms
        self.codee.samplingOn()
        # command callback data buffer
        self.command_response_data = []
        # command mutex
        self.command_mutex = Lock()
        self.command_response_mutex = Lock()
        # instantiate handler for commands
        self.codee.add_cmd_handler(pyfirmata2.STRING_DATA, self._messagehandler_command_callback)
        # note dictionary for user melodies amd tones
        self.notedictionary = {"RST": 0,
                               "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46, "G1": 49,
                               "GS1": 52,
                               "A1": 55, "AS1": 58, "B1": 62,
                               "C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93, "G2": 98,
                               "GS2": 104,
                               "A2": 110, "AS2": 117, "B2": 123,
                               "C3": 131, "CS3": 139, "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185,
                               "G3": 196,
                               "GS3": 208, "A3": 220, "AS3": 223, "B3": 248,
                               "C4": 262, "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370,
                               "G4": 392,
                               "G34": 415, "A4": 440, "AS4": 466, "B4": 494,
                               "C5": 523, "CS5": 554, "D5": 587, "DS5": 662, "E5": 659, "F5": 698, "FS5": 740,
                               "G5": 784,
                               "GS5": 831, "A5": 880, "AS5": 932, "B5": 988,
                               "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397, "FS6": 1480,
                               "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976,
                               "C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960,
                               "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951,
                               "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978}

    # Call back definitions

    def line_sensor_1_callback(self, data):
        self.line_sensor_1_state = (int(data + 0.5))

    def line_sensor_2_callback(self, data):
        self.line_sensor_2_state = (int(data + 0.5))

    def line_sensor_3_callback(self, data):
        self.line_sensor_3_state = (int(data + 0.5))

    def line_sensor_4_callback(self, data):
        self.line_sensor_4_state = (int(data + 0.5))

    def line_sensor_5_callback(self, data):
        self.line_sensor_5_state = (int(data + 0.5))
        
    def aux_1_callback(self, data):
        self.aux_1_reading = data

    def aux_2_callback(self, data):
        self.aux_2_reading = data

    # command message handler
    def _messagehandler_command_callback(self, *args, **kwargs):
        # process command response data
        self.command_response_data = []
        for digit in args:
            self.command_response_data.append(digit)
        # release command response mutext lock, informing caller data has been received
        try:
            self.command_response_mutex.release();
        except: RuntimeError
        
    # Public Functions

    def check_codee_firmware(self):
        """
        Checks firmata version is 2.5
        @return: True is Firmata is 2.5, False if it is not
        """
        print("Running pyFirmata version:\t%s" % pyfirmata2.__version__)
        if self.codee.get_firmata_version()[0] == 2 and self.codee.get_firmata_version()[1] == 5:
            print("Firmata version check passed OK")
            return True
        else:
            return False

    check_codee_firmware.__doc__ = "Check Firmata version is 2.5"

    

    def say(self, text):
        """
        This method makes Codee "Speak"
        @param text: a test string that Codee will say
        @return: True if Codee "Spoke", else False
        """
        text = text.strip()
        if len(text) < 30:
            saylist = [0x00]
            for x in text:
                saylist.append(ord(x))
            self.codee.send_sysex(0x09, saylist)
            return True
        else:
            print("Please enter text less than 30 characters in length")
            return False

    say.__doc__ = "Generate Audio tone for each char of a string (text)"

    def set_melody_tempo(self, tempo):
        """
        This method sets the tempo of melody playback
        @param tempo: an int tempo value
        """
        tmp = math.floor(tempo * 100)
        # frequency bytes
        t_low = tmp & 0xFF
        t_high = (tmp & 0xFFFF) >> 8
        self.codee.send_sysex(0x09, [0x04, t_high, t_low])

    set_melody_tempo.__doc__ = "Set tempo for playback"

    def play_melody(self, melody):
        """
        This method make Codee play preset melodies
        @param melody: preset melody Codee will play
        """
        global song_choice
        if melody == "green sleeves": song_choice = 0x00
        if melody == "little lamb": song_choice = 0x01
        if melody == "happy birthday": song_choice = 0x02
        if melody == "star wars": song_choice = 0x03
        if melody == "chariots": song_choice = 0x04
        self.codee.send_sysex(0x09, [0x01, song_choice])

    play_melody.__doc__ = "Melody variable choices: \n" \
                          "green sleeves \n" \
                          "little lamb \n" \
                          "happy birthday \n" \
                          "star wars \n" \
                          "chariots"

    def play_tone(self, frequency, duration):
        """
        This method makes Codee generate a tone
        @param frequency: int frequency of the tone
        @param duration: int duration of tone
        """
        # frequency bytes
        flow = frequency & 0xFF
        fhigh = (frequency & 0xFFFF) >> 8
        # durationbytes
        dlow = duration & 0xFF
        dhigh = (duration & 0xFFFF) >> 8
        self.codee.send_sysex(0x09, [0x03, fhigh, flow, dhigh, dlow])

    play_tone.__doc__ = "Play a single frequency tone for given milliseconds"

    def play_notes(self, noteList, duration):
        """
        This method will make Codee play notes of a given duration
        @param noteList: a list of note values as strings
        @param duration: int duration each note is played
        """
        # create melody list to hold song data
        melodylist = [0x02]
        for x in noteList:
            frequency = self.notedictionary.get(x, 0)  # set default value to 0 to avoid key errors
            flow = frequency & 0xFF
            fhigh = (frequency & 0xFFFF) >> 8
            melodylist.append(fhigh)
            melodylist.append(flow)
            melodylist.append(duration)
        self.codee.send_sysex(0x09, melodylist)

    play_notes.__doc__ = "Play notes from passed in List"

    def play_notes_with_duration(self, noteList):
        """
        This method will make Codee play notes of a given duration
        @param noteList: a list of note and duration values as strings delimited by '.'
        """
        # create melody list to hold song data
        melodylist = [0x02]
        # define notes/frequency key value pairs

        for x in noteList:
            frequency, duration = x.split('.')
            frequency = self.notedictionary.get(frequency, 0)  # set default value to 0 to avoid key errors
            flow = frequency & 0xFF
            fhigh = (frequency & 0xFFFF) >> 8
            melodylist.append(fhigh)
            melodylist.append(flow)
            melodylist.append(int(duration))
        self.codee.send_sysex(0x09, melodylist)

    play_notes_with_duration.__doc__ = "Play notes from passed in List"

    def swing_arms(self, speed):
        """
        This method will make Codee swing his arms
        @param speed: an int value between 0 and 10 inclusive
        """
        if speed > 10: speed = 10
        if speed < 0: speed = 0
        self.codee.send_sysex(0x0B, [speed, True])

    swing_arms.__doc__ = "Function to swing arms, speed is speed of swing"

    def set_right_arm(self, degrees):
        """
        This method will set Codees right arm to given degree
        @param degrees: an int value greater between -50 and 50 inclusive
        """
        degrees = 90 + degrees
        if (degrees) < 50: degrees = 50
        if (degrees > 130): degrees = 130
        self.codee.send_sysex(0x0E, [4, degrees])
        
    set_right_arm.__doc__ = "Set right servo angle to degrees x"

    def set_left_arm(self, degrees):
        """
        This method will set Codees left arm to given degree
        @param degrees: an int value between -50 and 50 inclusive
        """
        degrees = 90 + degrees
        if (degrees) < 50: degrees = 50
        if (degrees > 130): degrees = 130    
        self.codee.send_sysex(0x0E, [3, degrees])

    set_left_arm.__doc__ = "Set left servo angle to degrees x"

    def set_arms(self, leftarm_degree, rightarm_degree):
        """
        This method will set Codees arms to given degrees
        @param leftarm_degree: an int value between -90 and 90 inclusive
        @param rightarm_degree: an int value between -90 and 90 inclusive
        """
        self.set_left_arm(leftarm_degree)
        self.set_right_arm(rightarm_degree)

    set_arms.__doc__ = "Set both arm servo angles to degrees x, y"

    def stop_arms(self):
        """
        This method will stop Codee's arms moving
        """
        self.codee.send_sysex(0x0B, [0, 0])

    stop_arms.__doc__ = "Stop arm movement"

    def look_around(self, speed):
        """
        This method will make Codee's head turn from side to side
        @param speed: an int value between 0 and 5 inclusive
        """
        if speed > 5: speed = 5
        if speed < 0: speed = 0
        self.codee.send_sysex(0x0C, [speed, True])

    look_around.__doc__ = "Start head movement"

    def stop_head(self):
        """
        This method will stop Codee's head movements
        """
        self.codee.send_sysex(0x0C, [0, 0])

    stop_head.__doc__ = "Stop head movement"

    def set_head(self, degrees):
        """
        This method set Codee's head to a given degree
        @param degrees: an int value between -40 and 40 inclusive
        """
        
        degrees = 90 + degrees
        if (degrees) < 50: degrees = 50
        if (degrees > 130): degrees = 130    
        self.codee.send_sysex(0x0E, [5, degrees])

    set_head.__doc__ = "Set head to x position"

    def display_image(self, image):
        """
        This method will make Codees LED display a preset image
        @param image: string value of preset image
        """
        global imagetodisp
        if image == "smile": imagetodisp = 0x00
        if image == "neutral": imagetodisp = 0x01
        if image == "frown": imagetodisp = 0x02
        if image == "question": imagetodisp = 0x03
        if image == "ok": imagetodisp = 0x04
        if image == "tick": imagetodisp = 0x05
        if image == "cross": imagetodisp = 0x06
        if image == "rock": imagetodisp = 0x07
        if image == "paper": imagetodisp = 0x08
        if image == "sissors": imagetodisp = 0x09
        if image == "heart": imagetodisp = 0x0A
        if image == "quaver": imagetodisp = 0x0B
        if image == "quaverx2": imagetodisp = 0x0C
        if image == "blank": imagetodisp = 0x0D
        self.codee.send_sysex(0x0A, [0x01, imagetodisp])

    display_image.__doc__ = "Set head to selected image: \n" \
                       "smile \n" \
                       "neutral \n" \
                       "frown \n" \
                       "question \n" \
                       "ok \n" \
                       "tick \n" \
                       "cross \n" \
                       "paper \n" \
                       "sissors \n" \
                       "heart \n" \
                       "quaver \n" \
                       "quaverx2 \n" \
                       "blank"

    def display_scroll_text(self, text):
        """
        This method will make Codees LED display scroll given text
        @param text: text to scroll as string
        """
        if len(text) < 30:
            scroll_list = [0x02, True]
            for x in text:
                scroll_list.append(ord(x))
                self.codee.send_sysex(0x0A, scroll_list)
        else:
            print("Please enter text less than 30 characters in length")

    display_scroll_text.__doc__ = "Scroll text x on Codee head display"

    def display_stop_scroll_text(self):
        """
        This method will stop scrolling text and revert to state prior to scrolling
        """
        scroll_list = [0x02, False]
        self.codee.send_sysex(0x0A, scroll_list)

    display_stop_scroll_text.__doc__ = "Stop scroll text on Codee head display"

    def display_character(self, character):
        """
        This method will make Codees LED display display a character
        @param character : character to display as single character
        """
        self.codee.send_sysex(0x0A, [0x07, ord(character[0])])

    def display_number(self, number):
        """
        This method will make Codees LED display display a number
        @param number : number to display as int between 0 and 99 inclusive
        """
        if number >= 0 and number <= 99:
            self.codee.send_sysex(0x0A, [0x03, number])
        else:
            print("Please enter a number between 0 and 99")

    display_number.__doc__ = "Display number x on Codee head display"

    def display_clear(self):
        """
        This method will clear Codees LED display turning off all LED's
        """
        self.codee.send_sysex(0x0A, [0x06])

    display_clear.__doc__ = "Clear Codee head display"

    def display_set_pixel(self, row, column, state):
        """
        This method will set the state of a single LED in  Codees LED display
        @param row: row of pixel between 0 and 7 inclusive as int
        @param column: column of pixel between 0 and 7 inclusive as int
        @param state: set Pixel state True/False
        """
        if column > -1 and column < 8 and row > -1 and row < 8:
            self.codee.send_sysex(0x0A, [0x05, row, column, state])
        else:
            print("Please enter a row and column values between 0 and 7")

    display_set_pixel.__doc__ = "Set individual pixel state (True/False)"

    def set_left_wheel_velocity(self, speed):
        """
        This method will set the speed of the left wheel servo
        @param leftspeed: wheel speed between -30 and 30 inclusive as int
        """
        speed = 90 + speed
        if speed < 60: leftspeed = 60
        if speed > 120: leftspeed = 120
        self.codee.send_sysex(0x0E, [0x00, speed])

    set_left_wheel_velocity.__doc__ = "Set left wheel velocity"

    def set_right_wheel_velocity(self, speed):
        """
        This method will set the speed of the right wheel servo
        @param rightspeed: wheel speed between -30 and 30 inclusive as int
        """
        speed = 90 - speed
        if speed < 60: speed = 60
        if speed > 120: speed = 120
        self.codee.send_sysex(0x0E, [0x01, speed])

    set_right_wheel_velocity.__doc__ = "Set right wheel velocity"

    def set_wheel_velocities(self, leftspeed, rightspeed):
        """
        @param leftspeed: wheel speed between 0 and 180 inclusive as int
        @param rightspeed: wheel speed between 0 and 180 inclusive as int
        This method will set the speed of both wheel servos
        """
        self.set_right_wheel_velocity(rightspeed)
        self.set_left_wheel_velocity(leftspeed)

    set_wheel_velocities.__doc__ = "Set bothe wheel velocities, leftspeed rightspeed"

    def stop_wheels(self):
        """
        This method will stop both wheel servos
        """
        self.codee.send_sysex(0x0E, [0x02])

    stop_wheels.__doc__ = "Stop wheels"

    def change_bot_bluetooth_name(self, text):
        """
        This method will change the bluetooth name of your Codee
        @param text: new name as string
        """
        text = text.strip()
        if len(text) < 11:
            btlist = [1]
            # btlist = [01]
            for x in text:
                btlist.append(ord(x))
            self.codee.send_sysex(0x0D, btlist)
            time.sleep(8)
            self.codee.exit()
            print("Your robot is now named " + text)
        else:
            print("Please enter text less than 10 characters in length")

    change_bot_bluetooth_name.__doc__ = "Change Bluetooth name"

    def read_aux_input(self, aux_id):
        """
        This method will read the value of the AUX sensor
        and return a value of between 0 and 1
        @param aux_id: AUX ID as int either 1 or 2
        """
        if (aux_id == 1 or aux_id == 2):
            if aux_id == 1: return self.aux_1_reading
            if aux_id == 2: return self.aux_2_reading
        else:
            print("AUX ID should be either 1 or 2")
            
    read_aux_input.__doc__ = "Read status of AUX inputs"
                
    def read_line_sensor(self, sensor_id):
        """
        This method will read the value of one line sensor
        0.0 min value = black, 1.0 max value = white
        @param sensor_id: line sensor ID as int
        @param duration: time limit on sensor read
        @return result: the first read value that is not None else None is function has timed out
        """
        global line_sensor, result
        if (sensor_id >= 1 and sensor_id <= 5):
            if sensor_id == 1: line_sensor = self.line_sensor_1.state
            if sensor_id == 2: line_sensor = self.line_sensor_2.state
            if sensor_id == 3: line_sensor = self.line_sensor_3.state
            if sensor_id == 4: line_sensor = self.line_sensor_4.state
            if sensor_id == 5: line_sensor = self.line_sensor_5.state
            return result
        else:
            print("sensor ID should be between 1 and 5")

    read_line_sensor.__doc__ = "Read status of IR line sensor"

    def read_line_sensors_position_and_state(self, no_sensors):
        """
        This method will set the speed of both wheel servos
        @param no_sensors: no_sensor is either 3 or 5 as int
        @return array of int values 1 = black 0 = white
        """
        global sensor_result1, sensor_result2, sensor_result3, sensor_result4, sensor_result5, output_arr
        position, online, sensor_id = 0, 0, 0
        line_sensors = []

        if (no_sensors == 3 or no_sensors == 5):
            # set centre
            centre = 3
            if (no_sensors == 3): centre = 2            

            # read state of line sensors
            line_sensors.append(self.line_sensor_1_state)
            line_sensors.append(self.line_sensor_2_state)
            line_sensors.append(self.line_sensor_3_state)
            line_sensors.append(self.line_sensor_4_state)
            line_sensors.append(self.line_sensor_5_state)
            
            # calculate line position
            for sensor in line_sensors:
                sensor_id = sensor_id + 1
                if (sensor == 0):
                    online = online + 1
                    position = position + sensor_id
            
            # return results, line_position and line_state
            if (online == 0):
                return no_sensors + 1, 2 * no_sensors
            elif (online == no_sensors):
                return no_sensors, (2 * no_sensors) - 1
            else:
                return (position / online) - centre, int(2 * (((position / online) - centre) + 2))
        else:
            print("no of sensors must be 3 or 5")
            return 0

    read_line_sensors_position_and_state.__doc__ = "returns an array of all the sensor values that detect a black line, 1 is true 0 is false"

    def display_set_rows(self, hex_display_row_data):
        """
        This method will set the display rows
        @param hex: input rows as a 64 bit hex number i.e. 0x1122334455667788 where each two digit hex number is row, top to bottom
        """
        hex_display_data = [(hex_display_row_data >> (i * 8)) & 0xFF for i in range(7, -1, -1)]
        if len(hex_display_data) == 8:
            self.codee.send_sysex(0x0A, [0x04] + hex_display_data)
        else:
            print("Please enter 16 hex digits")

    display_set_rows.__doc__ = "Set active display rows"
    
    def connect_reset_and_hello(self):
        """
        This method will stop Codees limbs and reset the display and play "Hello World"
        """
        self.stop_arms()
        self.stop_head()
        self.stop_wheels()
        self.display_image("smile")
        self.say("Hello World!")
        
    connect_reset_and_hello.__doc__ = "Stop codee, reset display and say helllo world"

    def reset_codee_body_and_exit(self):
        """
        This method will reset Codees limbs to default position
        stop head, wheel movements and clear the display then disconnect codee
        """
        self.stop_arms()
        self.set_right_arm(0)
        self.set_left_arm(0)
        self.stop_head()
        self.set_head(0)
        self.stop_wheels()
        self.display_clear()
        time.sleep(2) # allow time for the servos to move
        self.stop_arms()
        self.stop_head()
        self.display_image("smile")
        self.exit()

    reset_codee_body_and_exit.__doc__ = "Reset codee's body and disconnect"

    def read_ultrasound_distance_cm(self):
        """
        This method will read Codees ultrasound sensor and return the result from 2 to 60 cm
        A result of 0 indicates no object detected
        """
        
        return self.__firmata_command(0x08, [])
        
    read_ultrasound_distance_cm.__doc__ = "Returns ultrasound distance sensor reading in cm"
    
    def read_battery_voltage(self):
        """
        This method will read Codees board voltage and return the result in volts to 1 decimal place.
        """
        
        return self.__firmata_command(0x07, [0x00]) / 10
        
    read_battery_voltage.__doc__ = "Returns board volatge in volts"
    
    def is_playing_melody(self):
        if (self.__firmata_command(0x07, [0x01]) == 1):
            return(True)
        return(False)

    is_playing_melody.__doc__ = "Returns true if codee is playing a melody, false otherwise"


    def is_scrolling_text(self):
        if (self.__firmata_command(0x07, [0x02]) == 1):
            return(True)
        return(False)

    is_scrolling_text.__doc__ = "Returns true if codee is scrolling text, false otherwise"
    
    def is_saying_text(self):
        if (self.__firmata_command(0x07, [0x03]) == 1):
            return(True)
        return(False)

    is_scrolling_text.__doc__ = "Returns true if codee is saying text, false otherwise"
    
    def is_moving(self):
        # maps to has_stopped, return is inverted
        if (self.__firmata_command(0x07, [0x04]) == 0): 
            return(True)
        return(False)

    is_moving.__doc__ = "Returns true if codee's wheels are moving, false otherwise"
 
    # Helper Functions

    @staticmethod
    def get_com_ports():
        """
        Can be called as a static class method to obtain COM ports on windows
        @return a list of COM ports (string)
        """
        print("COM port list")
        portlist = list(serial.tools.list_ports.comports())
        for p in portlist:
            print(p)
        return portlist

    get_com_ports.__doc__ = "Get list of available COM ports"

    def exit(self):
        self.codee.exit()

    exit.__doc__ = "Exit and disconnect port"

    def __set_as_nano(self):
        """
        Sets Firmata spec to nano
        """
        nano = {
            'digital': tuple(x for x in range(14)),
            'analog': tuple(x for x in range(8)),
            'pwm': (3, 5, 6, 9, 10, 11),
            'use_ports': True,
            'disabled': (0, 1)  # Rx, Tx, Crystal
        }
        self.codee.setup_layout(nano)
    
    def __firmata_command(self, command, data):
        """
        This method will issue a firmata command to codee and return the recrived value back to the calling method.
        """
        value = 0
        # aquire command mutex lock
        self.command_mutex.acquire()
        # aquire command response mutex lock, step 1
        self.command_response_mutex.acquire()
        # start ultrasound
        self.codee.send_sysex(command, data)
        # aquire command response mutex lock, step 2
        self.command_response_mutex.acquire()
        # decode response data
        for digit in self.command_response_data:
            #print("Digit 0x{:02x}".format(digit))
            if (digit == 0x0D): break;
            # update return value
            value = (value * 10) + (digit - 0x30)
        # release command response mutext lock
        self.command_response_mutex.release();
        # release command mutext lock
        self.command_mutex.release();
        return value
    
    __firmata_command.__doc__ = "This method will issue a firmata command to the connected board"

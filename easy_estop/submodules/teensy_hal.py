import serial
import codecs
import sys
import time
import numpy as np

COMMAND_ECHO = bytearray.fromhex("62")
COMMAND_PING = bytearray.fromhex("61")
COMMAND_SERVO = bytearray.fromhex("63")
COMMAND_LED = bytearray.fromhex("64")
COMMAND_BUTTON = bytearray.fromhex("6b")
START_BYTE = bytearray.fromhex("41")
END_BYTE = bytearray.fromhex("5A")


port = '/dev/ttyACM1'
baud = 115200

blank_message = bytearray.fromhex("00000000000000000000000000000000")

# This function composes and transmits each command frame. 
# It must be provided with the command byte, data payload,
# and length of expected reply (if appropriate)
# This function will return a list in the form [bool, responce] where 
# bool is True if the communication was succesful, and False if it failed. 
# if a length of 0 is specified for the responce that index will be set at ""
def send_frame(command, data, reply_length = 0, port_id = None):
	
	# if no port has been provided use the global default. 
	if port_id == None: 
		port_id = port

	try: 
	    teensy = serial.Serial(port_id,baudrate = baud)
	    frame = START_BYTE
	    frame = frame + command + data
	    frame = frame + bytearray.fromhex("00") # add checksum
	    frame = frame + END_BYTE
	    
	    print(frame)
	    teensy.write(frame)
	    if reply_length != 0:
	        return [True, teensy.read(reply_length)]
	    else:
	    	return [True, ""]
	except serial.SerialException as e: 
		print("serial exception: " + str(e))
		return[False,""]

def request_echo(payload):
    responce = send_frame(COMMAND_ECHO, payload, 2)
    return responce

def set_light(lit, value = 0, port_id = None):
    """ Set the LED's pin 0 led.
    Args:
        lit (bool) - should the led be on or off. 
        value (uint8) - if non-zero an analogue write will be used. if 0 then
                        a digital write will be used. 
        port_id (string) - which comport to use. 
    """
    message =  blank_message
    message[0] = int(lit)
    
    message[1] = value
    send_frame(COMMAND_LED, message, port_id = port_id)

# Requests the device ID of the target device. 
def request_ping(port_id = None):
	responce = send_frame(COMMAND_PING,
                              blank_message,
                              reply_length = 3,
                              port_id = port_id)
	return responce

def get_button(port_id = None):
    response = send_frame(COMMAND_BUTTON,
                          blank_message,
                          reply_length = 1,
                          port_id = port_id)
    return response

def set_servos(angles, port_id = None):
    message = blank_message
    for i in range(0, 16):
        assert(angles[i] < 256 and angles[i] >= 0)
        message[i] =  angles[i]
    send_frame(COMMAND_SERVO, message, port_id = port_id)  

def find_comport(id, max_num = 100):
	""" Search all comports for a teensy with the correct ID.

	This function is not thread-safe, see ros implimentation for a thread-safe
	variant. 
	
	Values are returned as a dict for ros compatability. 
	Args:
		id (byte[]) - A 3 byte string representing the teensy id. 
		max_num (int) - highest port index to try for each type. 
	Returns:
		success (bool) - true if found, false if not. 
		port (string) - port name if found, current port if not. 
	"""

	# Pause servo command sending
	time.sleep(0.1)


	target_id = id
	print("target_id: ",target_id)

	# Search ACM ports (teensy)
	for i in range(0, max_num):
		port = "/dev/ttyACM{}".format(i)

		success, response = request_ping(port_id = port)

		print((response))
		if success and response == target_id:
			return({"success":success, "port":port})

	# Search USB ports (esp32)
	for i in range(0, max_num):
		port = "/dev/ttyUSB{}".format(i)
		success, response = request_ping(port_id = port)
		print((response))
		if success and response == target_id:
			return({"success":success, "port":port})       
	
	# Nothing was found... 
	return({"success":False, "port":None})


if __name__ == "__main__":

    port_id = find_comport(b'STP')['port']
    print(port_id)
    set_light(True, 255, port_id)
    time.sleep(2)
    set_light(False,port_id =  port_id)
    print(request_ping(port_id = port_id))
    time.sleep(1)
    set_light(True, port_id =  port_id)
    time.sleep(2)
    set_light(False, port_id =  port_id)
    print(request_ping( port_id = port_id))

    for i in range(0, 100):
        print(get_button(port_id))
        time.sleep(0.1)
        led_value = np.sin(i*3.14/10) * 120 + 120
        set_light(True, int(led_value), port_id)

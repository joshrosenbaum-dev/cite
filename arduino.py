#   arduino.py
#   -------------------------------------------------------
#   Lights up each fidicual marker based on touch recognition
#   or removal.
#
#   https://pythonforundergradengineers.com/python-arduino-LED.html#write-a-python-script-to-turn-the-led-on-and-off
#
#   Current question(s): The serial monitor relies on each
#   device code (i.e. "COM4") -- how do we uniquely identify
#   each marker in this situation? Also, do COM numbers get
#   reassigned every time... how complex will this get?

from serial import Serial

def lightUp(flag):
    markerSerial = Serial('COM4', 9800, timeout = 1)
    if flag:
        markerSerial.write(b'H')    # ON
    else:
        markerSerial.write(b'L')    # OFF
    markerSerial.close()
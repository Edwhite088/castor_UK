import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port and baud rate
while True:
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        print(line)

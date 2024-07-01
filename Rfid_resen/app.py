import serial
import threading
import time

port1 = '/dev/ttyUSB0'
port2 = '/dev/ttyUSB1'

# Function to read from serial port and print data
def serial_reader(port):
    ser = serial.Serial(port, 4800, timeout=None)
    while True:
        try:
            line = ser.readline().strip()
            if line:
                decoded_line = line.decode('utf-8')
                print(f"Data from {port}: {decoded_line}")
        except serial.SerialException as e:
            print(f"Serial port error on {port}: {e}")
            time.sleep(1)  # Wait and retry after encountering an error

try:
    thread1 = threading.Thread(target=serial_reader, args=(port1,))
    thread2 = threading.Thread(target=serial_reader, args=(port2,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

except serial.SerialException as e:
    print(f"Serial port error: {e}")
except KeyboardInterrupt:
    print("\nProgram terminated by user")


#Ovaj program samo stampa vrednosti dok Serial_app.py smesta u bazu, sad ti iskoristi sta ti je lakse.
import serial
import threading
import sqlite3
import time

port1 = '/dev/ttyUSB0'
port2 = '/dev/ttyUSB1'

# Function to read from serial port and store data
def serial_reader(port):
    # SQLite database setup for this thread
    conn = sqlite3.connect('serial_data.db')
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS serial_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            port TEXT,
            data TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    ser = serial.Serial(port, 4800, timeout=None)
    while True:
        try:
            line = ser.readline().strip()
            if line:
                decoded_line = line.decode('utf-8')
                print(f"Data from {port}: {decoded_line}")
                insert_data(cursor, port, decoded_line)
        except serial.SerialException as e:
            print(f"Serial port error on {port}: {e}")
            time.sleep(1)  # Wait and retry after encountering an error

    # Close the database connection when done
    conn.close()

# Function to insert data into database
def insert_data(cursor, port, data):
    try:
        cursor.execute('INSERT INTO serial_data (port, data) VALUES (?, ?)', (port, data))
        cursor.connection.commit()  # Commit using the connection associated with the cursor
    except sqlite3.Error as e:
        print(f"Error inserting into database: {e}")

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
finally:
    # Closing the database connection when done
    conn.close()

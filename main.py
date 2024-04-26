import os
import serial
import serial.tools.list_ports
from database import Database
from password_hasher import PasswordHasher
from bbs import BBS

def main():
    com_port = detect_icom_radio_port()
    if com_port:
        ser = serial.Serial(com_port, 9600, timeout=1)
        BBS.initialize_radio(ser)
        database = Database(
            os.environ.get('DB_HOST'),
            os.environ.get('DB_USER'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_NAME')
        )
        password_hasher = PasswordHasher()
        bbs = BBS(ser, database)
        bbs.handle_packets()
    else:
        print("Icom radio not detected.")

def detect_icom_radio_port():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if "icom" in desc.lower() or "icom" in hwid.lower():
            return port
    return None

if __name__ == "__main__":
    main()

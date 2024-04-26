from password_hasher import PasswordHasher

class BBS:
    def __init__(self, ser, database):
        self.ser = ser
        self.db = database
        self.password_hasher = PasswordHasher()

    def send_packet(self, data):
        try:
            self.ser.write(data.encode())
            print("Packet sent successfully")
        except Exception as e:
            print(f"Error sending packet: {e}")

    def receive_packet(self):
        try:
            received_data = self.ser.readline().strip().decode()
            print("Received Packet Data:", received_data)
            return received_data
        except Exception as e:
            print(f"Error receiving packet: {e}")
            return None

    def initialize_radio(self):
        try:
            self.send_packet('PKT ON\r\n')  # Enable packet mode
            self.send_packet('PKTSEND 0\r\n')  # Disable automatic transmission
            print("Radio initialized for packet mode")
        except Exception as e:
            print(f"Error initializing radio: {e}")

    def register_user(self, username, password):
        salt = self.password_hasher.generate_salt()
        hashed_password = self.password_hasher.hash_password(password, salt)
        query = "INSERT INTO users (username, password_hash, salt) VALUES (%s, %s, %s)"
        params = (username, hashed_password, salt)
        self.db.execute_query(query, params)

    def login_user(self, username, password):
        query = "SELECT password_hash, salt FROM users WHERE username = %s"
        result = self.db.execute_query(query, (username,))
        if result:
            row = result.fetchone()
            if row:
                stored_password_hash, salt = row
                hashed_password = self.password_hasher.hash_password(password, salt)
                if hashed_password == stored_password_hash:
                    return True
        return False

    def send_message(self, sender, recipient, message):
        query = "INSERT INTO messages (sender, recipient, message) VALUES (%s, %s, %s)"
        params = (sender, recipient, message)
        self.db.execute_query(query, params)

    def get_messages(self, recipient):
        query = "SELECT sender, message FROM messages WHERE recipient = %s"
        result = self.db.execute_query(query, (recipient,))
        if result:
            messages = result.fetchall()
            return messages
        return []

    def handle_packets(self):
        while True:
            packet_data = self.receive_packet()
            if packet_data:
                # Process incoming packet data
                print("Received Packet Data:", packet_data)
                # For simplicity, assume packet_data includes command and parameters
                command, *params = packet_data.split()
                if command == "REGISTER":
                    if len(params) == 2:
                        username, password = params
                        self.register_user(username, password)
                    else:
                        self.send_packet("Invalid command format for REGISTER")
                elif command == "LOGIN":
                    if len(params) == 2:
                        username, password = params
                        if self.login_user(username, password):
                            self.send_packet(f"Login successful for user: {username}")
                        else:
                            self.send_packet("Invalid username or password")
                    else:
                        self.send_packet("Invalid command format for LOGIN")
                elif command == "SEND_MESSAGE":
                    if len(params) >= 3:
                        sender, recipient, message = params
                        self.send_message(sender, recipient, message)
                    else:
                        self.send_packet("Invalid command format for SEND_MESSAGE")
                elif command == "GET_MESSAGES":
                    if len(params) == 1:
                        recipient = params[0]
                        messages = self.get_messages(recipient)
                        for sender, message in messages:
                            self.send_packet(f"FROM: {sender} MESSAGE: {message}")
                    else:
                        self.send_packet("Invalid command format for GET_MESSAGES")

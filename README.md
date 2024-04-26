# Packet Radio BBS System

This is a simple Bulletin Board System (BBS) implemented over packet radio using an Icom IC-7300 transceiver. The BBS allows users to register, login, send and receive messages.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PartTimeLegend/packet-radio-bbs.git
   cd packet-radio-bbs
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Connect your Icom IC-7300 transceiver to your computer via USB.
2. Configure the MySQL database settings in your environment variables:
   ```bash
   export DB_HOST="your_database_host"
   export DB_USER="your_database_username"
   export DB_PASSWORD="your_database_password"
   export DB_NAME="your_database_name"
   ```
3. Run the `main.py` script:
   ```bash
   python main.py
   ```

## Features

- Register new users with username and password.
- Login existing users with username and password.
- Send messages to other users.
- Receive messages from other users.
- Initialise the Icom IC-7300 transceiver for packet radio mode.

## Contributing

Contributions are welcome! Please feel free to open a pull request or submit an issue if you find any bugs or have any suggestions for improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

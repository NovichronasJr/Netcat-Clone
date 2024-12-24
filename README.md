# Netcat Replacement
![Netcat Logo](https://via.placeholder.com/150 "Netcat Replacement Logo")

This is a Python-based implementation of a Netcat-like tool for networking tasks. It supports server-client communication, file uploads, command execution, and an interactive shell. This project is a good starting point to understand socket programming, threading, and basic command-line networking tools.

## Features

- **Server Mode**: Listen on a specified port for incoming connections.
- **Client Mode**: Connect to a server and send data or commands.
- **Command Execution**: Execute system commands on the server and return the output to the client.
- **Interactive Shell**: Provides a command shell for remote interaction.
- **File Upload**: Upload files from the client to the server.

## How It Works

### Server Mode
Run the script with the `-l` flag to start the server. The server will listen on the specified host and port for incoming connections.

Example:
```bash
python Netcat.py -t 0.0.0.0 -p 5556 -l -c
```

### Client Mode
Run the script without the `-l` flag to connect to a server. You can send commands or files depending on the mode.

Example:
```bash
python Netcat.py -t 127.0.0.1 -p 5556
```

## Usage

```bash
python Netcat.py -t target_host -p port [options]

Options:
  -l, --listen                Listen on [host]:[port] for incoming connections
  -e, --execute=file_to_run   Execute the given file upon receiving a connection
  -c, --command               Initialize a command shell
  -u, --upload=destination    Upload a file to [destination] upon receiving a connection
```

### Examples

1. **Start a server with a command shell**:
   ```bash
   python Netcat.py -t 0.0.0.0 -p 5556 -l -c
   ```

2. **Upload a file to the server**:
   ```bash
   python Netcat.py -t 0.0.0.0 -p 5556 -l -u=/path/to/destination
   ```

3. **Execute a command on the server**:
   ```bash
   python Netcat.py -t 0.0.0.0 -p 5556 -l -e="ls"
   ```

4. **Connect to a server as a client**:
   ```bash
   python Netcat.py -t 127.0.0.1 -p 5556
   ```

## Requirements

- Python 3.x

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/NovichronasJr/Netcat-Clone
   cd Netcat-Clone

   ```

2. Run the script using Python:
   ```bash
   python Netcat.py [options]
   ```

## Known Issues

- Requires a valid server-client setup for testing.

## Future Enhancements

- Support for UDP protocol.
- Build a GUI for easier usage.

## License

This project is open-source and available under the [MIT License](LICENSE).

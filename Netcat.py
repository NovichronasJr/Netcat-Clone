#!/usr/bin/env python3
import sys
import socket
import getopt
import threading
import subprocess

# Define global variables
listen = False
command = False
upload = False
execute = ""
upload_destination = ""
target = ""
port = 0

def usage():
    print("Netcat Replacement")
    print()
    print("Usage: Netcat.py -t target_host -p port")
    print("-l --listen                - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run   - execute the given file upon receiving a connection")
    print("-c --command               - initialize a command shell")
    print("-u --upload=destination    - upon receiving connection upload a file and write to [destination]")
    print()
    print("Examples:")
    print("Netcat.py -t 192.168.0.1 -p 5555 -l -c")
    print("Netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("Netcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./Netcat.py -t 192.168.11.12 -p 135")
    sys.exit(0)

def client_handler(client_socket):
    global upload
    global execute
    global command

    # Check for upload
    if len(upload_destination):
        file_buffer = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file_buffer += data

        try:
            with open(upload_destination, "wb") as file_descriptor:
                file_descriptor.write(file_buffer)
            client_socket.send(f"Successfully saved file to {upload_destination}\r\n".encode('utf-8'))
        except Exception as e:
            client_socket.send(f"Failed to save file to {upload_destination}: {str(e)}\r\n".encode('utf-8'))

    # Check for command execution
    if len(execute):
        output = run_command(execute)
        client_socket.send(output.encode('utf-8'))

    # Command shell execution
    if command:
        while True:
            try:
                client_socket.send(b"<NETC:#> ")
                cmd_buffer = ""
                while "\n" not in cmd_buffer:
                    cmd_buffer += client_socket.recv(1024).decode('utf-8')
                
                print(f"Received command: {cmd_buffer}")  # Debugging: Show received command in the server log
                response = run_command(cmd_buffer)
                print(f"Sending response: {response}")  # Debugging: Show the response being sent back
                client_socket.send(response.encode('utf-8'))
            except Exception as e:
                print(f"Exception: {str(e)}")
                break

def run_command(command):
    command = command.rstrip()
    try:
        # Ensure text output, and capture both stdout and stderr
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
        print(f"Command Output: {output}")  # Debugging: Show command output in the server log
    except subprocess.CalledProcessError as e:
        output = f"Command failed: {e.output}\r\n"
        print(f"Command failed: {e.output}")  # Debugging: Show error output in the server log
    except Exception as e:
        output = f"Error: {str(e)}\r\n"
        print(f"Error: {str(e)}")  # Debugging: Show general error in the server log
    return output


def server_loop():
    global target
    global port

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((target, port))
        print(f"[*] Server bound to {target}:{port}")  # Debugging: Confirm binding
    except OSError as e:
        print(f"Error binding to {target}:{port} - {e}")
        sys.exit(1)

    server.listen(5)
    print(f"[*] Listening on {target}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")  # Debugging: Confirm accepted connection

        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def client_sender(buffer):
    global target
    global port

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer.encode('utf-8'))

        while True:
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode('utf-8')
                if recv_len < 4096:
                    break

            print(response, end="")

            buffer = input("")
            buffer += "\n"
            client.send(buffer.encode('utf-8'))
    except Exception as e:
        print(f"[*] Exception: {str(e)}")
        client.close()

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute=", "target=", "port=", "command", "upload="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)

    if listen:
        server_loop()

if __name__ == "__main__":
    main()

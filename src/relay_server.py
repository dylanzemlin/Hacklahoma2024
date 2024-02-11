import socket
import threading
import argparse

# Configuration for the relay
listen_addr = "0.0.0.0"
listen_port = 65431
forward_client = None
forward_ready = False
microphone_thread = None
microphone_die = False
transmit_type = "MICROPHONE"
receive_type = "TRANSCRIBER"

def microphone_client(connection, address):
    global forward_client, forward_ready
    print(f"Received connection from {address}")
    with connection:
        while not microphone_die:
            data = None
            try:
                data = connection.recv(1024 * 1024)
            except Exception as e:
                print(f"Failed to receive data from {address}: {e}")
                break
            if not data:
                break
            print(f"Received {len(data)} bytes from {address}")
            # Forward the data to the destination
            if forward_ready:
                try:
                    forward_client.sendall(data)
                except Exception as e:
                    forward_ready = False
                    forward_client = None
                    break

def listen_for_data():
    global forward_ready, forward_client, microphone_thread, microphone_die
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((listen_addr, listen_port))
    sock.listen(1)
    
    print(f"Listening on {listen_addr}:{listen_port} for incoming TCP packets...")

    while True:
        try:
            # Wait for a connection
            conn, addr = sock.accept()
            print(f"Received connection from {addr}")
            
            # Check their type
            user_data = conn.recv(1024)
            print(f"Received {user_data} from {addr}")
            
            if user_data == bytes(transmit_type, "utf-8"):
                microphone_die = True
                if microphone_thread is not None:
                    print("Waiting for microphone thread to die...")
                    microphone_thread.join()
                microphone_die = False
                microphone_thread = threading.Thread(target=microphone_client, args=(conn, addr))
                microphone_thread.daemon = True
                microphone_thread.start()
                continue
        
            if user_data == bytes(receive_type, "utf-8"):
                forward_ready = True
                forward_client = conn
                print(f"Forwarding set to {addr}")
                continue
        except KeyboardInterrupt:
            print("Shutting down...")
            sock.close()
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

def main():
    listen_for_data()
        
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Relay server for Whisper")
    argparser.add_argument("--listen_addr", default="0.0.0.0", help="Address to listen on", type=str)
    argparser.add_argument("--listen_port", default=65431, help="Port to listen on", type=int)
    argparser.add_argument("--transmit_type", default="MICROPHONE", help="Type of data to transmit", type=str)
    argparser.add_argument("--receive_type", default="TRANSCRIBER", help="Type of data to receive", type=str)
    
    args = argparser.parse_args()
    listen_addr = args.listen_addr
    listen_port = args.listen_port
    transmit_type = args.transmit_type
    receive_type = args.receive_type
    
    main()
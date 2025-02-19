import socket
import struct

def start_teltonika_server(host='0.0.0.0', port=5020):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"TCP Listening on {host}:{port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"TCP Connection from {client_address}")
        
        try:
            # Receive the IMEI number (length-prefixed)
            imei_length = struct.unpack('B', client_socket.recv(1))[0]
            imei = client_socket.recv(imei_length).decode('utf-8')
            print(f"Received IMEI: {imei}")
            
            # Send acknowledgment byte (0x01)
            client_socket.sendall(b'\x01')
            
            # Receive the AVL data packet
            preamble = client_socket.recv(4)
            if preamble != b'\x00\x00\x00\x00':
                print("Invalid preamble")
                continue
            
            data_field_length = struct.unpack('>I', client_socket.recv(4))[0]
            codec_id = struct.unpack('B', client_socket.recv(1))[0]
            if codec_id != 0x08:
                print(f"Unexpected Codec ID: {codec_id}")
                continue
            
            number_of_data_1 = struct.unpack('B', client_socket.recv(1))[0]
            avl_data = client_socket.recv(data_field_length - 10)  # Subtracting lengths of known fields
            number_of_data_2 = struct.unpack('B', client_socket.recv(1))[0]
            crc = client_socket.recv(2)
            
            # Process the AVL data
            process_avl_data(avl_data)
            
            # Send acknowledgment for the received data
            client_socket.sendall(struct.pack('>I', number_of_data_1))
        
        except Exception as e:
            print(f"Error processing data: {e}")
        
        finally:
            client_socket.close()

def process_avl_data(data):
    # Implement your AVL data processing logic here
    print(f"Processing AVL data: {data.hex()}")

if __name__ == "__main__":
    start_teltonika_server()

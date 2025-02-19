# import socket
# import threading

# def start_tcp_listener(host='0.0.0.0', port=5020):
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server_socket.bind((host, port))
#     server_socket.listen(5)
#     print(f"TCP Listening on {host}:{port}")
    
#     while True:
#         client_socket, client_address = server_socket.accept()
#         print(f"TCP Connection from {client_address}")
        
#         data = client_socket.recv(1024)
#         if data:
#             print(f"TCP Received: {data.decode('utf-8')}")
#             client_socket.sendall(b"Message received")
        
#         client_socket.close()

# def start_udp_listener(host='0.0.0.0', port=5021):
#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_socket.bind((host, port))
#     print(f"UDP Listening on {host}:{port}")
    
#     while True:
#         data, client_address = udp_socket.recvfrom(1024)
#         print(f"UDP Received from {client_address}: {data.decode('utf-8')}")
#         udp_socket.sendto(b"Message received", client_address)

# if __name__ == "__main__":
#     tcp_thread = threading.Thread(target=start_tcp_listener)
#     udp_thread = threading.Thread(target=start_udp_listener)
    
#     tcp_thread.start()
#     udp_thread.start()
    
#     tcp_thread.join()
#     udp_thread.join()

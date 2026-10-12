import socket

class MyServer:
    def __init__(self, address="127.0.0.1", port=5050):
        self.address = address
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            server_socket.bind((self.address, self.port))
            server_socket.listen()
            print(f"TCP Server is listening on {self.address}:{self.port}...")
            
            while True:
                try:
                    conn, addr = server_socket.accept()
                    print(f"Client connected: {addr}")
                    
                    with conn:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                print(f"Client {addr} disconnected.")
                                break
                            
                            print(f"Received: {data.decode('utf-8')} from {addr}. Sending back...")
                            conn.sendall(data)
                
                except KeyboardInterrupt:
                    print("\nServer shutting down manually (Ctrl+C).")
                    break

if __name__ == "__main__":
    server = MyServer()
    server.run()
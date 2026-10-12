import socket

class RawHTTPServer:
    def __init__(self, address="127.0.0.1", port=8000):
        self.address=address
        self.port=port

    def safe_send(self, conn: socket.socket, message: str):
        try:
            conn.sendall(message.encode('utf-8'))
        except ConnectionError as e:
            print(f"Client disconnected during send: {e}")

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            server_socket.bind((self.address, self.port))
            server_socket.listen()
            print(f"Server is listening on {self.address}:{self.port}...")

            while True:
                try:
                    conn, addr = server_socket.accept()
                    print(f"Client connected: {addr}")
                    
                    with conn:

                        try:
                            data = conn.recv(1024)
                        except ConnectionError as e:
                            print(f"Client disconnected during receiving: {e}")
                            continue

                        if not data:
                            print(f"Client {addr} disconnected.")
                            continue

                        decoded = data.decode('utf-8', errors='ignore')
                        lines = decoded.splitlines()
                        if not lines:
                            continue

                        print(f"Request: {lines[0]}")

                        if lines[0].startswith("GET / HTTP/1.1"):
                            response = (
                                "HTTP/1.1 200 OK\r\n"
                                "Content-Type: text/html; charset=utf-8\r\n"
                                "Connection: close\r\n"
                                "\r\n"
                                "<h1>Raw HTTP server sent this to you</h1>"
                            )
                            self.safe_send(conn, response)
                        
                        elif lines[0].startswith("GET /favicon.ico"):
                            response = (
                                "HTTP/1.1 404 Not Found\r\n"
                                "Connection: close\r\n"
                                "Content-Length: 0\r\n"
                                "\r\n"
                            )
                            self.safe_send(conn, response)

                        else:
                            response = (
                                "HTTP/1.1 400 Bad Request\r\n"
                                "Connection: close\r\n"
                                "\r\n"
                            )
                            self.safe_send(conn, response)
                
                except KeyboardInterrupt:
                    print("\nServer shutting down manually (Ctrl+C).")
                    break


if __name__ == "__main__":
    server = RawHTTPServer()
    server.run()
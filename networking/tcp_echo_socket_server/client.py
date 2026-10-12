import socket
import time

class MyClient:
    def __init__(self, server_address="127.0.0.1", server_port=5050):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.connect((server_address, server_port))
        print(f"Client initialized and connected to {server_address}:{server_port}")

    def send_string(self, message):
        print(f"Sending message to the server...")
        self.socket.sendall(message.encode('utf-8'))
        response = self.socket.recv(1024)
        print(f"Message sent, received response: {response.decode('utf-8')}")

    def close(self):
        self.socket.close()

if __name__ == "__main__":
    client = MyClient()
    client.send_string("Message to the server")
    client.send_string("Another message")
    time.sleep(2)
    client.send_string("The last message")
    client.close()
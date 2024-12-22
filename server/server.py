"""
openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -days 365 -nodes
"""
import ssl
import socket

HOST = '127.0.0.1'
PORT = 8446

# Paths to the server's certificate and private key files
CERTFILE = 'server.crt'
KEYFILE = 'server.key'

def create_tls_server():
    
    # Create an SSL context explicitly for TLS 1.2
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    # Force RSA for key exchange
    context.set_ciphers('RSA')

    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)

    return context.wrap_socket(server_socket, server_side=True)

def handle_client(connection):
    try:
        print("Client connected.")

        data = connection.recv(4096)
        print("Received:", data.decode('utf-8'))

        response = "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, Client!"
        connection.send(response.encode('utf-8'))
        print("Response sent.")
    except Exception as e:
        print("Error handling client:", e)
    finally:
        connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    print(f"Starting TLS server on {HOST}:{PORT}...")
    tls_server = create_tls_server()

    try:
        while True:
            connection, address = tls_server.accept()
            print(f"Connection accepted from {address}")
            handle_client(connection)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        tls_server.close()
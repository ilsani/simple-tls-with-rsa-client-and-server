import ssl
import socket

# Configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8446

def create_ssl_client():
    # Create an SSL context for TLS 1.2
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    # Force RSA as the key exchange method
    context.set_ciphers('RSA')

    # Load trusted certificates
    context.check_hostname = False       # Disable hostname verification for testing
    context.verify_mode = ssl.CERT_NONE  # Disable certificate verification for testing

    # Create a socket and wrap it with SSL
    raw_sock = socket.create_connection((SERVER_HOST, SERVER_PORT))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=SERVER_HOST)

    return ssl_sock

def main():
    try:
        # Create SSL client
        ssl_sock = create_ssl_client()
        print("SSL/TLS connection established.")

        # Send an HTTP request as an example application data
        request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(SERVER_HOST)
        ssl_sock.sendall(request.encode('utf-8'))

        # Receive server response
        response = ssl_sock.recv(4096)
        print("Server response:")
        print(response.decode('utf-8'))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if ssl_sock:
            ssl_sock.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()

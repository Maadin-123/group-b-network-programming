import socket
import threading
import time

class HelpdeskServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.ticket_counter = 1000
        
    def start(self):
        """Start the server and listen for connections"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print(f"[SERVER] Helpdesk Server started on {self.host}:{self.port}")
        print("[SERVER] Waiting for client connections...")
        print("[SERVER] Press Ctrl+C to stop\n")
        
        try:
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"[SERVER] Connection established from {client_address}")
                
                # Handle each client in a new thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n[SERVER] Shutting down...")
        finally:
            server_socket.close()
    
    def handle_client(self, client_socket, client_address):
        """Handle communication with a single client"""
        try:
            # Receive data from client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                return
            
            # Parse client message (format: "reg_number|issue")
            parts = data.split('|')
            if len(parts) >= 2:
                reg_number = parts[0].strip()
                issue = parts[1].strip()
                
                print(f"[SERVER] Received from {client_address}:")
                print(f"    Registration: {reg_number}")
                print(f"    Issue: {issue}")
                
                # Generate ticket number
                self.ticket_counter += 1
                ticket_number = f"TKT-{self.ticket_counter}"
                
                # Send response back to client
                response = f"Ticket generated: {ticket_number}"
                client_socket.send(response.encode('utf-8'))
                
                print(f"[SERVER] Sent: {response}\n")
            else:
                client_socket.send("ERROR: Invalid format. Use: reg_number|issue".encode('utf-8'))
                
        except Exception as e:
            print(f"[SERVER] Error handling client: {e}")
        finally:
            client_socket.close()

def main():
    server = HelpdeskServer()
    server.start()

if __name__ == "__main__":
    main()
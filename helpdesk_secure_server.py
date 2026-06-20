import socket
import threading
import time
from datetime import datetime
import os

class SecureHelpdeskServer:
    def __init__(self, host='127.0.0.1', port=5001):
        self.host = host
        self.port = port
        self.ticket_counter = 1
        self.TOKEN = "NET123"  # Secret token for validation
        self.MIN_MESSAGE_LENGTH = 10  # Minimum message length
        self.log_file = "helpdesk.log"
        
        # Create log file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("=== HELPDESK LOG ===\n")
                f.write(f"Server started at {datetime.now()}\n\n")
    
    def log_message(self, message):
        """Write message to log file"""
        with open(self.log_file, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
        print(f"[LOG] {message}")
    
    def generate_ticket(self):
        """Generate a unique ticket number"""
        ticket = f"HD{self.ticket_counter:03d}"
        self.ticket_counter += 1
        return ticket
    
    def start(self):
        """Start the secure server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        self.log_message(f"Secure Helpdesk Server started on {self.host}:{self.port}")
        self.log_message(f"Token: {self.TOKEN}")
        self.log_message(f"Min message length: {self.MIN_MESSAGE_LENGTH}")
        print(f"[SERVER] Waiting for client connections...\n")
        
        try:
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"[SERVER] Connection established from {client_address}")
                
                # Handle each client in a new thread (multiple clients!)
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            self.log_message("Server shutting down...")
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
            
            # Parse client message (format: "token|reg_number|issue")
            parts = data.split('|')
            
            # VALIDATION 1: Check if message has correct format
            if len(parts) < 3:
                response = "ERROR: Invalid format. Use: token|reg_number|issue"
                client_socket.send(response.encode('utf-8'))
                self.log_message(f"REJECTED (Invalid format): {data}")
                print(f"[SERVER] Rejected: Invalid format from {client_address}")
                return
            
            token = parts[0].strip()
            reg_number = parts[1].strip()
            issue = parts[2].strip()
            
            # VALIDATION 2: Check token
            if token != self.TOKEN:
                response = "ERROR: Invalid token. Access denied."
                client_socket.send(response.encode('utf-8'))
                self.log_message(f"REJECTED (Invalid token): {reg_number} - {issue}")
                print(f"[SERVER] Rejected: Invalid token from {client_address}")
                return
            
            # VALIDATION 3: Check message length
            if len(issue) < self.MIN_MESSAGE_LENGTH:
                response = f"ERROR: Message too short. Minimum {self.MIN_MESSAGE_LENGTH} characters."
                client_socket.send(response.encode('utf-8'))
                self.log_message(f"REJECTED (Too short): {reg_number} - '{issue}'")
                print(f"[SERVER] Rejected: Message too short from {client_address}")
                return
            
            # ALL VALIDATIONS PASSED - Process the request
            ticket_number = self.generate_ticket()
            
            # Log the accepted request
            self.log_message(f"ACCEPTED: {reg_number} | Issue: {issue} | Ticket: {ticket_number}")
            
            # Send response back to client
            response = f"SUCCESS: Ticket generated: {ticket_number}"
            client_socket.send(response.encode('utf-8'))
            
            print(f"[SERVER] Accepted from {client_address}:")
            print(f"    Registration: {reg_number}")
            print(f"    Issue: {issue}")
            print(f"    Ticket: {ticket_number}\n")
            
        except Exception as e:
            print(f"[SERVER] Error handling client: {e}")
            self.log_message(f"ERROR: {e}")
        finally:
            client_socket.close()

def main():
    server = SecureHelpdeskServer()
    server.start()

if __name__ == "__main__":
    main()
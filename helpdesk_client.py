import socket

class HelpdeskClient:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
    
    def send_request(self, reg_number, issue):
        """Send a helpdesk request to the server"""
        try:
            # Create socket and connect
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            
            # Prepare message: "reg_number|issue"
            message = f"{reg_number}|{issue}"
            client_socket.send(message.encode('utf-8'))
            
            # Receive response from server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"[CLIENT] Server response: {response}")
            
            client_socket.close()
            return response
            
        except ConnectionRefusedError:
            print("[CLIENT] ERROR: Could not connect to server. Is the server running?")
            return None
        except Exception as e:
            print(f"[CLIENT] ERROR: {e}")
            return None

def main():
    print("=" * 50)
    print(" HELPDESK CLIENT")
    print("=" * 50)
    
    # Get user input
    reg_number = input("Enter your registration number: ")
    issue = input("Describe your issue: ")
    
    # Send request
    client = HelpdeskClient()
    response = client.send_request(reg_number, issue)
    
    if response:
        print("\n[CLIENT] Request completed successfully!")
    else:
        print("\n[CLIENT] Request failed.")

if __name__ == "__main__":
    main()
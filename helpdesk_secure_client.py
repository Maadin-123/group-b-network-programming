import socket

class SecureHelpdeskClient:
    def __init__(self, host='127.0.0.1', port=5001):
        self.host = host
        self.port = port
        self.TOKEN = "NET123"  # Must match server token
    
    def send_request(self, reg_number, issue):
        """Send a secure helpdesk request to the server"""
        try:
            # Create socket and connect
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            
            # Prepare message: "token|reg_number|issue"
            message = f"{self.TOKEN}|{reg_number}|{issue}"
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
    print("=" * 60)
    print(" SECURE HELPDESK CLIENT")
    print("=" * 60)
    print(f"Token: NET123 (must match server)")
    print(f"Minimum message length: 10 characters")
    print("=" * 60)
    print()
    
    # Get user input
    reg_number = input("Enter your registration number: ")
    issue = input("Describe your issue (min 10 characters): ")
    
    print("\n[CLIENT] Sending request...")
    
    # Send request
    client = SecureHelpdeskClient()
    response = client.send_request(reg_number, issue)
    
    if response and response.startswith("SUCCESS"):
        print("\n[CLIENT] ✅ Request accepted!")
    elif response:
        print("\n[CLIENT] ❌ Request rejected.")
    else:
        print("\n[CLIENT] ❌ Request failed.")

if __name__ == "__main__":
    main()
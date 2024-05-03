import socket
import json

UDP_IP = "127.0.0.1"   # IP address to bind to (localhost in this case)
UDP_PORT = 55555       # Port to bind to

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the IP address and port
sock.bind((UDP_IP, UDP_PORT))

print("UDP Receiver started...")

received_data = []

try:
    while True:
        # Receive message from the sender
        data, addr = sock.recvfrom(1024)
        
        # Decode the received message as JSON
        try:
            json_data = json.loads(data.decode('utf-8'))
            # Print the received JSON data
            print("Received JSON:", json_data)
            received_data.append(json_data)
        except json.JSONDecodeError:
            print("Received data is not in JSON format:", data.decode('utf-8'))

except KeyboardInterrupt:
    # Save received data to a file
    filename = "gnb_metrics.json"
    with open(filename, "w") as file:
        for entry in received_data:
            json.dump(entry, file)
            file.write("\n")  # Add a new line after each entry
    print(f"Received data saved to {filename}. Exiting...")
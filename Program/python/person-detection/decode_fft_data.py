import socket
import struct


buffer_size = 65536

msg_from_client = "-f 1"

bytes_to_send = str.encode(msg_from_client)

server_address_port = ("192.168.128.1", 61231)


# Create a UDP socket at client side
udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket

udp_client_socket.sendto(bytes_to_send, server_address_port)

packet = udp_client_socket.recv(buffer_size)

print(f"Total Received : {len(packet)} Bytes.")


header_length = int(struct.unpack("@f", packet[:4])[0])
ultrasonic_data_length = int(struct.unpack("@f", packet[4:8])[0])


header_data = []
for i in struct.iter_unpack("@f", packet[:header_length]):
    header_data.append(i[0])


ultrasonic_data = []
for i in struct.iter_unpack("@h", packet[header_length:]):
    ultrasonic_data.append(i[0])

print(f"Ultrasonic Data Length : {ultrasonic_data_length} Bytes")
print("Ultrasonic Data : ", ultrasonic_data)

print("Total Length ", len(header_data) + len(ultrasonic_data))
print(f"Header_Length : {header_length} Bytes.")
print("Header_Data : ", header_data)
print(f"Length of Header : {len(header_data)}")
print(f"Length of Ultrasonic Data : {len(ultrasonic_data)}")

udp_client_socket.close()

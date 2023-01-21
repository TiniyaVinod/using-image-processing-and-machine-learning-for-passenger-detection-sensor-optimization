import socket
import asyncio
import numpy as np, random, time

server_address_port = ("192.168.178.25", 61231)

buffer_size = 65536

start = time.time()
# Create a UDP socket at client side
socket_obj = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

msg_from_client = "-a 1"

bytes_to_send = str.encode(msg_from_client)

socket_obj.sendto(bytes_to_send, server_address_port)


async def get_server():
    packet = socket_obj.recv(buffer_size)
    np.save(
        f"../test_concurrency/{time.time()}_adc_{random.randint(0,1000)}.npy", packet
    )


count = 0


async def main():
    global count
    while count < 60:
        count += 1
        await get_server()


asyncio.run(main())
asyncio.run(main())


stop = time.time()

print("total time : ", stop - start)

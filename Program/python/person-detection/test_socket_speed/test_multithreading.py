import time

import numpy as np, random, time
import threading
import concurrent.futures
import asyncio, multiprocessing, threading


start = time.time()

import socket, numpy as np
server_address_port = ("192.168.178.25", 61231)
buffer_size = 65536
# Create a UDP socket at client side
socket_obj = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
msg_from_client = "-a 1"
bytes_to_send = str.encode(msg_from_client)
socket_obj.sendto(bytes_to_send, server_address_port)


def save_server_data(i):
    print(f"save server- {i} called ", time.time())
    packet = socket_obj.recv(buffer_size)
    # np.save(f'../test_concurrency/{time.time()}_adc_{random.randint(0,1000)}.npy', packet)
    print(f"save server- {i} finished  ", time.time())



# t1 = threading.Thread(target=save_server_data)
# t2 = threading.Thread(target=save_server_data)


# t1.start()
# t2.start()

# t1.join()
# t2.join()


# with concurrent.futures.ThreadPoolExecutor() as executor:
#     f1 = executor.submit(save_server_data)
#     print(f1.result())

# 4.9
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(save_server_data, list(range(10)))


# def threads_to_work():
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         results = [executor.submit(save_server_data) for _ in range(4)]

# 4.7
# for _ in range(10):
#     save_server_data(_)

# with concurrent.futures.ProcessPoolExecutor() as executor:
#     results = [executor.submit(threads_to_work) for _ in range(2)]


# concurrency with multithreading

# def multithreading_logic(sth):
#     threads = [threading.Thread(target=save_server_data, args=(i,)) for i in range(4)]
#     for thread in threads:
#         thread.start()
#     for thread in threads:
#         thread.join()


# def multiprocessing_executor():
#     with multiprocessing.Pool() as multiprocessing_pool:
#         multiprocessing_pool.map(multithreading_logic, list(range(4)))

# multiprocessing_executor()

# using aiohttp web sockets

# import asyncio
# import aiohttp

# async def main():
#     async with aiohttp.ClientSession.ws_connect('http://192.168.178.25:61231') as ws:
#         async for msg in ws:
#             if msg.type == aiohttp.WSMsgType.TEXT:
#                 if msg.data == 'close cmd':
#                     await ws.close()
#                     break
#                 else:
#                     await ws.send_str(msg.data + '/answer')
#             elif msg.type == aiohttp.WSMsgType.ERROR:
#                 break


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

# async def main():
#     task1 = loop.create_task(save_server_data())
#     task2 = loop.create_task(save_server_data())
#     task3 = loop.create_task(save_server_data())
#     task4 = loop.create_task(save_server_data())
#     task5 = loop.create_task(save_server_data())
#     task6 = loop.create_task(save_server_data())
#     await asyncio.wait([task1, task2, task3, task4, task5, task6])








# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     loop.close()



finish = time.time()
socket_obj.close()

print("Finished :", finish-start)
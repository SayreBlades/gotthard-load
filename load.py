import string
import socket
import sys
from datetime import datetime

from scapy.all import UDP
from scapy.all import IP
from scapy.all import Ether
from scapy.all import sendp
from dask.distributed import Client


def doit(i):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("127.0.0.1", 1680)
    timestamp = datetime.now().isoformat()+'Z'

    message = f'{{"rxpk":[{{"tmst":1015564868,"time":"{timestamp}","chan":1,"rfch":0,"freq":902.500000,"stat":1,"modu":"LORA","datr":"SF10BW125","codr":"4/5","lsnr":9.0,"rssi":-48,"size":23,"data":"wAIAAAAA7v/AQ3wNk1SUAgP7CNx/7WE="}}]}}'  # noqa
    try:
        # Send data
        print(f'task {i}, sending {message}')
        sock.sendto(message.encode('utf-8'), server_address)
    finally:
        print(f'task {i}, closing socket')
        sock.close()
    return f"completed {i}"

if __name__ == '__main__':
    # Process(target=sample).start()
    # Process(target=sample).start()
    client = Client()
    print(f"before map")
    doit_futs = client.map(doit, [1, 2, 3, 4, 5])
    futs_list = client.submit(",".join, doit_futs)
    print(f"after map")
    print(futs_list.result())

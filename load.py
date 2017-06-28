from scapy.all import UDP
from scapy.all import IP
from scapy.all import Ether
from scapy.all import sendp
from dask.distributed import Client
import string


def doit(i):
    print(f"inside doit {i}")
    packet = b'\x02B\xac\x11\x00\x02\x02B\xcbAR\xf2\x08\x00E\x00\x01\x10L+@\x00+\x11\xe3\xb1\x9ej\xd4\x82\xac\x11\x00\x02\xb2\x13\x06\x90\x00\xfctE\x01\x02\xd4\x00\x00\x80\x00\x00\xa0\x00\x07\xa5{"rxpk":[{"tmst":1015564868,"time":"2017-06-21T21:25:23.496577Z","chan":1,"rfch":0,"freq":902.500000,"stat":1,"modu":"LORA","datr":"SF10BW125","codr":"4/5","lsnr":9.0,"rssi":-48,"size":23,"data":"wAIAAAAA7v/AQ3wNk1SUAgP7CNx/7WE="}]}'  # noqa
    sendp(Ether() / IP(dst="52.206.193.219") / UDP(dport=1680) / packet)
    return f"completed {i}"


if __name__ == '__main__':
    # Process(target=sample).start()
    # Process(target=sample).start()
    client = Client()
    print(f"before map")
    doit_futs = client.map(doit, [1, 2])
    futs_list = client.submit(",".join, doit_futs)
    print(f"after map")
    print(futs_list.result())

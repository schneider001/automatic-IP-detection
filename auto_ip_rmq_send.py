import scapy.all as scapy
import base64
import binascii
import pika


ack_paket = ""
is_ack = 0


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet, filter="port 68", stop_filter=stopfilter)


def stopfilter(packet):
    global is_ack
    if is_ack == 1:
        return True
    else:
        return False

    
def process_sniffed_packet(packet):
    global ack_paket
    global is_ack
    pktHex = binascii.hexlify(str(packet))
    is_ack = pktHex.rfind("350105")
    if is_ack != -1:
        ack_paket = pktHex
        is_ack = 1
        

def extract_ip():
    global ack_paket
    hex_ip = ""
    ip = ""
    dns_index = ack_paket.rfind("0604")
    for i in range(4 + dns_index, 12 + dns_index, 2):
        hex_ip = hex_ip + ack_paket[i] + ack_paket[i+1] + "."
    split_hex_ip = hex_ip.split(".")
    del split_hex_ip[-1]
    for byte in split_hex_ip:
        ip = ip + str(int(byte, 16)) + "."
    ip = ip[:-1]
    return ip


def send_messege(ip):
    credentials = pika.PlainCredentials("postman", "11362266")
    parameters = pika.ConnectionParameters(ip, credentials=credentials) 
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue="hello")

    channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
    print ("[x] Sent 'Hello World!")
    connection.close()


def main():
    sniff("eth0")
    send_messege(extract_ip())


if __name__ == "__main__":
	main()
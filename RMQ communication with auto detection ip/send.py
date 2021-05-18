#!/usr/bin/python

import scapy.all as scapy
import binascii
import pika


class Sniffer(object):

    def __init__(self, interface):
        self.interface = interface
        self.ack_paket = ""
        self.is_ack = 0


    def sniff(self):
        scapy.sniff(iface=self.interface, store=False, prn=self.process_sniffed_packet, filter="port 68", stop_filter=self.stopfilter)


    def stopfilter(self, packet):
        return self.is_ack == 1

    
    def process_sniffed_packet(self, packet):
        pkt_hex = binascii.hexlify(str(packet))
        self.is_ack = pkt_hex.rfind("350105")
        if self.is_ack != -1:
            self.ack_paket = pkt_hex
            self.is_ack = 1
        

    def extract_ip(self):
        rmq_index = self.ack_paket.rfind("e104")
        
        hex_ip_row = self.ack_paket[4+rmq_index:12+rmq_index]
        split_hex_ip = map("".join, zip(*[iter(hex_ip_row)]*2))
        split_dec_ip = map(lambda byte : str(int(byte, 16)), split_hex_ip)
        dec_ip_row = ".".join(split_dec_ip)
        
        return dec_ip_row


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
    rmq_sinffer = Sniffer("eth0")
    rmq_sinffer.sniff()
    send_messege(rmq_sinffer.extract_ip())


if __name__ == "__main__":
    main()
        

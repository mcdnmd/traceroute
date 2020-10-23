import time
import socket
import random


class Tracer:
    def __init__(self, destination, hops=64):
        self.destination = destination
        self.target = None
        self.hops = hops
        self.ttl = 1
        self.current_address = None
        self.port = random.choice(range(33434, 33535))

    def find_route(self):
        self.get_server_address()
        print(f'traceroute to {self.destination} ({self.target}), '
              f'{self.hops} hops max')
        self.looper()

    def looper(self):
        while True:
            ping_array = self.send_request_to_intermediate_servers()
            self.print_route(ping_array)
            self.ttl += 1
            if self.is_a_destination():
                break

    def send_request_to_intermediate_servers(self):
        ping_array = ['*'] * 3
        for i in range(3):
            receiver = self.create_receiver()
            sender = self.create_sender()
            self.current_address, current_ping = \
                self.send_and_receive_response(
                receiver, sender)
            ping_array[i] = f'{current_ping:.3f}ms'
        return ping_array

    def create_receiver(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                             socket.IPPROTO_ICMP)
        sock.setsockopt(socket.SOL_IP, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('', self.port))
        except socket.error as e:
            raise IOError(f'Unable to bind receiver socket: {e}')
        return sock

    def create_sender(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                             socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)
        return sock

    def send_and_receive_response(self, receiver, sender):
        start_time = time.time()
        sender.sendto(b'', (self.destination, self.port))
        try:
            data, addr = receiver.recvfrom(1024)
            stop_time = (time.time() - start_time) * 1000
            return addr, stop_time
        except socket.error as e:
            raise ConnectionError(f'Socket error: {e}')
        finally:
            receiver.close()
            sender.close()

    def is_a_destination(self):
        return self.current_address[0] == self.target or self.ttl > self.hops

    def print_route(self, current_ping):
        if self.current_address:
            print(f'{self.ttl:<4} {self.current_address[0]:<4} '
                  f'{current_ping[0]:<4} {current_ping[1]:<4} '
                  f'{current_ping[2]:<4}')
        else:
            print(f'{self.ttl:<4} *')

    def get_server_address(self):
        try:
            self.target = socket.gethostbyname(self.destination)
        except Exception as e:
            raise IOError(f'Unable to resolve{self.destination}: {e}')

import socket
import time


class SocketManager:
    def __init__(self, timeout):
        self.timeout = timeout

    # TODO check how icmp sender works
    def create_sender(self, ttl, method):
        if method == 'icmp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                 socket.IPPROTO_ICMP)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                 socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        # sock.setblocking(False) - не работают
        return sock

    # TODO 1) add connection timeout
    # TODO 2) create solution to detect only self socket packs
    def create_receiver(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                             socket.IPPROTO_ICMP)
        sock.setsockopt(socket.SOL_IP, socket.SO_REUSEADDR, 1)
        sock.settimeout(self.timeout)
        # sock.setblocking(False) - не работают
        try:
            sock.bind(('', port))
        except socket.error as e:
            raise IOError(f'Unable to bind receiver socket: {e}')
        return sock

    @staticmethod
    def send_message(sender, dest, port):
        try:
            sender.sendto(b'', (dest, port))
        except socket.error as e:
            raise ConnectionError(f'Socket error while send MSG: {e}')
        finally:
            sender.close()

    @staticmethod
    def receive_message(receiver):
        try:
            data, addr = receiver.recvfrom(1024)
            stop_time = time.time()
            return addr, stop_time
        except socket.timeout as e:
            return -1, -1
        except socket.error as e:
            raise ConnectionError(f'Socket error while receive MSG: {e}')
        finally:
            receiver.close()

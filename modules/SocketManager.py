import socket
import time


class SocketManager:
    @staticmethod
    def create_sender(ttl):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                             socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        return sock

    # TODO 1) add connection timeout
    # TODO 2) create solution to detect only your socket packets!
    @staticmethod
    def create_receiver(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                             socket.IPPROTO_ICMP)
        sock.setsockopt(socket.SOL_IP, socket.SO_REUSEADDR, 1)
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
        except socket.error as e:
            raise ConnectionError(f'Socket error while receive MSG: {e}')
        finally:
            receiver.close()

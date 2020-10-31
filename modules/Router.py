import socket
import time

from modules.SocketManager import SocketManager
from modules.TerminalWriter import TerminalWriter


class Router:
    def __init__(self, traceroute):
        self.traceroute = traceroute
        self.sockmanager = SocketManager()
        self.terminal_writer = TerminalWriter(self.traceroute.ttl)

    def start(self):
        self.terminal_writer.add_start_line(self.traceroute.dest,
                                            self.traceroute.ttl,
                                            self.traceroute.max_hops)
        self.terminal_writer.print_buffer()
        while True:
            addr = self.make_request_to_intermediate_server()
            self.terminal_writer.print_buffer()
            self.traceroute.ttl += 1
            if self.traceroute.is_a_destination(addr):
                break

    # TODO add UDP, ICMP separation
    def make_request_to_intermediate_server(self):
        current_addr = None
        for i in range(self.traceroute.pack_per_hop):
            receiver = self.sockmanager.create_receiver(self.traceroute.port)
            sender = self.sockmanager.create_sender(self.traceroute.ttl,
                                                    self.traceroute.method)

            start_time = time.time()

            self.sockmanager.send_message(sender, self.traceroute.dest,
                                          self.traceroute.port)

            current_addr, end_time = self.sockmanager.receive_message(receiver)

            ping = (end_time - start_time) * 1000

            self.terminal_writer.add_info_from_intermediate_server(
                self.traceroute.ttl, current_addr[0], ping)
        return current_addr

    def get_server_address(self):
        try:
            self.traceroute.target = socket.gethostbyname(self.traceroute.dest)
        except Exception as e:
            raise IOError(f'Unable to resolve{self.traceroute.dest}:'
                          f' {e}')

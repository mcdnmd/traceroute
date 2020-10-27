from modules.Router import Router


class Traceroute:
    def __init__(self, dest, max_hops, icmp_echo, method, port, timeout,
                 pack_num, ttl):
        self.dest = dest
        self.max_hops = max_hops
        self.icmp_echo = icmp_echo
        self.method = method
        self.port = port
        self.timeout = timeout
        self.pack_per_hop = pack_num
        self.ttl = ttl
        self.target = None
        self.current_address = None
        self.Router = Router(self)

    def find_route(self):
        self.Router.start()

    def is_a_destination(self, addr):
        return addr == self.target or self.ttl > self.max_hops


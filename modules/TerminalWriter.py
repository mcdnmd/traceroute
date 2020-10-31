class TerminalWriter:
    def __init__(self, ttl):
        self.buffer = ''
        self.last_ttl = ttl
        self.last_ip_address = None

    def clear_buffer(self):
        self.buffer = ''

    def add_start_line(self, dest, target, max_hops):
        self.buffer += f'traceroute to {dest} ({target}), {max_hops} hops max'

    def add_info_from_intermediate_server(self, ttl, addr, ping):
        if self.last_ip_address is None or self.last_ttl < ttl:
            self.last_ip_address = addr
            self.last_ttl = ttl
            self.buffer = f'{ttl:<4} {addr:<4} {ping:.3f}ms '
        else:
            self.buffer += f'{ping:.3f}ms '

    def add_text(self, text):
        self.buffer += f'{text} '
    def print_buffer(self):
        print(self.buffer)
        self.clear_buffer()

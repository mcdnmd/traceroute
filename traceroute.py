import argparse
from modules.Traceroute import Traceroute


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('destination', action='store',
                        help='domain name or IP-address')
    parser.add_argument('-f', '--first-hop', type=int, action='store',
                        default=1,  dest='ttl',
                        help='set initial hop distance, i.e., time-to-live '
                             '(default: 1)')
    parser.add_argument('-I', '--icmp', action='store_true', dest='icmp_echo',
                        default=False, help='use ICMP ECHO as probe')
    parser.add_argument('-m', '--max-hop', type=int, action='store',
                        dest='max_hops',
                        default=64, help='Maximum number of hops')
    parser.add_argument('-M', '--method', action='store', type=str,
                        dest='method', default="udp",
                        help='use METHOD ("icmp" or "udp") for traceroute '
                             'perations, ' \
                             'defaulting to `udp')
    parser.add_argument('-p', '--port', action='store', type=int, dest='port',
                        default=33434,
                        help='use destination PORT port (default: 33434)')
    parser.add_argument('-q', '--tries', action='store', type=int,
                        dest='packet_number', default=3,
                        help='send NUM probe packets per hop (default: 3)')
    parser.add_argument('-w', '--wait', action='store', type=int,
                        dest='timeout', default=3,
                        help='wait NUM seconds for response (default: 3)')

    args = parser.parse_args()
    launch(args)


def launch(args):
    dest = args.destination
    hops = args.max_hops
    icmp_echo = args.icmp_echo
    method = args.method
    port = args.port
    timeout = args.timeout
    pack_num = args.packet_number
    ttl = args.ttl

    tracer = Traceroute(dest, hops, icmp_echo, method, port, timeout, pack_num,
                        ttl)
    tracer.find_route()


if __name__ == '__main__':
    main()

import argparse
from modules.Tracer import Tracer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'destination',
        action='store',
        help='domain name or IP-address')
    parser.add_argument(
        '-hops',
        type=int,
        action='store',
        default=64,
        help='Maximum number of hops'
    )
    args = parser.parse_args()

    tracer = Tracer(args.destination, args.hops)
    tracer.find_route()


if __name__ == '__main__':
    main()

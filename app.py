from multiprocessing.pool import ThreadPool

import socket
import argparse


def test(proxy, timeout=2):
    ip, port = proxy.split(':')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, int(port)))

    valid = result == 0
    print '%s\t%s' % (proxy.strip(), 'OK' if valid else 'FAIL')
    if valid:
        return proxy
    return None


def validate(proxies, concurrency=16):
    pool = ThreadPool(concurrency)
    ret = pool.map(test, proxies)

    return filter(lambda x: x is not None, ret)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for proxy testing')
    parser.add_argument('proxy_file', type=str,
                        help='file containing proxies, one per line. eg.: 127.0.0.1:1087')
    parser.add_argument('output', type=str,
                        help='output file')
    parser.add_argument('--concurrency', metavar='N', help='concurrency. default=16', type=int, default=16)
    args = parser.parse_args()

    with open(args.proxy_file) as f:
        proxies = map(str.strip, f.readlines())
    valid_proxies = validate(proxies, args.concurrency)

    with open(args.output, 'w') as of:
        of.write('\n'.join(valid_proxies))

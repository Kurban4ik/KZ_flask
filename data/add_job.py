import argparse

parser = argparse.ArgumentParser()
parser.add_argument("bb", nargs='*', default=[], type=str, help='List of IPs')
parser.add_argument('--sort', action='store_true')
args = parser.parse_args()
dictt = {}

for i in args.bb:
    a, b = i.split('=')
    dictt[a] = b

for i in (sorted(dictt.keys()) if args.sort else dictt.keys()):
    print('Key:', i, '\t', 'Value:', dictt[i])

from sys import path
path.append('..')
from sys import argv
from Litterfinger import Receiver

if __name__ == '__main__':
	host, subs = argv[1:]
	r = Receiver(subs, host)
	for i in r:
		print i
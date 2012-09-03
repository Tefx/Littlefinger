from sys import path
path.append('..')
from sys import argv
from Litterfinger import Receiver

def obj2str(d):
	return "\"%s\"" % ", ".join(["%s: %s" % i for i in d.items()])

if __name__ == '__main__':
	host, subs = argv[1:]
	r = Receiver(subs, host)
	for i in r:
		print obj2str(i)
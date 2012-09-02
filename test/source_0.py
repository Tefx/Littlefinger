from sys import path
path.append('..')
from sys import argv
from Litterfinger import Source
from Litterfinger.tools import const, rand, gen_auto_iter

if __name__ == '__main__':
	host = argv[1]
	config = {"name":	const("cam0"),
			  "x":		rand(0,5),
			  "y":		rand(0,7),
			  "_delta":	rand(0.3,1)}
	a = gen_auto_iter(config)

	s = Source(host)

	for i in a:
		print i
		s.send(i)
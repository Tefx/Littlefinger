from sys import path
path.append('..')
from sys import argv
from Litterfinger import Source
from Litterfinger.tools import const, rand, gen_auto_iter, choice
import time

def obj2str(d):
	return "\"%s\"" % ", ".join(["%s: %s" % i for i in d.items()])

if __name__ == '__main__':
	host = argv[1]
	config = {"city":		const("nanjing"),
			  "temp":		rand(20,35),
			  "weather":	choice(["sun", "rain", "cloud", "snow"]),
			  "_delta":		rand(1,3)}
	a = gen_auto_iter(config)

	s = Source(host)

	for i in a:
		t = time.strftime("%X", time.localtime(time.time()))
		print "[%s (%s)]: %s" % (t, __file__.split(".")[0], obj2str(i))
		s.send(i)
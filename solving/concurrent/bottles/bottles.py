#! /usr/bin/env python
import sys
from time import time

from sensors import Weight, Volume, Acid

def main(args):
	ti = time()
	bottles = 8 if len(args) < 2 else args[1]
	for b in range(bottles):
		if b%2 == 0: a = Acid(); a.start(); a.join()
		w,v = Weight(),Volume()
		w.start()
		v.start()
		w.join()
		v.join()
	tf = time()-ti
	info('Tempo de execucao: %ss' % tf)
	info('Valvulas desativadas')
	info('Sistema encerrado')

if __name__ == '__main__':
	main(sys.argv)

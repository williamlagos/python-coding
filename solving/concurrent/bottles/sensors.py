from threading import Thread,Semaphore
from time import sleep
from logging import log,INFO
from logging import basicConfig as start_log

# from valves import *

start_log(filename='messages.log',level=INFO)

def info(message):
	log(INFO,message)
	print(message)
	print('\nValvula Volume: %i' % valve_vol)
	print('\nValvula Peso: %i' % valve_wei)
	print('\nValvula Acido: %i' % valve_pha)
	print('\nTrava de garrafa: %i' % bottle_lk)

valve_vol = False
valve_wei = False
valve_pha = False
bottle_lk = False

volume = Semaphore()
weight = Semaphore()
phacid = Semaphore()
btlock = Semaphore()

class Acid(Thread):
	def __init__(self):
		self.pha = 0
		Thread.__init__(self)
	def run(self):
		global valve_vol
		global valve_pha
		info('Acidez no tanque detectada')
		volume.acquire()
		valve_vol = False
		volume.release()
		info('Valvula de controle de PH ativada')
		valve_pha = True
		for i in range(5): 
			self.pha += 1
			info('Mais 1mL de estabilizador para o tanque')
			sleep(1)
		info('Acidez no tanque resolvida')
		volume.acquire()
		valve_vol = True
		volume.release()
		info('Valvula de controle de PH desativada')
		valve_pha = False

class Bottle(Thread):
	def run(self):
		global bottle_lk
		info('Nova garrafa no colocador de garrafas')
		info('Trava de garrafas ativada')
		bottle_lk = True
		sleep(2)
		info('Garrafa liberada para distribuicao')
		bottle_lk = False
		
class Weight(Thread):
	def __init__(self):
		self.weight = 0
		Thread.__init__(self)
	def run(self):
		global valve_vol
		global valve_wei
		info('Valvula de volume desligada')
		volume.acquire()
		valve_vol = False
		volume.release()
		info('Nova garrafa na balanca')
		weight.acquire()
		valve_weight = False
		weight.release()
		info('Valvula de peso desativada')
		for i in range(10): 
			self.weight += 10
			info('Mais 10g para a garrafa')
			sleep(1)
		b = Bottle()
		b.start()
		b.join()

class Volume(Thread):
	def __init__(self):
		self.volume = 100
		Thread.__init__(self)
	def run(self):
		global valve_vol
		global valve_wei
		info('Valvula de peso ativada')
		weight.acquire()
		valve_weight = True
		weight.release()
		info('Tanque sendo preenchido')
		volume.acquire()
		valve_vol = True
		volume.release()
		info('Valvula de volume ativada')
		for i in range(10):
			self.volume -= 10
			info('Menos 10mL para o tanque')
			sleep(1)

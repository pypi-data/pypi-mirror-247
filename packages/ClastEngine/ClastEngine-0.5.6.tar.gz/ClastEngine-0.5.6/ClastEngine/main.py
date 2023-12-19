''' PEP-8 '''

# Import standart libraries
import random
import time
import os
import logging
import keyboard

logging.basicConfig(level=logging.INFO, filename="clastengine.log",filemode="w")
logging.debug('ClastEngine started!')

# Main class
class Engine:
	def __init__(self): # Initialization
		logging.debug('ClastEngine started!')

	def draw(weight=5, height=5, pos=0):
		logging.info(f'Drawed {weight}x{height} | Position: {pos}; Mode: Default\n\n')
		weighto = weight * 2
		weighto -= 2
		pos = ' ' * pos
		weighto = ' ' * weighto
		weighta = '* ' * (weight + 1)
		print(f'{pos}{weighta}')
		for i in range(height + 1):
			if i < height:
				print(f'{pos}* {weighto}*')
				i += 1
			elif i == height:
				print(f'{pos}* {weighto}*')
				break
		print(f'{pos}{weighta}')

	def dual_draw(w1=5, h1=5, pos1=0, pos2=1):
		logging.info(f'Drawed {w1}x{h1} | Position: {pos1},{pos2}; Mode: Dual\n\n')
		w2 = w1
		h2 = h1
		weighto1 = w1 * 2
		weighto2 = w2 * 2
		weighto1 -= 2
		weighto2 -= 2
		pos1 = ' ' * pos1
		pos2 = ' ' * pos2
		weighto1 = ' ' * weighto1
		weighto2 = ' ' * weighto2
		weighta1 = '* ' * (w1 + 1)
		weighta2 = '* ' * (w2 + 1)
		print(f'{pos1}{weighta1}{pos2}{weighta2}')
		for i in range(h1 + 1):
			if i < h1:
				print(f'{pos1}* {weighto1}*{pos2} *{weighto2} *')
				i += 1
			elif i == h1:
				print(f'{pos1}* {weighto1}*{pos2} *{weighto2} *')
				break
		print(f'{pos1}{weighta1}{pos2}{weighta2}')


	def edit(uptime):
		time.sleep(uptime)
		os.system('cls' if os.name=='nt' else 'clear')
		logging.info((f'Updated | Uptime: {uptime}\n\n'))

	def infobar():
		fps = 60
		debug = True
		print(f'Frames per second: {fps}\nEngine version: 0.5.5\nDebug: {debug}\n\n\n')
		logging.info(f'Drawed infobar | Debug: True\n\n')

	def key(key, function):
		if keyboard.is_pressed(key):
			logging.info(f'Activated function {function} | Key: {key}')
			function()
		
	def draw_template(text: str, pos1, pos2):
		pos2_n = ' ' * pos2
		text = text.replace('\n', f'\n{pos2_n}')
		text = (pos1 * '\n') + pos2_n + text
		pos1_n = '\n' * pos1
		print(text)



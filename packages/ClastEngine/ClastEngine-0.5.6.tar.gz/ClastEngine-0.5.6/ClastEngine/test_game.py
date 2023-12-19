from ClastEngine.main import Engine
import keyboard
import time


distance = 5
ots = 5
print('PRESS W TO START')
a = '----------\n----------\n----------'
template = '    (¯`°v°´¯)\n     (_.^._)'

while True:
	try:
		
		if keyboard.is_pressed('w'):
			Engine.edit(0.01)
			Engine.infobar()
			Engine.draw_template(template, distance, ots)

			distance -= 1

		
		if keyboard.is_pressed('s'):
			Engine.edit(0.01)
			Engine.infobar()
			Engine.draw_template(template, distance, ots)
	
			distance += 1
		
		if keyboard.is_pressed('a'):
			Engine.edit(0.01)
			Engine.infobar()
			Engine.draw_template(template, distance, ots)
		
			ots -= 1
		
		if keyboard.is_pressed('d'):
			Engine.edit(0.01)
			Engine.infobar()
			Engine.draw_template(template, distance, ots)
	
			ots += 1
		
		if keyboard.is_pressed('q'):
			exit()

	except Exception as e:
		raise e


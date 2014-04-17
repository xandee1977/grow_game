#! /usr/bin/python
'''
tetris.py

starts the game
'''

if __name__ == "__main__":
	from traceback_plus import print_exc_plus
	import debug
	try:
		from main import main
		main()
	except:
		print_exc_plus(File = debug.log)

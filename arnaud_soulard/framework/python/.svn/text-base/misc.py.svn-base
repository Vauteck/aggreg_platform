#! /usr/bin/python
# -*- coding: utf-8 -*-

# import python libraries
#import os
import time

# import aggregation-platform's libraries
import globals
import utils



	#print ("init...")

	# curses.wrapper : terminal handler for curses programs
	##curses.wrapper(restoreTerminal)

	# starting a curses application
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(1)

	curses.init_pair(1, 1, curses.COLOR_BLACK)
	stdscr.addstr(0, 5, "Current mode: Typing mode", curses.A_REVERSE)

	# terminating a curses application
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()

	##stdscr.clear()
	#i = curses.COLOR_CYAN
	#curses.init_pair(i, curses.COLOR_BLUE, curses.COLOR_BLACK)
	#stdscr.addstr("COLOR %d! " % i, curses.color_pair(i))
	#stdscr.addstr(0, 5, "Current mode: Typing mode", curses.A_REVERSE)
'''
	if curses.has_colors():
		#for i in range(1, curses.COLORS):
		curses.init_pair(1, 1, curses.COLOR_BLACK)
		stdscr.addstr("C'est bon", curses.color_pair(curses.COLOR_GREEN))
			#stdscr.addstr("COLOR %d! " % i, curses.color_pair(i))
			#stdscr.addstr("BOLD! ", curses.color_pair(i) | curses.A_BOLD)
			#stdscr.addstr("STANDOUT! ", curses.color_pair(i) | curses.A_STANDOUT)
			#stdscr.addstr("UNDERLINE! ", curses.color_pair(i) | curses.A_UNDERLINE)
			#stdscr.addstr("BLINK! ", curses.color_pair(i) | curses.A_BLINK)
			#stdscr.addstr("DIM! ", curses.color_pair(i) | curses.A_DIM)
			#stdscr.addstr("REVERSE! ", curses.color_pair(i) | curses.A_REVERSE)
'''
	#stdscr.refresh()
#	sleep(2)
	#stdscr.getch()



import curses

'''
curses.A_ALTCHARSET
curses.A_BLINK
curses.A_BOLD
curses.A_DIM
curses.A_NORMAL
curses.A_REVERSE
curses.A_STANDOUT
curses.A_UNDERLINE

curses.COLOR_BLACK
curses.COLOR_BLUE
curses.COLOR_CYAN
curses.COLOR_GREEN
curses.COLOR_MAGENTA
curses.COLOR_RED
curses.COLOR_WHITE
curses.COLOR_YELLOW
'''

class Window(object):

	def __init__(self, screen):
		self.screen = screen
		self.height, self.width = self.screen.getmaxyx()
		self.screen.nodelay(1)

	def redraw(self):
		self.screen.clear()
		self.screen.addstr(0, 0, 'hai')
		self.screen.addstr(0, 0, 'aaa')
		self.screen.refresh()

	def main(self):
		while 1:
			key = self.screen.getch()
			if key == ord('q'):
					break
			self.redraw()

	def display(self, string, color, x=0, y=0):
		self.addstr(0, 20, string, color)
		# un nouvel attribut de l'instance
		#self.y = 12
		# l'attribut de la classe
		##print (Dmng.x, self.y)

'''
	def __init__(self):
		# starting a curses application
		self = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.keypad(1)
		#self.start_color()

		#create a color and associate it with an integer identifier:
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

		#retrieve the color using the integer identifier:
		green = curses.color_pair(1)
		# initialisation de l'attribut d'instance x
		#self.x = n
'''

'''
if __name__ == '__main__':

	globals.scriptStartTime = time.time()
	myText = Window()
	#myText.display('aaa', green)

	# terminating a curses application
	curses.nocbreak()
	myText.keypad(0)
	curses.echo()
	curses.endwin()
'''


def main(stdscr):
	myWindow = Window(stdscr)
	myWindow.main()
	#myWindow.screen.addstr(0, 0, 'aaaa')

if __name__ == '__main__':
	globals.scriptStartTime = time.time()
	try:
		curses.wrapper(main)
	except KeyboardInterrupt:
		pass




	#print ("init...")

	# curses.wrapper : terminal handler for curses programs
	##curses.wrapper(restoreTerminal)

'''
	# starting a curses application
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(1)

	curses.init_pair(1, 1, curses.COLOR_BLACK)
	stdscr.addstr(0, 5, "Current mode: Typing mode", curses.A_REVERSE)



	##stdscr.clear()
	#i = curses.COLOR_CYAN
	#curses.init_pair(i, curses.COLOR_BLUE, curses.COLOR_BLACK)
	#stdscr.addstr("COLOR %d! " % i, curses.color_pair(i))
	#stdscr.addstr(0, 5, "Current mode: Typing mode", curses.A_REVERSE)
'''
'''
	if curses.has_colors():
		#for i in range(1, curses.COLORS):
		curses.init_pair(1, 1, curses.COLOR_BLACK)
		stdscr.addstr("C'est bon", curses.color_pair(curses.COLOR_GREEN))
			#stdscr.addstr("COLOR %d! " % i, curses.color_pair(i))
			#stdscr.addstr("BOLD! ", curses.color_pair(i) | curses.A_BOLD)
			#stdscr.addstr("STANDOUT! ", curses.color_pair(i) | curses.A_STANDOUT)
			#stdscr.addstr("UNDERLINE! ", curses.color_pair(i) | curses.A_UNDERLINE)
			#stdscr.addstr("BLINK! ", curses.color_pair(i) | curses.A_BLINK)
			#stdscr.addstr("DIM! ", curses.color_pair(i) | curses.A_DIM)
			#stdscr.addstr("REVERSE! ", curses.color_pair(i) | curses.A_REVERSE)
'''
	#stdscr.refresh()
#	time.sleep(2)
	#stdscr.getch()





'''
def my_program(stdscr):
	#create a color and associate it with an integer identifier:
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    #retrieve the color using the integer identifier:
    green = curses.color_pair(1)

    #insert text on screen using the color:
    stdscr.addstr(0, 20, "WELCOME TO MY PROGRAM", green)

    #move cursor elsewhere:
    stdscr.move(20, 0)

    #update screen with the changes:
    stdscr.refresh()

    stdscr.getch()

curses.wrapper(my_program)
#Handles the initialization of a new terminal window
#and returns window operation back to normal behavior
#when the program finishes
'''



'''
begin_x = 20 ; begin_y = 7
height = 5 ; width = 40
win = curses.newwin(height, width, begin_y, begin_x)
'''

'''
pad = curses.newpad(100, 100)
#  These loops fill the pad with letters; this is
# explained in the next section
for y in range(0, 100):
    for x in range(0, 100):
        try: pad.addch(y,x, ord('a') + (x*x+y*y) % 26 )
        except curses.error: pass

#  Displays a section of the pad in the middle of the screen
pad.refresh( 0,0, 5,5, 20,75)
'''
'''
stdscr.addstr(0, 5, "Current mode: Typing mode", curses.A_REVERSE)
#stdscr.start_color()
#stdscr.addstr(0, 0, "RED ALERT!", curses.color_pair(1) )
stdscr.refresh()

time.sleep(2)

#print (curses.baudrate())
#print (curses.can_change_color())
#curses.beep()

#curses.nocbreak(); stdscr.keypad(0); curses.echo()
'''


##def restoreTerminal(stdscr):
##	curses.endwin()

'''
import curses

# initialize curses
stdscr = curses.initscr()
curses.start_color()

# initialize color #1 to Blue with Cyan background
curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)

stdscr.addstr('A sword and a shield.', curses.color_pair(1))
stdscr.refresh()

# finalize curses
curses.endwin()
'''


#import sys

# for data compression
#import zlib

#print sys.argv[0]

'''
while True:
	try:
		x = int(input("Please enter a number: "))
		break
	except ValueError:
		print("Oops!  That was no valid number.  Try again...")
		sys.exit(1)
'''

#print(sys.argv)
'''
now = date.today()
now
'''

#self.__logger.info('[CHECKPOINT] %s' , Helpers.get_my_name())
#logger.info('[START] main')


#export PYTHONPATH=`pwd`


'''
class TestSequenceFunctions(unittest.TestCase):

	# setUp : the test runner will run that method before each test
	def setUp(self):
		self.seq = list(range(10))

	# tearDown : the test runner will run that method after each test
	def tearDown(self):
		self.seq = list(range(10))

	def test_shuffle(self):
		# make sure the shuffled sequence does not lose any elements
		random.shuffle(self.seq)
		self.seq.sort()
		self.assertEqual(self.seq, list(range(10)))

	# should raise an exception for an immutable sequence
		self.assertRaises(TypeError, random.shuffle, (1,2,3))

	def test_choice(self):
		element = random.choice(self.seq)
		self.assertTrue(element in self.seq)

	def test_sample(self):
		with self.assertRaises(ValueError):
			random.sample(self.seq, 20)
		for element in random.sample(self.seq, 5):
			self.assertTrue(element in self.seq)
'''
#if __name__ == '__main__':
#	unittest.main()

# Other way to run the tests with a finer level of control
#suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
#unittest.TextTestRunner(verbosity=2).run(suite)

#python -m unittest test_module1 test_module2

'''
bandwidthTestSuite = unittest.TestSuite()
bandwidthTestSuite.addTest(TestSequenceFunctions('test_shuffle'))
bandwidthTestSuite.addTest(TestSequenceFunctions('test_choice'))
unittest.TextTestRunner(verbosity=2).run(bandwidthTestSuite)
#return bandwidthTestSuite
'''




'''
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
'''

#o1 = dmng.Dmng(10)


'''
begin_x = 20 ; begin_y = 7
height = 5 ; width = 40
win = curses.newwin(height, width, begin_y, begin_x)
'''

'''
pad = curses.newpad(100, 100)
#  These loops fill the pad with letters; this is
# explained in the next section
for y in range(0, 100):
    for x in range(0, 100):
        try: pad.addch(y,x, ord('a') + (x*x+y*y) % 26 )
        except curses.error: pass

#  Displays a section of the pad in the middle of the screen
pad.refresh( 0,0, 5,5, 20,75)
'''
'''
stdscr.addstr(0, 5, "Current mode: Typing mode", curses.A_REVERSE)
#stdscr.start_color()
#stdscr.addstr(0, 0, "RED ALERT!", curses.color_pair(1) )
stdscr.refresh()

time.sleep(2)

#print (curses.baudrate())
#print (curses.can_change_color())
#curses.beep()

#curses.nocbreak(); stdscr.keypad(0); curses.echo()
'''


def restoreTerminal(stdscr):
	curses.endwin()

'''
curses.A_ALTCHARSET
curses.A_BLINK
curses.A_BOLD
curses.A_DIM
curses.A_NORMAL
curses.A_REVERSE
curses.A_STANDOUT
curses.A_UNDERLINE

curses.COLOR_BLACK
curses.COLOR_BLUE
curses.COLOR_CYAN
curses.COLOR_GREEN
curses.COLOR_MAGENTA
curses.COLOR_RED
curses.COLOR_WHITE
curses.COLOR_YELLOW
'''










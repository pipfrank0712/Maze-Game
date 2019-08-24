## setup the maze
import turtle
import math
import random

wn = turtle.Screen()
wn.bgcolor("white")
wn.title("A Maze Game")
wn.setup(700, 700)
wn.update()
#Turn off screen updates to speed up the game, stop screen animation completely
wn.tracer(0)

# register shapes
turtle.register_shape("tt2.gif")
turtle.register_shape("hll.gif")
turtle.register_shape("hlr.gif")
turtle.register_shape("heart.gif")
turtle.register_shape("tree.gif")
turtle.register_shape("enemy2.gif")
turtle.register_shape("paw.gif")


def create_text(pos, txt):   ####print text on the screen
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("black")
    pen.penup()
    pen.setposition(pos)
    pen.write(txt, False, align="center", font= ("Arial", 60, "bold"))
    pen.hideturtle()
    return pen

#create Pen
class Pen(turtle.Turtle):   #CT: "Class defines an object. In this case, it defines an object Pen. 
## Pen is a child of turtle module turtle class. 
## Pen is a turtle, it can do anything turtle can do. Class is not an object.""
	def __init__(self):     # initialize. self refers to the object.
		turtle.Turtle.__init__(self)  # initialize class as well. ** has other way to do this
		self.shape("square")
		self.color("white")
		self.penup()
		self.speed(0)
## with the defined class, we can create class instance. In this case, it will be a white square.


class Player(turtle.Turtle):
	def __init__(self):     # initialize. self refers to the object.
		turtle.Turtle.__init__(self)  # initialize class as well. ** has other way to do this
		self.shape("hlr.gif")
		self.color("blue")
		self.penup()
		self.speed(0)
		self.gold = 0
		# define player movement
	def go_up (self):
		#calculate coordinate move into
		move_to_x = self.xcor()
		move_to_y = self.ycor() + 24
		# check if that in wall list
		if (move_to_x, move_to_y) not in walls:
			self.goto(move_to_x, move_to_y)
	def go_down (self):
		#calculate coordinate move into
		move_to_x = self.xcor()
		move_to_y = self.ycor() - 24
		# check if that in wall list
		if (move_to_x, move_to_y) not in walls:
			self.goto(move_to_x, move_to_y)
	def go_left (self):
		#calculate coordinate move into
		move_to_x = self.xcor() - 24
		move_to_y = self.ycor()
		self.shape("hll.gif")
		# check if that in wall list
		if (move_to_x, move_to_y) not in walls:
			self.goto(move_to_x, move_to_y)
	def go_right (self):
		#calculate coordinate move into
		move_to_x = self.xcor() + 24
		move_to_y = self.ycor()
		self.shape("hlr.gif")
		# check if that in wall list
		if (move_to_x, move_to_y) not in walls:
			self.goto(move_to_x, move_to_y)
		#define collision between player and treasures
	def is_collision(self, other):    #other means treasures.
		a = self.xcor() - other.xcor()
		b = self.ycor() - other.ycor()
		distance = math.sqrt(a ** 2 + b ** 2)

		if distance < 5:
			self.shape("tt2.gif")			
			return True
		else:
			# self.shape("hlr.gif")			
			return False
		turtle.ontimer(self.is_collision, t = 1000000)

#Create treasure class
class Treasure(turtle.Turtle):
	def __init__(self, x, y):     # introducing x and y for setting treasure location
		turtle.Turtle.__init__(self)  
		self.shape("heart.gif")
		self.color("yellow")
		self.penup()
		self.speed(0)
		self.gold = 100  # set the value of gold for this treasure
		self.goto(x, y)

	def destroy(self):
		self.goto(2000,2000)
# ###########################################################
# ###########################################################
#Create bullet class
pawstate = "ready"
class Paw(turtle.Turtle):
	def __init__(self):    
		turtle.Turtle.__init__(self)  
		self.shape("paw.gif")
		self.color("yellow")
		self.penup()
		self.speed(0)
		self.hideturtle()
	def fire_up(self):
		global pawstate
		if pawstate == "ready":
			pawstate = "fire"
			self.goto(player.xcor(), player.ycor() + 24)			
			if (player.xcor(), player.ycor() + 24) not in walls:
				self.showturtle()
			else:
				pawstate = "ready"
	def fire_down(self):
		global pawstate
		if pawstate == "ready":
			pawstate = "fire"
			self.goto(player.xcor(), player.ycor() - 24)
			if (player.xcor(), player.ycor() - 24) not in walls:				
				self.showturtle()
			else:
				pawstate = "ready"
	def fire_left(self):
		global pawstate
		if pawstate == "ready":
			pawstate = "fire"
			self.goto(player.xcor() - 24, player.ycor())
			if (player.xcor() - 24, player.ycor()) not in walls:				
				self.showturtle()	
			else:
				pawstate = "ready"		
	def fire_right(self):
		global pawstate
		if pawstate == "ready":
			pawstate = "fire"
			self.goto(player.xcor() + 24, player.ycor())
			if (player.xcor() + 24, player.ycor()) not in walls:				
				self.showturtle()
			else:
				pawstate = "ready"
	def move(self):
		global pawstate
		if self.xcor() > player.xcor():
			x = self.xcor() + 6
			y = self.ycor() + 0
		elif self.xcor() < player.xcor():
			x = self.xcor() - 6
			y = self.ycor() + 0			
		elif self.ycor() < player.ycor():
			x = self.xcor()
			y = self.ycor() - 6
		elif self.ycor() > player.ycor():
			x = self.xcor()
			y = self.ycor() + 6

		if (x,y) not in walls:
			# turtle.ontimer(self.move, t = 10)
			self.goto(x,y)
			for enemy in enemies:
				if self.is_collision(enemy):
					enemy.destroy()
					player.gold += enemy.gold
					score_pen.clear()
					scorestring = "player gold: %s" %player.gold   ###########fill in the score
					score_pen.write(scorestring, False, align="center", font= ("Arial", 24, "normal"))	
					pawstate = "ready"			
		else:
			self.hideturtle()
			pawstate = "ready"

	def is_collision(self, other):    #other means treasures.
		a = self.xcor() - other.xcor()
		b = self.ycor() - other.ycor()
		distance = math.sqrt(a ** 2 + b ** 2)

		if distance < 5:
			return True
		else:
			return False

	# def move(self):
	# 	x = self.xcor() + dx
	# 	y = self.ycor() + dy
	# 	self.goto(x,y)
	# 	turtle.ontimer(self.move, t = 100)


#Create enemy
class Enemy(turtle.Turtle):
	def __init__(self, x, y):     # introducing x and y for setting treasure location
		turtle.Turtle.__init__(self)  
		self.shape("enemy2.gif")
		self.color("red")
		self.penup()
		self.speed(0)
		self.gold = 25  # set the value for kill a enemy
		self.goto(x, y)
		self.direction = random.choice(["up", "down", "left", "right"])  #setting direction with random module.
		# randonly select from choice list
	def move(self):
		if self.direction == "up":
			dx = 0
			dy = 24
		elif self.direction == "down":   # different between if/if and if/elif
			dx = 0
			dy = -24
		elif self.direction == "left":
			dx = -24
			dy = 0
		elif self.direction == "right":
			dx = 24
			dy = 0
		else:
			dx = 0
			dy = 0

		#when close to the player, start tracking the player
		if self.is_close(player):
			if self.xcor() > player.xcor():    ##without using elif here, enemy can go dianglely.
				self.direction = "left"
			elif self.xcor() < player.xcor():
				self.direction = "right"
			elif self.ycor() > player.ycor():
				self.direction = "down"
			elif self.ycor() > player.ycor():
				self.direction = "up"

		# coordinate move to, in order to check boundary
		move_to_x = self.xcor() + dx
		move_to_y = self.ycor() + dy

		# check boundary
		if (move_to_x, move_to_y) not in walls:
			self.goto(move_to_x, move_to_y)
		else:
			self.direction = random.choice(["up", "down", "left", "right"])  
		# use ontimer module to slow down the move of enemys. Otherwise, the enemys will move as fast as the player.
		turtle.ontimer(self.move, t = random.randint(300, 500))  # adding some randomization on enemy's moving speed.
		# turtle.ontimer(self.move, t = 200)
		# timer only work once. need to be reset for every time throught the move.

		#check enemy is close to player or not
	def is_close(self, other):
		a = self.xcor() - other.xcor()
		b = self.ycor() - other.ycor()
		distance = math.sqrt(a ** 2 + b ** 2)
		if distance < 100:
			return True
		else:
			return False

	def destroy(self):
		self.goto(2000,2000)
		self.hideturtle()

# Create level list
levels = [""]   ### align the index in the list with #level 

#Defince first level
level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XXP  T          XXXT  XXX",
"XXXX   XXXXX  E XXX   XXX",
"XXXX    XXXXXXXXXXX   XXX",
"XXXXX                  XX",
"XXXXXXXXXXXXXX   XXX  XXX",
"XXX E          XXXXXX  XX",
"XT XX   XXXX    XX  XX  X",
"X  XXX  XXXXX  XXX  XXXXX",
"X  XXX   XXXX       X  XX",
"X       XX     XXXXXX  XX",
"X   XX   XXXX          XX",
"X    XXXXXXX   XXXXXXE XX",
"XXX  X  XX     X  XXXXXXX",
"XXX  XXXXX  XXX        XX",
"XXX   XXXX      XXXXX  XX",
"XXX            XXXX  E XX",
"XXXE XXXXXXXXXXXT    XXXX",
"XXX XX  XXX   XXXX  XXXX",
"XXXXX  XX XXX        XXXX",
"XXXT    XX     XXX    XXX",
"XXXXXXX      XX    XXXXXX",
"XX    XXXXXXXXX  XXXXXXXX",
"XXX    XXXXX      XXXXXXX",
"XXXXX         XXXXX  XXXX"
]

# add treasure list
treasures = []

# add enemy list
enemies = []

# append level to level list
levels.append(level_1)

#create level setup functions
def setup_maze(level):
	for i in range(len(level)):
		for j in range(len(level[i])):
			#sweep all characters in level
			character = level[i][j]
			#calculate the screen x, y coordinates
			screen_x = -288 + 24 * j
			screen_y = 288 - 24 * i

			# Check if it is an X (representing a wall)
			if character == "X":
				pen.goto(screen_x, screen_y)
				pen.shape("tree.gif")          #### my understanding: by defining shape here, 
				                                 # easier for define other shapes with same pen class.
				pen.stamp()   # stemp means put it on the screen and leave it there
				# add coordinate into wall list
				walls.append((screen_x, screen_y))

			# check if it is a P (representing Player)
			if character == "P":
				player.goto(screen_x, screen_y)

			# check if it is a T (representing Treasure)
			if character == "T":
				treasures.append(Treasure(screen_x,screen_y)) 
				#Treasure(screen_x,screen_y) automatic put treasures on the screen

			# check if it it a E (representing enemy)
			if character == "E":
				enemies.append(Enemy(screen_x, screen_y))

# Create class instance
pen = Pen ()
player = Player ()
paw = Paw()
###pen and player need to be created as instances as we want to use their function as a turtle (goto, stamp, etc). 
##For Treasure, we dont use it function, just use its intrinsic goto function. Hence, can be directly used.

# Create wall coordinate list
walls = []

# show the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("black")
score_pen.penup()
score_pen.setposition(0,310)
scorestring = "player.gold: 0"   ###########fill in the score
score_pen.write(scorestring, False, align="center", font= ("Arial", 24, "normal"))
score_pen.hideturtle()

# Set up the leve
setup_maze(levels[1])

#Keyboard Binding
turtle.listen()
turtle.onkey(player.go_up, "Up")   ## as go_up etc is defined inside player class -> player.go_up
turtle.onkey(player.go_down, "Down")
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(paw.fire_up, "w") 
turtle.onkey(paw.fire_down, "s")
turtle.onkey(paw.fire_left, "a")
turtle.onkey(paw.fire_right, "d")

# Start moving enemies
for enemy in enemies:
	turtle.ontimer(enemy.move, t=250)

# Main game loop
while True:
	#check collision needs to be inside while loop as it requires continuous checking
	for treasure in treasures:
		if player.is_collision(treasure):
			player.gold += treasure.gold
			# print ("player.gold: {}".format(player.gold))
			score_pen.clear()
			scorestring = "player gold: %s" %player.gold   ###########fill in the score
			score_pen.write(scorestring, False, align="center", font= ("Arial", 24, "normal"))			
			treasure.destroy()
			#remove treasure from treasures list
			treasures.remove(treasure)	
	# check collision between player and enemies
	for enemy in enemies:
		if player.is_collision(enemy):
			for enemy in enemies:
				enemy.hideturtle()
			for treasure in treasures:
				treasure.hideturtle()
			player.hideturtle()
			paw.hideturtle()
			create_text((0,60), "Game Over")

	#start move the paw
	turtle.ontimer(paw.move, t=1)


	wn.update()   
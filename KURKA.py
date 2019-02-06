import sys, turtle 
from turtle import Turtle, Screen

walls=[]
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("turtle")
        self.color("yellow")
        self.penup()
        self.speed(0)

    def go_down(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 1
    
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)


    def go_right(self):
        move_to_x = player.xcor()+1
        move_to_y = player.ycor()
    
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)


    def go_left(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor()+1
    
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)


    def go_up(self):
        move_to_x = player.xcor()-1
        move_to_y = player.ycor()
    
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            
player=Player()    

turtle.onkey(player.go_right,"Right")
turtle.onkey(player.go_left,"Up")
turtle.onkey(player.go_down,"Down")
turtle.onkey(player.go_up,"Left")
turtle.listen()

MAP = '''
XXXXXXXXXXXXXXXXXXXXXXXXX
XOOOOOOOOOOOOOOOOOOOOOOXX
XOOOOOOOOOOOOOOOOOOOOOOXX
XOOXXXXXXXXXXXXXXXXXXOOXX
XOOOOOOOOOOOOOOOOOOXXOOXX
XOOOOOOOOOOOOOOOOOOXXOOXX
XXXXXXXOOXXXXXXXXOOXXOOXX
XXXXXXXOOXXOOXXXXOOXXOOXX
XOOOOOOOOXXOOOOOOOOXXXXXX
XOOOOOOOOXXOOOOOOOOXXXXXX
XOOXXXXXXXXXXXXXXOOOOOOXX
XOOOOOOOOOOXOOOXXOOOOOOXX
XOOOOOOOOOOXOOOXXXXXXOOXX
XOOOOXXXXOOXXOOOXXXXXOOXX
XXXOOXXXXOOXXOOOXXXXXOOXX
XXXOOOOOOXXXOOOOXXXXXOOXX
XXXOOOOOOXXXOOOOOOOOOOOXX
XXXXXXXOOXXXXXOOOOOOOOOXX
XXOOOOOOOXXXXXXXXOOXXXXXX
XXOOOOOOOXXOOOOXXOOOOOXXX
XXOOXXXXXXXOOOOXXOOOOOXXX
XXOOOOOOOXXXXOOOOOOXXXXXX
XXOOOOOOOOOOOOOOOOOXXXXXX
OOOOOOOOOOOOOOOXXXXXXXXXX
OOOOXXXXXXXXXXXXXXXXXXXXX
'''

Map_Array = [list(row) for row in MAP.strip().split('\n')]
Map_Array.reverse()
Scale = 3
Stamp_Size = 20
Width, Height = len(Map_Array[0]), len(Map_Array)

screen = Screen()
screen.setup(Width * Stamp_Size * Scale, Height * Stamp_Size * Scale)
screen.setworldcoordinates(-0.5, -0.5, Width - 0.5, Height - 0.5)

turtle = Turtle('square', visible=False)
turtle.shapesize(Scale)
turtle.speed('fastest')
turtle.penup()

for y, row in enumerate(Map_Array):
    for x, character in enumerate(row):
        if character == 'X':
            a=(x,y)
            walls.append(a)
            print (walls)
            turtle.goto(x, y)
            turtle.stamp()

screen.tracer(0)

#Main Game Loop
n=False
while n!=True:
    screen.update()
    
def endProgram():
    turtle.done()
    n=True
    screen.exitonclick()
    sys.exit()
    
screen.mainloop()
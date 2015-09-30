# Alex Maclay
# vPool

from visual import *

COEFFICIENT_OF_FRICTION = .99 #Friction constant of the balls against the table
MINIMUM_VELOCITY = .5 #Threshold used to stop balls, prevents aymptotic deceleration
BUFFER = .01 #buffer to prevent balls from sticking to the walls

def initializeGraphics():
    """This function initializes the table, the target, and the game balls.
    It has no input, and returns a list of each variable created into the
    main function.  This is to avoid a bloated main() function."""

    #Walls and Floor

    floor = box(pos = (0,0,0),length = 9,height = 0.1, \
                width = 4.5, color = color.green)
    target = box(pos = (-3,.025,-0), length = 3, height = 0.1, \
                 width = 3, color = color.orange)
    rightWall = box(pos = (4.5,0,0), length = .1, height = 0.5, \
                    width = 4.5, color = color.green)
    leftWall = box(pos = (-4.5,0,0), length = .1, height = 0.5, \
                    width = 4.5, color = color.green)
    frontWall = box(pos = (0,0,2.25), length = 9, height = 0.5, \
                    width = .1, color = color.green)
    backWall = box(pos = (0,0,-2.25), length = 9, height = 0.5, \
                   width = .1, color = color.green)

    #Balls

    cueBall = sphere(pos = (-2.25,.125,0), radius = 0.1, color = color.white)
    cueBall.vel = vector(0,0,0)
    oneBall = sphere(pos = (2.25,.125,0), radius = 0.1, color = color.blue)
    oneBall.vel = vector(0,0,0)
    twoBall = sphere(pos = (2.45,.125,.15), radius = 0.1, color = color.orange)
    twoBall.vel = vector(0,0,0)
    threeBall = sphere(pos = (2.45,.125,-.15), radius = 0.1, color = color.orange)
    threeBall.vel = vector(0,0,0)
    fourBall = sphere(pos = (2.7,.125,-.25), radius = 0.1, color = color.blue)
    fourBall.vel = vector(0,0,0)
    fiveBall = sphere(pos = (2.7,.125,0), radius = 0.1, color = color.orange)
    fiveBall.vel = vector(0,0,0)
    sixBall = sphere(pos = (2.7,.125,.25), radius = 0.1, color = color.blue)
    sixBall.vel = vector(0,0,0)

    ballList = [cueBall, oneBall, twoBall, threeBall, fourBall, fiveBall, sixBall] #Ball list object

    return [ballList, floor, target, rightWall, leftWall, frontWall, backWall]


def gameBallWallCollision(ballList,rightWall,leftWall,backWall,frontWall):
    """This functions handles the collisions between the 6 game balls and the walls.
    It takes the list of balls and each of the walls as input and ouputs
    modified velocities of the balls to simulate wall collision"""

    for i in range(len(ballList)):
        if (ballList[i].pos.x + ballList[i].radius) >= (rightWall.pos.x - rightWall.length):
            ballList[i].pos.x = (rightWall.pos.x - rightWall.length - ballList[i].radius - BUFFER) # This and similar lines place ball just inside the borders of the table, remedying an issue where balls would get stuck on the wall.
            ballList[i].vel.x *= -1
        if (ballList[i].pos.x - ballList[i].radius) <= (leftWall.pos.x + leftWall.length):
            ballList[i].pos.x = (leftWall.pos.x + leftWall.length + ballList[i].radius + BUFFER)
            ballList[i].vel.x *= -1
        if (ballList[i].pos.z - ballList[i].radius) <= (backWall.pos.z + backWall.width):
            ballList[i].pos.z = (backWall.pos.z + backWall.width + ballList[i].radius + BUFFER)
            ballList[i].vel.z *= -1
        if (ballList[i].pos.z + ballList[i].radius) >= (frontWall.pos.z - frontWall.width):
            ballList[i].pos.z = (frontWall.pos.z - frontWall.width - ballList[i].radius - BUFFER)
            ballList[i].vel.z *= -1
        

def collide(ball1, ball2):
    """This function handles collisions between any of the 7 balls in play.
    It takes ball1 and ball2, which come as input from two
    nested loops, and changes the velocity and position of each ball based
    on the collisions."""

    dt = 0.01
    diff = ball2.pos - ball1.pos
    dtan = rotate( diff, radians(90), vector(0,1,0) )
    # if they're too close...
    if mag( diff ) < 2*ball1.radius:
        # get the two velocities
        vi = ball2.vel
        vj = ball1.vel
        # undo the last time step
        ball2.pos -= ball2.vel*dt
        ball1.pos -= ball1.vel*dt
        # find the radial and tangent parts
        vi_rad = proj(vi, diff)
        vi_tan = proj(vi, dtan)
        vj_rad = proj(vj, -diff)
        vj_tan = proj(vj, dtan)
        # swap the radials and keep the tangents
        ball2.vel =  vj_rad + vi_tan
        ball1.vel =  vi_rad + vj_tan


def allStop(ballList):
    """ This function stops all balls if the ball with the highest velocity
        is less than the globally defined minimum velocity in order to
        facilitate gameplay.  It takes the list of balls as input and
        sets each velocity to zero once each ball has slowed sufficiently."""
    
    velocities = []
    for i in range(len(ballList)):
        if mag(ballList[i].vel) != 0:
            velocities += [abs(mag(ballList[i].vel))]
    if max(velocities) < MINIMUM_VELOCITY:
        for i in range(len(ballList)):
            ballList[i].vel = vector(0,0,0)
        return True
    

def isWin(target, ballList):
    """This function determines whether or not the user has won the game by placing
    all 6 game balls within the target region. It takes the target and the list of
    balls as input and returns True if win conditions are met"""

    counter = 0 # initialize variable to count number of balls in target region
    for j in range(1, len(ballList)):
        if ballList[j].pos.x > (target.pos.x - .5*target.length) and \
           ballList[j].pos.x < (target.pos.x + .5*target.length) and \
           ballList[j].pos.z > (target.pos.z - .5*target.width) and \
           ballList[j].pos.z < (target.pos.z + .5*target.width):
            counter += 1
        if counter == len(ballList)-1:
            return True

 
def main():
    """the main function that handles gameplay.  This function sets the parameters
    for the balls, the arrow that shoots them, and the target box that takes up
    the end of the pool table.  It takes no inputs, but outputs the game
    itself"""

    ballList, floor, target, rightWall, leftWall, frontWall, backWall = initializeGraphics()

    label(pos=(0,0,-5), text="Try to get all 6 balls into the orange box!") # Display instructions
    scene.range = 15
    scene.forward = vector(0,-1,0) # look straight down
    scene.autoscale = False
    dt = 0.01 # value defined in program instructions
   
    while True:
        if scene.mouse.events: 
            m1 = scene.mouse.getevent()
            if m1.press:
                ballList[0].vel = (0,0,0)
                ballList[0].vel = 2*vector(m1.pos.x-ballList[0].pos.x, 0, m1.pos.z-ballList[0].pos.z)
                while True:
                    rate(1/dt)
                    for i in range(len(ballList)):
                        ballList[i].vel *= COEFFICIENT_OF_FRICTION
                        ballList[i].pos += ballList[i].vel * dt
                    gameBallWallCollision(ballList,rightWall,leftWall,backWall,frontWall)
                    if allStop(ballList) is True:
                        break
                    #collisions
                    for i in range(len(ballList)):
                        for j in range(i+1, len(ballList)):
                            collide(ballList[i], ballList[j])
                if isWin(target, ballList) is True:
                    break
    label(pos=(0,0,5), text="You Win!", height=16)
                                
                                                        
if __name__ == "__main__":
    main()






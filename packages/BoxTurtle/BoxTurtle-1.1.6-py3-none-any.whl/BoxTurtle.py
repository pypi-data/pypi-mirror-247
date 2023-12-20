import turtle
import math


if __name__ == "__main__":
    print("Build v1.1.6")
    print("This was created using the Python turtle module. I do not take credit for the creation of the original Python turtle library")
    print("GitHub: https://github.com/chadwickjr (chadwickjr)")


camX, camY, camZ = 0, 0, -30
rotationX, rotationY, rotationZ = 0, 0, 0
FOV = 500
penUp = False
BTtracer = True


def stampaxis(width = 20):
    if width > 29:
        width = 29

    turtle.pensize(0.5)
    turtle.tracer(False)

    for num in range(-1 * width, width, 1):
        line(0, num + 0.25, 0, 0, num - 0.25, 0)

    for num in range(-1 * width, width, 1):
        line(num + 0.25, 0, 0, num - 0.25, 0, 0)

    for num in range(-1 * width, width, 1):
        line(0, 0, num + 0.25, 0, 0, num - 0.25)
    
    turtle.update()

    if BTtracer:
        turtle.tracer(True)


def movecam(x, y, z):
    global camX, camY, camZ
    camX += x
    camY += y
    camZ += z


def rotate(x, y, z):
    global rotationX, rotationY, rotationZ

    rotationX += x / 57.25
    rotationY += y / 57.25
    rotationZ += z / 57.25


def line(startX, startY, startZ, endX, endY, endZ):
    turtle.hideturtle()
    startX *= -1
    startY *= -1
    startZ *= -1
    endX *= -1
    endY *= -1
    endZ *= -1

    cosZ = math.cos(rotationZ)
    sinZ = math.sin(rotationZ)
    cosX = math.cos(rotationX)
    sinX = math.sin(rotationX)
    cosY = math.cos(rotationY)
    sinY = math.sin(rotationY)

    x1 = startX * cosZ - startY * sinX
    y1 = startX * sinZ + startY * cosZ
    y1 = startY * cosX - startZ * sinX
    z1 = startY * sinX + startZ * cosX
    x1 = startX * cosY + startZ * sinY
    z1 = -1 * startX * sinY + startZ * cosY

    x2 = endX * cosZ - endY * sinX
    y2 = endX * sinZ + endY * cosZ
    y2 = endY * cosX - endZ * sinX
    z2 = endY * sinX + endZ * cosX
    x2 = endX * cosY + endZ * sinY
    z2 = -1 * endX * sinY + endZ * cosY

    turtle.penup()
    turtle.goto(FOV * ((x1 + camX) / (z1 + camZ)), FOV * ((y1 + camY) / (z1 + camZ)))
    turtle.pendown()
    turtle.goto(FOV * ((x2 + camX) / (z2 + camZ)), FOV * ((y2 + camY) / (z2 + camZ)))
    
    if penUp:
        turtle.penup()


def goto(x, y, z):
    turtle.hideturtle()

    x *= -1
    y *= -1
    z *= -1

    cosZ = math.cos(rotationZ)
    sinZ = math.sin(rotationZ)
    cosX = math.cos(rotationX)
    sinX = math.sin(rotationX)
    cosY = math.cos(rotationY)
    sinY = math.sin(rotationY)

    x1 = x * cosZ - y * sinX
    y1 = x * sinZ + y * cosZ
    y1 = y * cosX - z * sinX
    z1 = y * sinX + z * cosX
    x1 = x * cosY + z * sinY
    z1 = -1 * x * sinY + z * cosY

    turtle.goto(FOV * ((x1 + camX) / (z1 + camZ)), FOV * ((y1 + camY) / (z1 + camZ)))


def cube(x = 0, y = 0, z = 0, size = 10):
    size /= 2

    line(x - size, y - size, z + size, x - size, y + size, z + size)
    line(x - size, y + size, z + size, x + size, y + size, z + size)
    line(x + size, y + size, z + size, x + size, y - size, z + size)
    line(x + size, y - size, z + size, x - size, y - size, z + size)
    line(x - size, y - size, z - size, x - size, y + size, z - size)
    line(x - size, y + size, z - size, x + size, y + size, z - size)
    line(x + size, y + size, z - size, x + size, y - size, z - size)
    line(x + size, y - size, z - size, x - size, y - size, z - size)
    line(x + size, y - size, z - size, x + size, y + size, z - size)
    line(x + size, y + size, z - size, x + size, y + size, z + size)
    line(x + size, y + size, z + size, x + size, y - size, z + size)
    line(x + size, y - size, z + size, x + size, y - size, z - size)
    line(x - size, y - size, z - size, x - size, y + size, z - size)
    line(x - size, y + size, z - size, x - size, y + size, z + size)
    line(x - size, y + size, z + size, x - size, y - size, z + size)
    line(x - size, y - size, z + size, x - size, y - size, z - size)


def bgcolor(color):
    turtle.bgcolor(color)

def speed(speed):
    turtle.speed(speed)

def title(title):
    turtle.title(title)

def done():
    turtle.done()

def penup():
    turtle.penup()
    penUp = True

def pendown():
    turtle.pendown()
    penUp = False

def color(color):
    turtle.color(color)

def pensize(size):
    turtle.pensize(size)

def clear():
    turtle.clear()

def tracer(a):
    global BTtracer
    BTtracer = a
    turtle.tracer(a)

def update():
    turtle.update()

def Screen():
    return turtle.Screen()

def mainloop():
    turtle.mainloop()

def setup(x, y):
    turtle.setup(x, y)

def stamp():
    turtle.stamp()

def exitonclick():
    turtle.exitonclick()

def bye():
    turtle.bye()

def Turtle():
    return turtle.Turtle()
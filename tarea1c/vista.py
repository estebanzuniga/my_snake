#Tarea 1
#Esteban Zuniga Salamanca
#20366619-5

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import transformations as tr
import basic_shapes as bs
import easy_shaders as es
import scene_graph as sg
import random
import modelo as mo

n = int(sys.argv[1])
#n = 15
global scale
scale = 1.9/n

x_ap = random.randint((-n//2)+1,(n-1)//2)*scale
y_ap = random.randint((-n//2)+1,n//2)*scale
if n%2==0:
    x_ap = (scale/2)+(random.randint(-n//2,(n-1)//2)*scale)
    y_ap = (scale/2)+(random.randint(-n//2,(n-1)//2)*scale)
    
x = scale
y = scale
if n%2==0:
    x = scale/2
    y = scale/2

class Controller:
    fillPolygon = True

controller = Controller()

posiciones = [[x,y]]
largo = 1
i = 1
cola = []
state = "RIGHT"

def update():

    global snake
    global x
    global y
    global i
    global cola
    
    if state == "UP":
        y += scale
        cola = posiciones.pop(len(posiciones)-1)
        i += 1
        posiciones.insert(0,[x,y])
        snake.transform = tr.translate(x, y, 0)

    elif state == "DOWN":
        y -= scale
        cola = posiciones.pop(len(posiciones)-1)
        i += 1
        posiciones.insert(0,[x,y])
        snake.transform = tr.translate(x, y, 0)

    elif state == "RIGHT":
        x += scale
        cola = posiciones.pop(len(posiciones)-1)
        i += 1
        posiciones.insert(0,[x,y])
        snake.transform = tr.translate(x, y, 0)

    elif state == "LEFT":
        x -= scale
        cola = posiciones.pop(len(posiciones)-1)
        i += 1
        posiciones.insert(0,[x,y])
        snake.transform = tr.translate(x, y, 0)

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller
    global state

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
        print("Toggle GL_FILL/GL_LINE")

    elif key == glfw.KEY_ESCAPE:
        sys.exit()
    
    if key == glfw.KEY_UP or key == glfw.KEY_W:
        if state != "DOWN":
            state = "UP"

    elif key == glfw.KEY_DOWN or key == glfw.KEY_S:
        if state != "UP":
            state = "DOWN"

    elif key == glfw.KEY_RIGHT or key == glfw.KEY_D:
        if state != "LEFT":
            state = "RIGHT"

    elif key == glfw.KEY_LEFT or key == glfw.KEY_A:
        if state != "RIGHT":
            state = "LEFT"

    else:
        print('Unknown key')

if __name__ == "__main__":
    
    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 700
    height = 700

    window = glfw.create_window(width, height, "Snake", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.SimpleTextureTransformShaderProgram()
    pipeline2 = es.SimpleTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Creating shapes on GPU memory
    gpuWall = es.toGPUShape(bs.createTextureQuad("wall.png",10,10), GL_REPEAT, GL_NEAREST)
    wallTransform = tr.scale(2, 2, 1)

    gpuGrass = es.toGPUShape(bs.createTextureQuad("grass.png",10,10), GL_REPEAT, GL_NEAREST)
    grassTransform = tr.scale(1.9, 1.9, 1)

    gpuGameOver = es.toGPUShape(bs.createTextureQuad("game_over.png",1,1), GL_REPEAT, GL_NEAREST)
    gameOverTransform = tr.scale(1, 0.5, 1)
    
    if n%2==0:
        snakes = mo.createSnakes(largo,posiciones,scale,scale/2)
    elif n%2!=0:
        snakes = mo.createSnakes(largo,posiciones,scale,scale)

    apples = mo.createApple(x_ap,y_ap,scale)

    t0 = 0
    perder = False
    
while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Drawing the shapes with a specific shader program depending on the controller state
        glUseProgram(pipeline.shaderProgram)
        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, wallTransform)
        pipeline.drawShape(gpuWall)
        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, grassTransform)
        pipeline.drawShape(gpuGrass)

        if i > len(posiciones):
            i = 1

        if x_ap-0.001 <= x <= x_ap+0.001 and y_ap-0.001 <= y <= y_ap+0.001:
            if n%2 == 0:
                x_ap = (scale/2)+(random.randint(-n//2,(n-1)//2)*scale)
                y_ap = (scale/2)+(random.randint(-n//2,(n-1)//2)*scale)
                while [x_ap,y_ap] in posiciones:
                    x_ap = (scale/2)+(random.randint(-n//2,(n-1)//2)*scale)
                    y_ap = (scale/2)+(random.randint(-n//2,(n-1)//2)*scale)
            elif n%2 != 0:
                x_ap = random.randint((-n//2)+1,(n-1)//2)*scale
                y_ap = random.randint((-n//2)+1,n//2)*scale
                while [x_ap,y_ap] in posiciones:
                    x_ap = random.randint((-n//2)+1,(n-1)//2)*scale
                    y_ap = random.randint((-n//2)+1,n//2)*scale

            apple = sg.findNode(apples, "traslatedApple")
            apple.transform = tr.translate(x_ap,y_ap,0)
            largo += 1
            posiciones.append(cola)
            snakes = mo.createSnakes(largo,posiciones,scale,scale/2)
            i = 1

        if perder == False:    
            snake = sg.findNode(snakes, "snakes"+str(len(posiciones)-i))
            sg.drawSceneGraphNode(snakes, pipeline, "transform")
            glUseProgram(pipeline2.shaderProgram)
            sg.drawSceneGraphNode(apples, pipeline2, "transform")

        glUseProgram(pipeline.shaderProgram)

        t0 += 1
        if t0%(30-(5*largo)//8) == 0:
            update()
            t0 = 0

        t = glfw.get_time() 
        theta = 0.2 * np.cos(0.5 * t)       

        if x <= -0.95 or x >=0.95 or y <= -0.95 or y >= 0.95 or posiciones[0] in posiciones[1:len(posiciones)] or perder == True:
            perder = True
            gameOver = sg.SceneGraphNode("gameOver")
            gameOver.transform = tr.rotationZ(theta)
            gameOver.childs += [gpuGameOver]
            game_over = sg.findNode(gameOver, "gameOver")
            sg.drawSceneGraphNode(gameOver, pipeline, "transform")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

glfw.terminate()

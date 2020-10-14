from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es
from math import pi, cos, sin

#Creates a green circle
def drawGreenCircle(r,n):

    gpuShape = es.GPUShape()

    def vertices(n):
        phi = (2*pi)/n
        theta = 0
        ver = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
        while theta <= 2*pi:
            ver.append(r*cos(theta))
            ver.append(r*sin(theta))
            ver.append(0.0)
            ver.append(95/256)
            ver.append(212/256)
            ver.append(28/256)
            theta += phi
        return ver

    vertexData = np.array(vertices(n), dtype = np.float32)

    def index(n):
        ind = []
        for i in range(2,3*n):
            ind.append(0)
            ind.append(i-1)
            ind.append(i)
        return ind

    indices = np.array(index(n), dtype = np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * 4, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4, indices, GL_STATIC_DRAW)

    return gpuShape

#Creates a green circle
def drawRedCircle(r,n):

    gpuShape = es.GPUShape()

    def vertices(n):
        phi = (2*pi)/n
        theta = 0
        ver = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
        while theta <= 2*pi:
            ver.append(r*cos(theta))
            ver.append(r*sin(theta))
            ver.append(0.0)
            ver.append(240/256)
            ver.append(22/256)
            ver.append(22/256)
            theta += phi
        return ver

    vertexData = np.array(vertices(n), dtype = np.float32)

    def index(n):
        ind = []
        for i in range(2,3*n):
            ind.append(0)
            ind.append(i-1)
            ind.append(i)
        return ind

    indices = np.array(index(n), dtype = np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * 4, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4, indices, GL_STATIC_DRAW)

    return gpuShape

#Creates an apple
def createApple(x, y, scale):

    gpuBody = drawRedCircle(1,20)
    gpuLeaf = drawGreenCircle(0.08,20)    

    #Creating the leaf
    leaf = sg.SceneGraphNode("leaf")
    leaf.transform = tr.translate(0,0.25,0)
    leaf.childs += [gpuLeaf]
    
    #Creating the body
    body = sg.SceneGraphNode("body")
    body.transform = tr.uniformScale(0.2)
    body.childs += [gpuBody]

    #Creatin an apple
    apple = sg.SceneGraphNode("apple")
    apple.childs += [leaf]
    apple.childs += [body]

    #Scaling the apple
    scaledApple = sg.SceneGraphNode("scaledApple")
    scaledApple.transform = tr.uniformScale(scale)
    scaledApple.childs += [apple]

    #Traslating the apple
    traslatedApple = sg.SceneGraphNode("traslatedApple")
    traslatedApple.transform = tr.translate(x,y,0)
    traslatedApple.childs += [scaledApple]

    return traslatedApple

#Creates a snake
def createSnake(scale,pos):

    gpuSnake = es.toGPUShape(bs.createTextureQuad("snake.png", 1, 1), GL_REPEAT, GL_NEAREST)

    # Creating a snake
    snake1 = sg.SceneGraphNode("snake1")
    snake1.transform = tr.uniformScale(scale)
    snake1.childs += [gpuSnake]

    return snake1

#Creates a snake of length N 
def createSnakes(N,posiciones,scale,pos):

    # Creating the snake of length N
    final_snakes = sg.SceneGraphNode("final_snakes")
    final_snakes.transform = tr.identity()
    final_snakes.childs += [createSnake(scale,pos)]

    snakes = sg.SceneGraphNode("snakes")

    baseName = "snakes"
    for i in range(N):
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.translate(posiciones[i][0], posiciones[i][1], 0)
        newNode.childs += [final_snakes]

        snakes.childs += [newNode]

    return snakes


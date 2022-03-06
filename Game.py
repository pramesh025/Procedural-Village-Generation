from turtle import position
import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import pyrr
import random
import Material as mat
import ObjMesh as obj
import Player as pl
import Physics as phy
import TileCreator
import GameObject as go
from pygame import Vector3


class Game:
    def __init__(self):
        #Place Game variables

        self.renderDistance = 10
        self.gravity = 5
        self.speed = 0.0025
        self.slowUpdateTime = 0.5

        self.mainInit()
        pass

    
    def start(self): #CALLED Before the first frame
        ####   list of created variables
        #  cubes =[8 cubes]
        #  lights = [8 lights]
        #  player
        ####   end of variable list
        self.tilecreator = TileCreator.TileCreator(self.gameMeshes, self.gameMaterials)


        self.ckeydown = False
        self.spkeydown = False

        self.view.setProperties(640,480)
        self.camera.setProperties(45,640/480,0.1,40)
        self.player.setProperties(position = [5, 5, 1], eulers = [0, 0, 0])

        self.ppx = 320
        self.ppy = 240

        #COLLECT MESHES
        self.gameMeshes.append(Mesh("models/Triangulated/woodfloor.obj"))  #WOOD FLOOR LEVEL 0 # 0
        self.gameMeshes.append(Mesh("models/Triangulated/woodfloorL.obj")) #WOOD FLOOR L       # 1
        self.gameMeshes.append(Mesh("models/Triangulated/woodfloorI.obj")) #WOOD FLOOR I       # 2
        self.gameMeshes.append(Mesh("models/Triangulated/wallblank.obj"))  #BLANK WALL         # 3
        self.gameMeshes.append(Mesh("models/Triangulated/wallwindow.obj")) #1 WALL WITH WINDOW # 4
        self.gameMeshes.append(Mesh("models/Triangulated/window.obj"))     #WINDOW             # 5
        self.gameMeshes.append(Mesh("models/Triangulated/walldoorR.obj"))  #RIGHT DOOR         # 6
        self.gameMeshes.append(Mesh("models/Triangulated/walldoorL.obj"))  #LEFT DOOR          # 7
        self.gameMeshes.append(Mesh("models/Triangulated/door.obj"))       #DOOR               # 8
        self.gameMeshes.append(Mesh("models/Triangulated/windowbars.obj")) #WINDOW BARS        # 9
        self.gameMeshes.append(Mesh("models/Triangulated/doorbars.obj"))   #WINDOW BASE        # 10
        self.gameMeshes.append(Mesh("models/Triangulated/post.obj"))       #POST               # 11
        self.gameMeshes.append(Mesh("models/Triangulated/windowbase.obj")) #WINDOW BASE        # 12
        self.gameMeshes.append(Mesh("models/Triangulated/lamp.obj"))       #LAMP               # 13
        self.gameMeshes.append(Mesh("models/Triangulated/sand.obj"))       #SAND               # 14
        self.gameMeshes.append(Mesh("models/Triangulated/woodfloor.obj"))  #WOOD CEILING       # 15


        #COLLECT MATERIALS
        
        self.gameMaterials.append(Matt("Floor", "png"))     #WOOD FLOOR       # 0
        self.gameMaterials.append(Matt("Wall", "png"))      #STONE WALL       # 1
        self.gameMaterials.append(Matt("Metal", "png"))     #SILVER METAL     # 2
        self.gameMaterials.append(Matt("Door", "png"))      #WINDOW           # 3
        self.gameMaterials.append(Matt("Door", "png"))      #DOOR             # 4
        self.gameMaterials.append(Matt("Post", "png"))      #POST             # 5
        self.gameMaterials.append(Matt("Lamp", "png"))      #LANTERN          # 6
        self.gameMaterials.append(Matt("Sand", "png"))      #SAND             # 7
        self.gameMaterials.append(Matt("Stone", "png"))     #STONE            # 8
        self.gameMaterials.append(Matt("crate", "png"))     #TEST CRATE       # 9

        self.tilecreator.createInitial(self.player.vposition)


        #EIGHT RANDOM LIGHTS
        for i in range(11):
            self.lights.append(Light(
                name = "light " + str(i),
                position = [random.uniform(a = -10, b = 10) for x in range(3)],
                # color = []
                color = [random.uniform(a = 0.5, b = 1) for x in range(3)]
            ))

        pass

    def slowUpdate(self): #called every certain amount of time
        self.tilecreator.iterateTileCreation(self.player.vposition, 50)


        return
        if(abs(self.player.position[0] - self.prevPlayerPos[0]) > 1 or abs(self.player.position[1] - self.prevPlayerPos[1]) > 1):
            self.tilecreator.iterateTileCreation(self.player.vposition, 5)
            self.prevPlayerPos = [int(self.player.position[0]), int(self.player.position[1])]
            #print(self.player.position, self.prevPlayerPos)
            pass
        pass

    def mouseInputUpdate(self):
        ### mouse control ##

        (x,y) = pg.mouse.get_pos()
        theta_increment = self.frameTime * 0.05 * (320 - x)
        phi_increment = self.frameTime * 0.05 * (240 - y)
        self.player.increment_direction(theta_increment, phi_increment)
        pg.mouse.set_pos((320,240))
        
        pass


    def inputUpdate(self):
        
        ### keyboard control ###
        keys = pg.key.get_pressed()
        if keys[pg.K_g]:
            self.player.isGravity = not self.player.isGravity
            return

        if keys[pg.K_SPACE]:
            if self.spkeydown == False:
                self.player.jump(0.005*self.frameTime)
                self.spkeydown = True
        else:
            self.spkeydown = False
        pass
        if keys[pg.K_UP] or keys[pg.K_w] or keys[pg.K_COMMA]:
            self.player.moveForward(self.speed*self.frameTime)
            return
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.player.moveRight(self.speed*self.frameTime)
            return
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.player.moveLeft(self.speed*self.frameTime)
            return
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.player.moveBack(self.speed*self.frameTime)
            return
      

        if keys[pg.K_c]:
            if self.ckeydown == False:
                self.tilecreator.iterateTileCreation(self.player.vposition, 50)
                self.ckeydown = True
        else:
            self.ckeydown = False
        pass

    def update(self): #Is called every frame
        ####
        if(self.player.vposition.z > 1.5):
            self.player.displacement += Vector3(0,0,-0.0001*self.gravity*self.frameTime)
        else:
            if(self.player.displacement.z < 0):
                self.player.displacement.z = 0
                self.player.vposition.z = 1.5
            pass

        self.player.translate(self.player.displacement)                               
        self.player.position = np.array(self.player.vposition,dtype=np.float32)
        ####
        
        self.autoCreateMeshTransforms()
        pass

    #Don't change things after here unless you know what you're doing -Rob
    def mainInit(self):
        self.lastTime = 0
        self.currentTime = 0
        self.numFrames = 0
        self.frameTime = 0
        self.speedMultiplier = 0.0025
        self.lightCount = 0
        
        self.lights = []
        self.player = pl.Player(
            position = [0, 1, 1.5],
            eulers = [0, 0, 0]
        )
        self.prevPlayerPos = [0,1]
        self.physics = phy.physics(
            position = [-10, 0, 0]
        )
        self.camera = Camera(45,640/480,0.1,40)
        self.view = View(640,480)

        self.gameMeshes = []
        self.gameMaterials = []
     
        self.start()

        #initialise pygame
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((self.view.hres,self.view.vres), pg.OPENGL|pg.DOUBLEBUF)
        pg.mouse.set_pos((int(self.view.hres/2),int(self.view.vres/2)))
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        

        self.glStuffInit(self.camera)
        
        # start main loop
        self.mainLoop()
        pass 

    def mainLoop(self):
        running = True
        while (running):
            #check events
            for event in pg.event.get():
                if (event.type == pg.KEYDOWN and event.key==pg.K_ESCAPE):
                    running = False
            #update objects, get controls

            self.showFrameRate()
            
            self.mouseInputUpdate()
            self.inputUpdate()
            self.update()

            # self.physics()
            #refresh screen
            #print(self.currentTime)
            
            self.draw()
            
            
        self.quit()
        pass

    def showFrameRate(self):
        self.currentTime = pg.time.get_ticks()
        delta = self.currentTime - self.lastTime
        if (delta >= 1000*self.slowUpdateTime):
            self.slowUpdate()


            framerate = int(1000.0 * self.numFrames/delta)
            pg.display.set_caption(f"Running at {framerate} fps.")
            self.lastTime = self.currentTime
            self.numFrames = -1
            if(framerate != 0):
                self.frameTime = float(1000.0 / framerate)
            else:
                self.frateTime = 10000
        self.numFrames += 1
    
    def glStuffInit(self, icamera):
         #initialise opengl

        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)


        
        




        self.shaderTextured = self.createShader(
            "shaders/vertex.txt", 
            "shaders/fragment.txt"
        )
        self.shaderColored = self.createShader(
            "shaders/simple_3d_vertex.txt", 
            "shaders/simple_3d_fragment.txt"
        )
        
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = icamera.fovy, aspect = icamera.aspect, 
            near = icamera.near, far = icamera.far, dtype=np.float32
        )

        glUseProgram(self.shaderTextured)

        #get shader locations
        self.viewLocTextured = glGetUniformLocation(self.shaderTextured, "view")
        self.lightLocTextured = {

            "pos": [
                glGetUniformLocation(
                    self.shaderTextured,f"lightPos[{i}]"
                ) 
                for i in range(len(self.lights))
            ],

            "color": [
                glGetUniformLocation(
                    self.shaderTextured,f"lights[{i}].color"
                ) 
                for i in range(len(self.lights))
            ],

            "strength": [
                glGetUniformLocation(
                    self.shaderTextured,f"lights[{i}].strength"
                ) 
                for i in range(len(self.lights))
            ],

            "count": glGetUniformLocation(
                self.shaderTextured,f"lightCount"
            )
        }

        self.cameraLocTextured = glGetUniformLocation(self.shaderTextured, "viewPos")

        #set up uniforms
        glUniformMatrix4fv(
            glGetUniformLocation(
                self.shaderTextured,"projection"
            ),
            1,GL_FALSE,projection_transform
        )

        glUniform3fv(
            glGetUniformLocation(
                self.shaderTextured,"ambient"
            ), 
            1, np.array([0.1, 0.1, 0.1],dtype=np.float32)
        )

        glUniform1i(
            glGetUniformLocation(
                self.shaderTextured, "material.albedo"
            ), 0
        )

        glUniform1i(
            glGetUniformLocation(
                self.shaderTextured, "material.ao"
            ), 1
        )

        glUniform1i(
            glGetUniformLocation(
                self.shaderTextured, "material.normal"
            ), 2
        )

        glUniform1i(
            glGetUniformLocation(
                self.shaderTextured, "material.specular"
            ), 3
        )
        #create assets

        for mat in self.gameMaterials:
            mat.loadNow()
        
        for mesh in self.gameMeshes:
            mesh.loadNow()
            self.createTransform(mesh)

        
        #get shader locations
        self.viewLocUntextured = glGetUniformLocation(self.shaderColored, "view")
        self.modelLocUntextured = glGetUniformLocation(self.shaderColored, "model")
        self.colorLocUntextured = glGetUniformLocation(self.shaderColored, "color")

        glUniformMatrix4fv(
            glGetUniformLocation(
                self.shaderColored,"projection"
            ),1,GL_FALSE,projection_transform
        )

        

        pass

    def autoCreateMeshTransforms(self):
        for mesh in self.gameMeshes:
            if mesh.transformsCreated == False:
                self.createTransform(mesh)
                mesh.transformsCreated = True

    def createTransform(self, mesh):           
        mesh.transforms = np.array([
            pyrr.matrix44.create_identity(dtype = np.float32)
            for i in range(len(mesh.assignedGameObjects))
        ], dtype=np.float32)
        glBindVertexArray(mesh.objmesh.vao)
        mesh.transformVBO = glGenBuffers(1)
        glBindBuffer(
            GL_ARRAY_BUFFER, 
            mesh.transformVBO
        )
        glBufferData(
            GL_ARRAY_BUFFER, 
            mesh.transforms.nbytes, 
            mesh.transforms, 
            GL_STATIC_DRAW
        )
        glEnableVertexAttribArray(5)
        glVertexAttribPointer(5, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(0))
        glEnableVertexAttribArray(6)
        glVertexAttribPointer(6, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(16))
        glEnableVertexAttribArray(7)
        glVertexAttribPointer(7, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(32))
        glEnableVertexAttribArray(8)
        glVertexAttribPointer(8, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(48))
        glVertexAttribDivisor(5,1)
        glVertexAttribDivisor(6,1)
        glVertexAttribDivisor(7,1)
        glVertexAttribDivisor(8,1)

        glUseProgram(self.shaderColored)


        for i, mgameObject in enumerate(mesh.assignedGameObjects):
            model_transform = pyrr.matrix44.create_identity(dtype=np.float16)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform, 
                m2=mgameObject.eulermat
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform, 
                m2=mgameObject.posmat
            )
            mesh.transforms[i] = model_transform
        pass

        if(mesh == self.gameMeshes[13]):
            for i, mgameObject in enumerate(mesh.assignedGameObjects):
                if i > 10: break
                self.lights[i].position = mgameObject.position


    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()

        temp1 = compileShader(vertex_src, GL_VERTEX_SHADER)
        temp2 = compileShader(fragment_src, GL_FRAGMENT_SHADER)
        
        shader = compileProgram(temp1,
                                temp2)
        
        return shader

    def draw(self):
        #refresh screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        

        view_transform = pyrr.matrix44.create_look_at(
            eye = self.player.position,
            target = self.player.position + self.player.get_forwards(),
            up = self.player.get_up(),
            dtype = np.float32
        )

        glUseProgram(self.shaderTextured)
        glUniformMatrix4fv(
            self.viewLocTextured, 1, GL_FALSE, view_transform
        )
        glUniform3fv(self.cameraLocTextured, 1, self.player.position)
        #lights
        glUniform1f(self.lightLocTextured["count"], min(8,max(0,len(self.lights))))
            
        for i, light in enumerate(self.lights):
            glUniform3fv(self.lightLocTextured["pos"][i], 1, light.position)
            glUniform3fv(self.lightLocTextured["color"][i], 1, light.color)
            glUniform1f(self.lightLocTextured["strength"][i], 0.5)
        

        for mesh in self.gameMeshes:
            if(len(mesh.assignedGameObjects) > 0):
                """for i, mgameObject in enumerate(mesh.assignedGameObjects):
                    model_transform = pyrr.matrix44.create_identity(dtype=np.float16)
                    model_transform = pyrr.matrix44.multiply(
                        m1=model_transform, 
                        m2=mgameObject.eulermat
                    )
                    model_transform = pyrr.matrix44.multiply(
                        m1=model_transform, 
                        m2=mgameObject.posmat
                    )
                    mesh.transforms[i] = model_transform
                """
            
                glBindVertexArray(mesh.objmesh.vao)
                glBindBuffer(
                    GL_ARRAY_BUFFER, 
                    mesh.transformVBO
                )
                glBufferData(GL_ARRAY_BUFFER, mesh.transforms.nbytes, mesh.transforms, GL_STATIC_DRAW)

                mesh.assignedGameObjects[0].material.matmat.use()
                glDisable(GL_CULL_FACE)
                glBindVertexArray(mesh.objmesh.vao)
                glBindBuffer(
                    GL_ARRAY_BUFFER, 
                    mesh.transformVBO
                )
                glDrawArraysInstanced(GL_TRIANGLES, 0, mesh.objmesh.vertex_count, len(mesh.assignedGameObjects))



        #self.gameMaterials[0].matmat.use()
        
        """for mesh in self.gameMeshes:
            if(len(mesh.assignedGameObjects) > 0):
                mesh.assignedGameObjects[0].material.matmat.use()
                glDisable(GL_CULL_FACE)
                glBindVertexArray(mesh.objmesh.vao)
                glBindBuffer(
                    GL_ARRAY_BUFFER, 
                    mesh.transformVBO
                )
                glDrawArraysInstanced(GL_TRIANGLES, 0, mesh.objmesh.vertex_count, len(mesh.assignedGameObjects))
        """

        #glDrawArraysInstanced(GL_TRIANGLES, 0, self.cube_mesh.vertex_count, len(scene.cubes))
        
        glUseProgram(self.shaderColored)
        
        glUniformMatrix4fv(self.viewLocUntextured, 1, GL_FALSE, view_transform)

        pg.display.flip()

    def quit(self):
        for mesh in self.gameMeshes:
            glDeleteBuffers(1, (mesh.transformVBO,))
        glDeleteProgram(self.shaderTextured)
        glDeleteProgram(self.shaderColored)
        pg.quit()





"""
class GameObject:
    def __init__(self, name, position, eulers, eulerVelocity, mesh, material):
        self.name = name
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
        self.eulerVelocity = np.array(eulerVelocity, dtype=np.float32)
        self.mesh = mesh
        if(self.mesh != None):
            self.mesh.assignGameObject(self)
        self.material = material
"""
        

class Light:
    def __init__(self, name, position, color):
        self.name = name
        self.position = np.array(position, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)

class Camera:
    def __init__(self, ifovy, iaspect, inear, ifar):
        self.fovy = ifovy
        self.aspect = iaspect
        self.near = inear
        self.far = ifar
    def setProperties(self, ifovy, iaspect, inear, ifar):
        self.fovy = ifovy
        self.aspect = iaspect
        self.near = inear
        self.far = ifar
    

class View:
    def __init__(self, horizontal_resolution, vertical_resolution):
        self.hres = horizontal_resolution
        self.vres = vertical_resolution
    def setProperties(self, horizontal_resolution, vertical_resolution):
        self.hres = horizontal_resolution
        self.vres = vertical_resolution

class Mesh:
    def __init__(self, filename):
        self.filename = filename
        self.assignedGameObjects = []
        self.transformVBO = None
        self.transform = None
        self.transformsCreated = False
    
    def assignGameObject(self, gameObject):
        self.assignedGameObjects.append(gameObject)

    def unassignGameObject(self, gameObject):
        if(gameObject in self.assignedGameObjects):
            self.assignedGameObjects.remove(gameObject)

    def loadNow(self):
        self.objmesh = obj.ObjMesh(self.filename)

class Matt:
    def __init__(self, filename, filetype):
        self.filename = filename
        self.filetype = filetype
        self.matmat = None
    
    def loadNow(self):
        self.matmat = mat.Material(self.filename, self.filetype)

game = Game()

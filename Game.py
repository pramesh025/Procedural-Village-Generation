import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import pyrr
import random
import Material as mat
import ObjMesh as obj
import Player as pl
# import Physics as phy

class Game:
    def __init__(self):
        #Place Game variables

        self.renderDistance = 10
        self.gravity = 9.8

        self.slowUpdateTime = 1
        

        self.mainInit()
        pass

    
    def start(self): #CALLED Before the first frame
        ####   list of created variables
        #  cubes =[8 cubes]
        #  lights = [8 lights]
        #  player
        ####   end of variable list
        self.ckeydown = False

        self.view.setProperties(800,600)
        self.camera.setProperties(45,800/600,0.1,40)
        self.player.setProperties(position = [5, 5, 1], eulers = [0, 0, 0])

        #self.gameMeshes["CubeMesh"] = Mesh("models/cube.obj")
        #self.gameMaterials["CrateMat"] = Matt("crate", "png")

        self.gameMeshes.append(Mesh("models/cube.obj")) # 0
        self.gameMeshes.append(Mesh("models/testmodel1.obj")) # 1

        self.gameMaterials.append(Matt("crate", "png")) # 0
        self.gameMaterials.append(Matt("wood", "png")) # 1
        self.gameMaterials.append(Matt("white", "png")) # 2

        
        #CREATING FLOATING SPINNING CRATES
        for i in range(10):
            self.gameObjects.append(GameObject(
                name = "cube " + str(i),
                position = [random.uniform(a = -5, b = 5), random.uniform(a = -5, b = 5), 5 ],
                eulers = [random.uniform(a = 0, b = 360) for x in range(3)],
                eulerVelocity = [random.uniform(a = -0.1, b = 0.1) for x in range(3)],
                mesh = self.gameMeshes[0], #Cube
                material = self.gameMaterials[0] #
            ))

        
        #CREATING ROOMS
        
        for i in range(10):
            for ii in range(5):
                self.gameObjects.append(GameObject(
                    name = "weird " + str(i),
                    position = [i*2, ii*2, 0],
                    eulers = [-90,0,random.randint(0,3) * 90],
                    eulerVelocity = [0,0,0],
                    mesh = self.gameMeshes[1], #Weird
                    material = self.gameMaterials[2] #white
                ))
            self.lights.append(Light(
                name = "light " + str(i),
                position = [i*2, ii*2, 1],
                color = [0.5,0.5,0.5]

                # color = [random.uniform(a = 0, b = 1) for x in range(3)]
            ))
            


        #EIGHT RANDOM LIGHTS
        for i in range(8):
            self.lights.append(Light(
                name = "light " + str(i),
                position = [random.uniform(a = -10, b = 10) for x in range(3)],
                # color = []
                color = [random.uniform(a = 0.5, b = 1) for x in range(3)]
            ))

        
        
        pass

    def slowUpdate(self): #called every certain amount of time
        pass

    def update(self): #Is called every frame
        ### mouse control ##
        (x,y) = pg.mouse.get_pos()
        theta_increment = self.frameTime * 0.05 * (320 - x)
        phi_increment = self.frameTime * 0.05 * (240 - y)
        self.player.increment_direction(theta_increment, phi_increment)
        pg.mouse.set_pos((320,240))

        ### keyboard control ###

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.player.move(0, self.speedMultiplier*self.frameTime)
            return
        if keys[pg.K_a]:
            self.player.move(90, self.speedMultiplier*self.frameTime)
            return
        if keys[pg.K_s]:
            self.player.move(180, self.speedMultiplier*self.frameTime)
            return
        if keys[pg.K_d]:
            self.player.move(-90, self.speedMultiplier*self.frameTime)
            return

        #Press c to put a crate where the player is
        if keys[pg.K_c]:
            if self.ckeydown == False:
                #doo thu stuff
                self.gameObjects.append(GameObject(
                    name = "cube extra",
                    position = self.player.position,
                    eulers = [random.uniform(a = 0, b = 360) for x in range(3)],
                    eulerVelocity = [random.uniform(a = -0.1, b = 0.1) for x in range(3)],
                    mesh = self.gameMeshes[0], #Cube
                    material = self.gameMaterials[0] #
                ))
                self.createTransform(self.gameMeshes[0])


                print("C key pressed!")
                self.ckeydown = True
        else:
            self.ckeydown = False
            
            


        ### Other stuff (add scene-object related things here) ###
        for cube in self.gameObjects:
            cube.eulers = np.mod(
                cube.eulers + cube.eulerVelocity, 
                [360, 360, 360], 
                dtype=np.float32
            )
        

        pass

    # def physics(self):
    #     # gravity
    #     self.player.move

    #Don't change things after here unless you know what you're doing -Rob

    def mainInit(self):
        self.lastTime = 0
        self.currentTime = 0
        self.numFrames = 0
        self.frameTime = 0
        self.speedMultiplier = 0.0025
        self.lightCount = 0

        self.gameObjects = []
        self.lights = []
        self.player = pl.Player(
            position = [-10, 0, 0],
            eulers = [0, 0, 0]
        )
        
        self.camera = Camera(45,640/480,0.1,40)
        self.view = View(800,600)

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

        #self.engine = Engine(self.scene)
        

        self.glStuffInit(self.camera, self.gameObjects)
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
            self.update()
            # self.physics()
            #refresh screen
            self.draw()
            self.showFrameRate()
        self.quit()
        pass

    def showFrameRate(self):
        self.currentTime = pg.time.get_ticks()
        delta = self.currentTime - self.lastTime
        if (delta >= 1000):
            framerate = int(1000.0 * self.numFrames/delta)
            pg.display.set_caption(f"Running at {framerate} fps.")
            self.lastTime = self.currentTime
            self.numFrames = -1
            if(framerate != 0):
                self.frameTime = float(1000.0 / framerate)
            else:
                self.frateTime = float(1000.0/1)
        self.numFrames += 1
    
    def glStuffInit(self, icamera, igameObjects):
         #initialise opengl
        glClearColor(0.1, 0.1, 0.1, 1)
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
        pass

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
            glUniform1f(self.lightLocTextured["strength"][i], 1)
        

        for mesh in self.gameMeshes:
            for i, mgameObject in enumerate(mesh.assignedGameObjects):
                model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
                model_transform = pyrr.matrix44.multiply(
                    m1=model_transform, 
                    m2=pyrr.matrix44.create_from_eulers(
                        eulers=np.radians(mgameObject.eulers), dtype=np.float32
                    )
                )
                model_transform = pyrr.matrix44.multiply(
                    m1=model_transform, 
                    m2=pyrr.matrix44.create_from_translation(
                        vec=np.array(mgameObject.position),dtype=np.float32
                    )
                )
                mesh.transforms[i] = model_transform
        
            glBindVertexArray(mesh.objmesh.vao)
            glBindBuffer(
                GL_ARRAY_BUFFER, 
                mesh.transformVBO
            )
            glBufferData(GL_ARRAY_BUFFER, mesh.transforms.nbytes, mesh.transforms, GL_STATIC_DRAW)


        #self.gameMaterials[0].matmat.use()
        
        for mesh in self.gameMeshes:
            mesh.assignedGameObjects[0].material.matmat.use()
            glDisable(GL_CULL_FACE)
            glBindVertexArray(mesh.objmesh.vao)
            glBindBuffer(
                GL_ARRAY_BUFFER, 
                mesh.transformVBO
            )
            glDrawArraysInstanced(GL_TRIANGLES, 0, mesh.objmesh.vertex_count, len(mesh.assignedGameObjects))


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
    
    def assignGameObject(self, gameObject):
        self.assignedGameObjects.append(gameObject)

    def loadNow(self):
        self.objmesh = obj.ObjMesh(self.filename)

class Matt:
    def __init__(self, filename, filetype):
        self.filename = filename
        self.filetype = filetype
        self.matmat = None
    
    def loadNow(self):
        self.matmat = mat.Material(self.filename, self.filetype)


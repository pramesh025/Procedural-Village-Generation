
import numpy as np
import pygame as pg


class GameObject:
    def __init__(self, name = "DefaultObject", position = [0,0,0], eulers = [0,0,0], eulerVelocity = [0,0,0], mesh = None, material = None, parent = None):
        self.name = name
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
        self.eulerVelocity = np.array(eulerVelocity, dtype=np.float32)
        self.setMesh(mesh)
        self.setMaterial(material)
        self.setParent(parent)
        self.children = []

    def setPosition(self, iposition):
        self.position = np.array(iposition, dtype=np.float32)
        for child in self.children:
            child.setPosition([iposition[i] + child.position[i] for i in range(3)])
        
    def setEulers(self, ieulers):
        self.eulers = np.array(ieulers, dtype=np.float32)
        for child in self.children:
            child.eulers([ieulers[i] + child.position[i] for i in range(3)])
    
    def setMesh(self, mesh):
        self.mesh = mesh
        

    def setMaterial(self, material):
        self.material = material

    def setParent(self, parentGameObject):
        self.parent = parentGameObject
    
    def setChild(self, childGameObject):
        self.children.append(childGameObject)


    def placeGameObject(self):
        if self.mesh != None:
            self.mesh.assignGameObject(self)

        self.mesh.transformsCreated = False
        for child in self.children:
            child.placeGameObject()
        pass

    def unplaceGameObject(self):
        for child in self.children:
            child.unplaceGameObject()
        self.mesh.transformscreated = False
        if self.mesh != None:
            self.mesh.unassignGameObject(self)
        del self
        pass

"""
class BuildingPartGameObjectList:
    #self.gameMeshes.append(Mesh("models/floorwood0.obj")) #WOOD FLOOR LEVEL 0 # 0
    #self.gameMeshes.append(Mesh("models/floorwoodL.obj")) #WOOD FLOOR L       # 1
    #self.gameMeshes.append(Mesh("models/floorwoodI.obj")) #WOOD FLOOR I       # 2
    #self.gameMeshes.append(Mesh("models/wallblank.obj"))  #BLANK WALL         # 3
    #self.gameMeshes.append(Mesh("models/wallwindowI.obj"))#1 WALL WITH WONDOW # 4
    #self.gameMeshes.append(Mesh("models/wallwindowL.obj"))#L WALL WITH WONDOW # 5
    #self.gameMeshes.append(Mesh("models/walldoorR.obj"))  #RIGHT DOOR         # 6
    #self.gameMeshes.append(Mesh("models/walldoorL.obj"))  #LEFT DOOR          # 7
    #self.gameMeshes.append(Mesh("models/windowbars.obj")) #WINDOW BARS        # 8
    #self.gameMeshes.append(Mesh("models/post.obj"))       #POST               # 9
    #self.gameMeshes.append(Mesh("models/windowbase.obj")) #WINDOW BASE        # 10

    
    #self.gameMaterials.append(Matt("floorwood", "png"))     #WOOD FLOOR       # 0
    #self.gameMaterials.append(Matt("stonewall", "png"))     #STONE WALL       # 1
    #self.gameMaterials.append(Matt("silver", "png"))        #SILVER METAL     # 2
    #self.gameMaterials.append(Matt("windowshutter", "png")) #WINDOW           # 3
    #self.gameMaterials.append(Matt("door", "png"))          #DOOR             # 4
    #self.gameMaterials.append(Matt("post", "png"))          #POST             # 5
    #self.gameMaterials.append(Matt("lantern", "png"))       #LANTERN          # 6

    #walls

    #EI (Square wooden floor with blank wall on one side)
    def cEI():
        EI = GameObject(name = "EI", mesh = main.game.gameMeshes[2], material=main.game.gameMaterials[0])          #FLOOR
        EI.setChild(GameObject(name = "EI", mesh = main.game.gameMeshes[3], material=main.game.gameMaterials[1]))  #WALL
        return EI


    #EL (Square wooden floor with two blank walls in an L shape)
    def cEL():
        EL = GameObject(name = "EI", mesh = main.game.gameMeshes[1], material=main.game.gameMaterials[0])          #FLOOR
        EL.setChild(GameObject(name = "EI", mesh = main.game.gameMeshes[3], material=main.game.gameMaterials[1]))  #WALL 1
        EL.setChild(GameObject(name = "EI", eulers=[0,0,90], mesh = main.game.gameMeshes[3], material=main.game.gameMaterials[1])) #Wall 2
        return EL

    #EWI (Square wooden floor with one windowed wall on one side)
    def cEWI():
        EWI = GameObject(name = "EI", mesh = main.game.gameMeshes[2], material=main.game.gameMaterials[0]) #FLOOR
        EWI.setChild(GameObject(name = "EI", mesh = main.game.gameMeshes[4], material=main.game.gameMaterials[1]))  #WALL
        EWI.setChild(GameObject(name = "EI", mesh = main.game.gameMeshes[8], material=main.game.gameMaterials[2]))  #BARS
        return EWI

    #EWL (Square wooden floor with two windowed wall in an L shape)
    def cEWL():
        EWL = GameObject(name = "EI", mesh = main.game.gameMeshes[2], material=main.game.gameMaterials[0]) #FLOOR
        EWL.setChild(GameObject(name = "EI", mesh = main.game.gameMeshes[4], material=main.game.gameMaterials[1]))  #WALL
        EWL.setChild(GameObject(name = "EI", mesh = main.game.gameMeshes[8], material=main.game.gameMaterials[2]))  #BARS

        EWL.setChild(GameObject(name = "EI", mesh = main.game.gameMeshes[4], material=main.game.gameMaterials[1]))  #WALL 2
        EWL.setChild(GameObject(name = "EI", mesh = main.game.gameMeshes[8], material=main.game.gameMaterials[2]))  #BARS 2
        return EWL





    pass"""
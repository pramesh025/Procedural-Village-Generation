import main
import numpy as np
import pygame as pg


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

        self.parent = None
        self.children = []

    def setPosition(self, iposition):
        self.position = np.array(iposition, dtype=np.float32)
        for child in self.children:
            child.setPosition([iposition[i] + child.position[i] for i in range(3)])
    
    def setParent(self, parentGameObject):
        self.parent = parentGameObject
    
    def setChild(self, childGameObject):
        self.children.append(childGameObject)

    def placeGameObject(self):
        main.game.gameObjects.append(self)
        self.mesh.transformsCreated = False
        for child in self.children:
            child.placeGameObject()
        pass

    def unplaceGameObject(self):
        for child in self.children:
            child.unplaceGameObject()
        self.mesh.transformscreated = False
        main.game.gameObjects.remove(self)
        pass
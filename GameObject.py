
import numpy as np
import pygame as pg
import pyrr


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

        self.eulermat = pyrr.matrix44.create_from_eulers(eulers = np.radians(self.eulers), dtype=np.float16)
        self.posmat = pyrr.matrix44.create_from_translation(
                            vec=np.array(self.position),dtype=np.float16
                        )

    def setPosition(self, iposition):
        self.position = np.array(iposition, dtype=np.float32)
        for child in self.children:
            child.setPosition([iposition[i] + child.position[i] for i in range(3)])
        self.posmat = pyrr.matrix44.create_from_translation(
                            vec=np.array(self.position),dtype=np.float16
                        )
        
        
    def setEulers(self, ieulers):
        self.eulers = np.array(ieulers, dtype=np.float32)
        for child in self.children:
            child.eulers([ieulers[i] + child.position[i] for i in range(3)])
        self.eulermat = pyrr.matrix44.create_from_eulers(eulers = np.radians(self.eulers), dtype=np.float16)
    
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


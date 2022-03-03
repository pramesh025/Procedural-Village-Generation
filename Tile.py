from pygame import Vector3
import GameObject

class BuildingPart:
    def __init__(self, gameObj, direction, lights, boxCollider, respectiveNode):  
        self.gameObj = GameObject
        self.direction = direction
        # self.theModel = mesh and material in GameObjects for now
        self.lights = []
        self.boxCollider = []
        self.respectiveNode = respectiveNode

    def addBuildingPart(self):
           # testing to add to gameObjs list
        for objects in self.gameObj:
            self.gameObjs.append(self.gameObj)
        
        
class Tile:
    def __init__(self, buildPart, worldCoord, tileCoord, neighbours):
        self.buildPart = BuildingPart
        self.worldCoord = worldCoord
        self.tileCoord = tileCoord
        self.neighbours = []

    def placeTile(self):
        self.gameObjects.append(self.tiles[0].buildPart.gameObj)



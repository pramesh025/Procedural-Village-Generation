
from pygame import Vector3
import GameObject as go
import Game as g

class BuildingPart:
    def __init__(self, builder) -> None:
        self.build = builder
        self.node = None
        pass


    pass

class BuildingPartList:
    #wood floor
    def __init__(self) -> None:
        self.woodFloor = BuildingPartList(self.CwoodFloor)
        self.windowI = BuildingPartList(self.CwindowI)

        pass

    def CwoodFloor(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = g.game.gameMeshes[3], #Weird
                    material = g.game.gameMaterials[3] #white
                )
        return tete
    
    def CwindowI(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = g.game.gameMeshes[3], #Weird
                    material = g.game.gameMaterials[3] #white
                )
        
        tete.setChild(go.GameObject(
                    name = "wall",
                    mesh = g.game.gameMeshes[2], #Weird
                    material = g.game.gameMaterials[0] #white
                ))
        return tete


    pass

class Tile:
    def __init__(self, tilecreator, node, position = Vector3(0,0,0)) -> None:
        self.position = position
        self.zenode = node
        self.buildingpart = node.buildingpart
        self.gameObject = None
        tilecreator.tilelist.append(self)
        self.neighbours = [None,None,None,None]
        self.neighbourpos = [self.position + Vector3(1,0,0), self.position + Vector3(0,1,0), self.position + Vector3(-1,0,0), self.position + Vector3(0,-1,0)]

    def placeTile(self, gameObjects):
        self.gameObject = self.buildingpart.build()
        self.gameObject.setPosition(self.position)
        self.gameObject.placeGameObject(gameObjects)
        
    def unplaceTile(self, gameObjects, tilecreator):
        tilecreator.tilelist.remove(self)
        if(self in tilecreator.edgetiles):
            tilecreator.edgetiles.remove(self)
        self.gameObject.unplaceGameObject(gameObjects)
        del self

        pass
    pass

class TileBuffer:
    def __init__(self, coords, buildingpart) -> None:
        pass
    pass

class TileCreator:
    def __init__(self) -> None:
        self.buipuilist = BuildingPartList()
        self.tilelist = []
        self.edgetiles = []
        self.buffertiles = []
        self.edgebuffers = []

        pass

    def createInitial(self, playerPos):
        firsttile = Tile(tilecreator = self, buildingpart = self.buipuilist.woodFloor, 
            position=Vector3(int(playerPos.x), int(playerPos.y, 0)))

        self.tilelist.append(firsttile)
        self.edgetiles.append(firsttile)
        firsttile.placeTile()

        pass

    def iterateTileCreation(self, playerPos):

        pass


    def createBuffers(self, playerPos):
        currentPos = Vector3(int(playerPos.x), int(playerPos.y, 0))
        for etile in self.edgetiles:
            
            for i in range(4):
                if etile.neighbours[i] == None:
                    if (etile.neighbourpos[i] - currentPos).magnitude_squared <= 10:

                        pass



        pass

    pass


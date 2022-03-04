
from pygame import Vector3
import GameObject as go
import ZeGraph as zg

class Tile:
    def __init__(self, tilecreator, node, position = Vector3(0,0,0)) -> None:
        self.position = position
        self.zenode = node
        self.gameObject = self.zenode.buildingpart.build()
        tilecreator.tilelist.append(self)
        self.neighbours = [None,None,None,None]
        self.neighbourpos = [self.position + Vector3(1,0,0), 
                            self.position + Vector3(0,1,0), 
                            self.position + Vector3(-1,0,0), 
                            self.position + Vector3(0,-1,0)]

    def placeTile(self):
        self.gameObject.setPosition(self.position)
        self.gameObject.placeGameObject()
        
    def unplaceTile(self, tilecreator):
        tilecreator.tilelist.remove(self)
        if(self in tilecreator.edgetiles):
            tilecreator.edgetiles.remove(self)
        self.gameObject.unplaceGameObject()
        del self

        pass
    pass

class TileBuffer:
    def __init__(self, coords, buildingpart) -> None:
        pass
    pass

class TileCreator: #SINGLETON
    def __init__(self, igameMeshes, igameMaterials) -> None:
        self.tilelist = []
        self.edgetiles = []
        self.buffertiles = []
        self.edgebuffers = []

        self.zeGraph = zg.ZeGraph(igameMeshes, igameMaterials)
        

        pass

    def createInitial(self, playerPos):
        firsttile = Tile(tilecreator = self, node = self.zeGraph.nodes[0], #playground
            position=Vector3(int(playerPos.x), int(playerPos.y), 0))

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



class NodeMinHeap:
    def __init__(self) -> None:
        self.theHeap = []
    
    def push(self, pushThis):
        self.theHeap.append(pushThis) 
        self.minHeapify(len(self.theHeap) - 1)

    def remove(self, removeThis):
        self.theHeap.remove(removeThis)
        self.minHeapify(len(self.theHeap) - 1)
        pass


    def root(self):
        return self.theHeap[0]

    def minHeapify(self, k):
        p = int((k-1)/2)
        while(p < len(self.theHeap) and self.theHeap[k].getEntropy() < self.theHeap[p].getEntropy()): #Make getEntropy
            self.theHeap[k], self.theHeap[p] = self.theHeap[p], self.theHeap[k]
            k = int((k-1)/2)
    pass

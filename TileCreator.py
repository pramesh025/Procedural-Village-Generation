
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
        firsttile = Tile(tilecreator = self, node = self.zeGraph.nodes[0], 
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

class MaxHeap:
    def __init__(self):
        # Initialize a heap using list
        self.heap = []

    def getParentPosition(self, i):
        # The parent is located at floor((i-1)/2)
        return int((i-1)/2)

    def getLeftChildPosition(self, i):
        # The left child is located at 2 * i + 1
        return 2*i+1

    def getRightChildPosition(self, i):
        # The right child is located at 2 * i + 2
        return 2*i+2

    def hasParent(self, i):
        # This function checks if the given node has a parent or not
        return self.getParentPosition(i) < len(self.heap)

    def hasLeftChild(self, i):
        # This function checks if the given node has a left child or not
        return self.getLeftChildPosition(i) < len(self.heap)

    def hasRightChild(self, i):
        # This function checks if the given node has a right child or not
        return self.getRightChildPosition(i) < len(self.heap)

    def insert(self, key):
        self.heap.append(key) # Adds the key to the end of the list
        self.heapify(len(self.heap) - 1) # Re-arranges the heap to maintain the heap property

    def getMax(self):
        return self.heap[0] # Returns the largest value in the heap in O(1) time.

    def heapify(self, i):
        while(self.hasParent(i) and self.heap[i] > self.heap[self.getParentPosition(i)]): # Loops until it reaches a leaf node
            self.heap[i], self.heap[self.getParentPosition(i)] = self.heap[self.getParentPosition(i)], self.heap[i] # Swap the values
            i = self.getParentPosition(i) # Resets the new position

    def printHeap(self):
        print(self.heap) # Prints the heap
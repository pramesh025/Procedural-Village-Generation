
from random import randint, choice
from pygame import Vector3
import GameObject as go
import ZeGraph as zg

class Tile:
    def __init__(self, tilecreator, index) -> None:
        self.position = Vector3(index[0],index[1],0)
        self.index = index
        self.neighbourindex = [ (index[0]+1,index[1]),  # 0 towards x axis
                                (index[0],index[1]+1),  # 1 towards y axis
                                (index[0]-1,index[1]),  # 2 towards -x axis
                                (index[0],index[1]-1)]  # 3 towards -y axis
        self.neighbour = [None, None, None, None]
        self.zenode = 0
        self.possiblenodes = None
        self.possiblenodeweights = None
        self.orientation = 0 #side of GameObject that faces 0 (x axis) in the world

    def placeTile(self, nodes):
        self.gameObject = nodes[self.zenode].buildingpart.build()
        #self.gameObject.setEulers([0,90*self.orientation,0])
        self.gameObject.setOrientation(self.orientation)
        self.gameObject.setPosition(self.position)
        self.gameObject.placeGameObject()
        
    def unplaceTile(self):
        self.gameObject.unplaceGameObject()
        del self

    def collapse(self):
        if len(self.possiblenodes) > 0:
            #tte = choice(self.possiblenodes)
            #print("collapsing at ", self.index)
            rinrin = randint(0, self.possiblenodeweights[-1])
            #print("rinrin is ", rinrin)
            tte = self.possiblenodes[0]
            for i in range(0, len(self.possiblenodes)):
                if rinrin <= self.possiblenodeweights[i]:
                    tte = self.possiblenodes[i]
                    break

            #print("selected node is ", tte)
            self.zenode = tte[0]
            self.orientation = tte[1]
        else:
            self.zenode = 0
            self.orientation = 0

    pass

class TileCreator: #SINGLETON
    def __init__(self, igameMeshes, igameMaterials) -> None:
        self.tiles = {}
        self.edgetiles = {}

        self.zeGraph = zg.ZeGraph(igameMeshes, igameMaterials)
        

        pass

    def createInitial(self, playerPos):
        firsttile = Tile(tilecreator = self, index=(int(playerPos.x), int(playerPos.y)))
        firsttile.zenode = 1
        firsttile.orientation = 0
        self.tiles[firsttile.index] = firsttile
        self.edgetiles[firsttile.index] = firsttile
        firsttile.placeTile(self.zeGraph.nodes)

        """secondtile = Tile(tilecreator = self, index=(int(playerPos.x)+2, int(playerPos.y)))
        secondtile.zenode = 11
        secondtile.orientation = 0
        self.tiles[secondtile] = secondtile
        self.edgetiles[secondtile.index] = secondtile
        secondtile.placeTile(self.zeGraph.nodes)

        midtile = Tile(tilecreator = self, index=(int(playerPos.x)+1, int(playerPos.y)))
        self.generatePossibleNodes(midtile)
        #print(midtile.possiblenodes)"""
        


        pass

    def generatePossibleNodes(self, thetile):

        towards = []

        tn = thetile.neighbourindex[0]
        if self.tiles.get(tn):
            towards.append((self.tiles[tn].zenode, (self.tiles[tn].orientation + 2) % 4))
        else:
            towards.append((0,0))
        
        tn = thetile.neighbourindex[1]
        if self.tiles.get(tn):
            towards.append((self.tiles[tn].zenode, (self.tiles[tn].orientation + 3) % 4))
        else:
            towards.append((0,0))

        tn = thetile.neighbourindex[2]
        if self.tiles.get(tn):
            towards.append((self.tiles[tn].zenode, self.tiles[tn].orientation))
        else:
            towards.append((0,0))
        
        tn = thetile.neighbourindex[3]
        if self.tiles.get(tn):
            towards.append((self.tiles[tn].zenode, (self.tiles[tn].orientation + 1) % 4))
        else:
            towards.append((0,0))

        #print("towards:", towards)

        thetile.possiblenodes, thetile.possiblenodeweights = self.zeGraph.possiblilites(towards)

    def fillTiles(self, playerPos, renderdist = 5):
        pass



        
    def iterateTileCreation(self, playerPos, renderdist = 5):


        toGenerate = set()
        #toRemoveFromEdge = set()
        #toTurnIntoEdge = set()
        toDelete = set()

        """for tileindex in self.edgetiles:
            if self.getTaxicabDist(tileindex, playerPos) > renderdist:
                #make every neighbour already present in tiles an edgetile
                for i in range(4):
                    if self.edgetiles[tileindex].neighbourindex[i] in self.tiles:
                        toTurnIntoEdge.add(self.edgetiles[tileindex].neighbourindex[i])
                
                #delete the current tile
                toDelete.add(tileindex)
                pass
            else:
                #generate every neighbour within limits and not already in tiles
                #if all neighbours were generated or were in tiles, remove tileindex from edge
            

            #generate waiting tiles, randomly"""

        for tileindex in self.tiles:
            if self.getTaxicabDist(tileindex, playerPos) > renderdist:
                ##print(tileindex, " is outside limits")
                toDelete.add(tileindex)
            else:
                ##print(tileindex, " is within limits")
                for i in range(4):
                    ##print("Checking neighbour ", i)
                    if not self.tiles[tileindex].neighbourindex[i] in self.tiles:
                        ##print("Neighbour doesn't exist")
                        if self.getTaxicabDist(self.tiles[tileindex].neighbourindex[i], playerPos) <= renderdist:
                            ##print("Neighbour inside limits, generating")
                            #self.tiles[tileindex].neighbour[i] = Tile(self, self.tiles[tileindex].neighbourindex[i])
                            ##print("Adding neighbour to generation set")
                            toGenerate.add(self.tiles[tileindex].neighbourindex[i])


                        
        while len(toDelete) > 0:
            
            tt = toDelete.pop()
            #print("removing at ", tt)
            ttt = self.tiles.pop(tt)
            ttt.unplaceTile()

        while len(toGenerate) > 0:
            tt = toGenerate.pop()
            #print("generating at", tt)
            self.tiles[tt] = Tile(self, tt)
            self.generatePossibleNodes(self.tiles[tt])
            self.tiles[tt].collapse()
            self.tiles[tt].placeTile(self.zeGraph.nodes)

        #print("iteration complete")

            

    def getTaxicabDist(self, tileIndex, playerPosition):
        return pow(tileIndex[0] - playerPosition.x,2) + pow(tileIndex[1] - playerPosition.y,2)

    def isWithinLimits(self, tile, limits):
        return tile[0] > limits[2] and tile[0] < limits[0] and tile[1] > limits[3] and tile[1] < limits[1]
                    

    """
    def iterateTileCreationOLD(self, playerPos, renderdist = 5):
        limits = [int(playerPos.x) + renderdist,
                    int(playerPos.y) + renderdist,
                    int(playerPos.x) - renderdist,
                    int(playerPos.y) - renderdist]

        topop = set()
        towithin = set()
        toremove = set()
        toedge = set()

        #List collapsables
        for tile in self.edgetiles.values():
            if not self.isWithinLimits(tile.index, limits):
                for i in range(4):
                    if tile.neighbourindex[i] in self.tiles:
                        toedge.add(tile.neighbourindex[i])
                        
                toremove.add(tile.index)

            else:
                staysedge = False
                for i in range(4):
                    ii = tile.neighbourindex[i]
                    if self.isWithinLimits(ii, limits):
                        if not ii in self.tiles:
                            topop.add(ii)
                            #self.tiles[ii]
                    else:
                        staysedge = True
                
                if not staysedge:
                    towithin.add(tile.index)
                    #self.edgetiles.pop(tile.index)
        #edge
        while len(toedge) > 0:
            tt = toedge.pop()
            self.edgetiles[tt] = self.tiles[tt]


        #remove
        while len(toremove) > 0:
            tt = toremove.pop()
            self.edgetiles.pop(tt)
            self.tiles.pop(tt)
            tile.unplaceTile() #PROBLEM


        #within
        while len(towithin) > 0:
            tt = towithin.pop()
            self.edgetiles.pop(tt)

        #Collapse
        while len(topop) > 0:
            ind = topop.pop()
            self.tiles[ind] = Tile(self, ind)
            self.edgetiles[ind] = self.tiles[ind]

            towards = []
            tn = self.tiles[ind].neighbourindex[0]
            if(tn in self.tiles):
                towards.append((self.tiles[tn].zenode, (self.tiles[tn].orientation + 2) % 4))
            else:
                towards.append((0,0))
            
            tn = self.tiles[ind].neighbourindex[1]
            if(tn in self.tiles):
                towards.append((self.tiles[tn].zenode, (self.tiles[tn].orientation + 3) % 4))
            else:
                towards.append((0,0))

            tn = self.tiles[ind].neighbourindex[2]
            if(tn in self.tiles):
                towards.append((self.tiles[tn].zenode, self.tiles[tn].orientation))
            else:
                towards.append((0,0))
            
            tn = self.tiles[ind].neighbourindex[3]
            if(tn in self.tiles):
                towards.append((self.tiles[tn].zenode, (self.tiles[tn].orientation + 1) % 4))
            else:
                towards.append((0,0))
            

            self.tiles[ind].possiblenodes = self.zeGraph.possiblilites(towards)
            if len(self.tiles[ind].possiblenodes) == 0:
                self.tiles[ind].possiblenodes.append(0)
            tte = choice(self.tiles[ind].possiblenodes)
            self.tiles[ind].zenode = tte[0]
            self.tiles[ind].orientation = tte[1]

            self.tiles[ind].placeTile(self.zeGraph.nodes)

        pass

    def isWithinLimits(self, tile, limits):
        
        return tile[0] > limits[2] and tile[0] < limits[0] and tile[1] > limits[3] and tile[1] < limits[1]






    def createBuffers(self, playerPos):
        currentPos = Vector3(int(playerPos.x), int(playerPos.y, 0))
        for etile in self.edgetiles:
            
            for i in range(4):
                if etile.neighbours[i] == None:
                    if (etile.neighbourpos[i] - currentPos).magnitude_squared <= 10:

                        pass



        pass

    pass"""



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


from random import randint
from secrets import choice
from pygame import Vector3
import GameObject as go
import Graph as zg

class Tile:
    def __init__(self, tilecreator, index, node = 0, orientation = 0, place = False, poss = None, wt = None) -> None:
        self.position = Vector3(index[0],index[1],0)
        self.index = index
        self.neighbourindex = [ (index[0]+1,index[1]),  # 0 towards x axis
                                (index[0],index[1]+1),  # 1 towards y axis
                                (index[0]-1,index[1]),  # 2 towards -x axis
                                (index[0],index[1]-1)]  # 3 towards -y axis
        self.zenode = node
        self.possiblenodes = poss
        self.possiblenodeweights = wt
        self.orientation = orientation #side of GameObject that faces 0 (x axis) in the world
        if place:
            self.placeTile(tilecreator.zeGraph.nodes)

    def getEntropy(self):
        return self.possiblenodeweights[-1]

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
            rinrin = randint(0, self.possiblenodeweights[-1])
            tte = self.possiblenodes[0]
            for i in range(0, len(self.possiblenodes)):
                if rinrin <= self.possiblenodeweights[i]:
                    tte = self.possiblenodes[i]
                    break
            self.zenode = tte[0]
            self.orientation = tte[1]

        else:
            self.zenode = 0
            self.orientation = 0

    pass



class Yard:
    def __init__(self, coords):
        self.coords = coords
        self.worldcoords = (self.coords[0]*5, self.coords[1]*5)
        self.seed = 1
        tet = randint(1,10)
        if tet > 5:
            self.seed = 2
    
    def generateSandYard(self, tc):
        x, y = self.worldcoords[0], self.worldcoords[1]
        nodes = tc.zeGraph.nodes
        for i in range(-1,2):
            for ii in range(-1,2):
                tc.tiles[(x+i, y+ii)] = Tile(tilecreator=tc, index=(x+i,y+ii), node=2, place=True)

        #                                          X T T T X
        #                                          T T T T T
        #   Generating these tiles:                T T S T T
        #                                          T T T T T
        #                                          X T T T X


        temp = Tile(tilecreator=tc, index=(x+2,y+2))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp

        temp = Tile(tilecreator=tc, index=(x-2,y+2))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp

        temp = Tile(tilecreator=tc, index=(x-2,y-2))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp

        temp = Tile(tilecreator=tc, index=(x+2,y-2))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp
        
        for i in range(3):
            temp = Tile(tilecreator=tc, index=(x-2,y-1+i))
            tc.generatePossibleNodes(temp)
            temp.collapse()
            temp.placeTile(nodes)
            tc.tiles[temp.index] = temp

            temp = Tile(tilecreator=tc, index=(x+2,y-1+i))
            tc.generatePossibleNodes(temp)
            temp.collapse()
            temp.placeTile(nodes)
            tc.tiles[temp.index] = temp

            temp = Tile(tilecreator=tc, index=(x-1+i,y-2))
            tc.generatePossibleNodes(temp)
            temp.collapse()
            temp.placeTile(nodes)
            tc.tiles[temp.index] = temp

            temp = Tile(tilecreator=tc, index=(x-1+i,y+2))
            tc.generatePossibleNodes(temp)
            temp.collapse()
            temp.placeTile(nodes)
            tc.tiles[temp.index] = temp

       



    def generateYard(self, tc):
        if self.seed == 2:
            self.generateSandYard(tc)
            return

        tc.tiles[self.worldcoords] = Tile(tilecreator=tc, index=self.worldcoords, node=self.seed, place=True)
        
        x, y = self.worldcoords[0], self.worldcoords[1]
        nodes = tc.zeGraph.nodes

        seedI = 0
        if self.seed == 1: seedI = 1

        #                                          X
        #  Generating these tiles directly:      X S X     (S is seed, X is tile to be generated)
        #                                          X

        temp = Tile(tilecreator=tc, index=(x+1, y), poss=tc.seedPossibilities[seedI][0], wt=tc.seedWeights[seedI])
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[(x + 1, y)] = temp

        temp = Tile(tilecreator=tc, index=(x, y+1), poss=tc.seedPossibilities[seedI][1], wt=tc.seedWeights[seedI])
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[(x, y + 1)] = temp

        temp = Tile(tilecreator=tc, index=(x-1, y), poss=tc.seedPossibilities[seedI][2], wt=tc.seedWeights[seedI])
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[(x - 1, y)] = temp

        temp = Tile(tilecreator=tc, index=(x, y-1), poss=tc.seedPossibilities[seedI][3], wt=tc.seedWeights[seedI])
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[(x, y - 1)] = temp

        #                                        X T X
        #  Generating these tiles:               T S T
        #                                        X T X

        temp = Tile(tilecreator=tc, index=(x+1,y+1))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp

        temp = Tile(tilecreator=tc, index=(x-1,y+1))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp

        temp = Tile(tilecreator=tc, index=(x-1,y-1))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp

        temp = Tile(tilecreator=tc, index=(x+1,y-1))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp


        #                                            X X X
        #                                          X T T T X
        #   Generating these tiles:                X T S T X
        #                                          X T T T X
        #                                            X X X

        for i in range(3):
            temp = Tile(tilecreator=tc, index=(x-2,y-1+i))
            tc.generatePossibleNodes(temp)
            temp.collapse()
            temp.placeTile(nodes)
            tc.tiles[temp.index] = temp

            temp = Tile(tilecreator=tc, index=(x+2,y-1+i))
            tc.generatePossibleNodes(temp)
            temp.collapse()
            temp.placeTile(nodes)
            tc.tiles[temp.index] = temp

            temp = Tile(tilecreator=tc, index=(x-1+i,y-2))
            tc.generatePossibleNodes(temp)
            temp.collapse()
            temp.placeTile(nodes)
            tc.tiles[temp.index] = temp

            temp = Tile(tilecreator=tc, index=(x-1+i,y+2))
            tc.generatePossibleNodes(temp)
            temp.collapse()
            temp.placeTile(nodes)
            tc.tiles[temp.index] = temp

        #                                          X T T T X
        #                                          T T T T T
        #   Generating these tiles:                T T S T T
        #                                          T T T T T
        #                                          X T T T X


        temp = Tile(tilecreator=tc, index=(x+2,y+2))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp

        temp = Tile(tilecreator=tc, index=(x-2,y+2))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp

        temp = Tile(tilecreator=tc, index=(x-2,y-2))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp

        temp = Tile(tilecreator=tc, index=(x+2,y-2))
        tc.generatePossibleNodes(temp)
        temp.collapse()
        temp.placeTile(nodes)
        tc.tiles[temp.index] = temp


    def removeYard(self, tc):
        x, y = self.worldcoords[0], self.worldcoords[1]
        for i in range(-2,3):
            for ii in range(-2,3):
                tc.tiles[(x+i, y+ii)].unplaceTile()






class TileCreator: #SINGLETON
    def __init__(self, igameMeshes, igameMaterials) -> None:
        self.tiles = {}
        self.yards = {}

        self.zeGraph = zg.ZeGraph(igameMeshes, igameMaterials)

        #PrecalculatedTemps
        self.seedPossibilities = [[[(2, 0), (3, 3), (4, 0), (5, 3), (6, 0), (7, 0), (8, 0), (10, 3), (11, 3)], #SAND
                                [(2, 0), (3, 2), (4, 3), (5, 2), (6, 3), (7, 3), (8, 3), (10, 2), (11, 2)],
                                [(2, 0), (3, 1), (4, 2), (5, 1), (6, 2), (7, 2), (8, 2), (10, 1), (11, 1)],
                                [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (10, 0), (11, 0)]],

                                [[(1, 0), (3, 1), (5, 1), (9, 0), (12, 2)],  #FLOOR
                                [(1, 0), (3, 0), (5, 0), (9, 0), (12, 0)],
                                [(1, 0), (3, 3), (5, 3), (9, 0), (12, 0)],
                                [(1, 0), (3, 2), (5, 2), (9, 0), (12, 3)]]]

        self.seedWeights = [[250, 258, 262, 270, 274, 278, 282, 286, 290], #SAND
                            [150, 158, 166, 167, 177]] #FLOOR
    
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


        thetile.possiblenodes, thetile.possiblenodeweights = self.zeGraph.possiblilites(towards)

    def generateCurrentYard(self, playerPos):
        yardx, yardy = int(playerPos.x/5), int(playerPos.y/5)
        self.yards[(yardx, yardy)] = Yard((yardx, yardy))
        self.yards[(yardx, yardy)].generateYard(self)


    def fillYards(self, playerPos, renderdist = 50):
        yardx, yardy = int(playerPos.x/5), int(playerPos.y/5)
        toGenerate = set()
        toRemove = set()
        for yardindex in self.yards:
            if not self.yardInLimits(yardindex, playerPos, 2):
                toRemove.add(yardindex)

        while len(toRemove) > 0:
            tt = toRemove.pop()
            self.yards[tt].removeYard(self)
            self.yards.pop(tt)
        
        for i in range(-2,3):
            for ii in range(-2,3):
                if not ((yardx-i, yardy+ii) in self.yards):
                    toGenerate.add((yardx-i, yardy+ii))


        while len(toGenerate) > 0:
            tt = toGenerate.pop()
            self.yards[tt] = Yard(tt)
            self.yards[tt].generateYard(self)

        pass

    
    def yardSqDist(self, yardindex, playerPos):
        return (yardindex[0]*5 - playerPos.x)**2 + (yardindex[1]*5 - playerPos.y)**2

    def yardInLimits(self, yardindex, playerPos, d):
        return yardindex[0] >= int(playerPos.x/5)-d and yardindex[0] <= int(playerPos.x/5)+d and yardindex[1] >= int(playerPos.y/5)-d and yardindex[1] <= int(playerPos.y/5)+d

        
    def iterateTileCreation(self, playerPos, renderdist = 5):

        toGenerate = set()
        #toRemoveFromEdge = set()
        #toTurnIntoEdge = set()
        toDelete = []

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
                toDelete.append(tileindex)
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

        waitingTiles = TileMinHeap()
        
        while len(toGenerate) > 0:
            tt = toGenerate.pop()
            #print("generating at", tt)
            self.tiles[tt] = Tile(self, tt)
            self.generatePossibleNodes(self.tiles[tt])
            waitingTiles.pushTile(self.tiles[tt])
            #self.tiles[tt].collapse()
            #self.tiles[tt].placeTile(self.zeGraph.nodes)

        print("Entropies", [x.getEntropy() for x in waitingTiles.theHeap])
        for tile in waitingTiles.theHeap:
            tile.collapse()
            tile.placeTile(self.zeGraph.nodes)

        #print("iteration complete")

            

    def getTaxicabDist(self, tileIndex, playerPosition):
        return pow(tileIndex[0] - playerPosition.x,2) + pow(tileIndex[1] - playerPosition.y,2)

    def isWithinLimits(self, tile, limits):
        return tile[0] > limits[2] and tile[0] < limits[0] and tile[1] > limits[3] and tile[1] < limits[1]
                    

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




class TileMinHeap:
    def __init__(self) -> None:
        self.theHeap = []
    
    def push(self, pushThis):
        self.theHeap.append(pushThis) 
        n = int((len(self.theHeap)//2)-1)
        for k in range(n, -1, -1):
            self.minHeapify(k)

    def remove(self, removeThis):
        self.theHeap.remove(removeThis)
        self.minHeapify(len(self.theHeap) - 1)
        pass

    def poproot(self):
        p = int((len(self.theHeap)-1)/2)
        min = self.theHeap.pop(p)
        self.minHeapify(p)
        return min

    def minHeapify(self, k):
        p = int((k-1)/2)
        while(p < len(self.theHeap) and self.theHeap[k].getEntropy() < self.theHeap[p].getEntropy()): #Make getEntropy
            self.theHeap[k], self.theHeap[p] = self.theHeap[p], self.theHeap[k]
            k = int((k-1)/2)
    pass

    def pushTile(self, pushThis):
        for i in range(len(self.theHeap)):
            if pushThis.getEntropy() <= self.theHeap[i].getEntropy():
                self.theHeap.insert(i, pushThis)
                return
        self.theHeap.append(pushThis)

    def pop(self):
        return self.theHeap.pop(0)
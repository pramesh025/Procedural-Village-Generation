from random import randint
import GameObject as go


class BuildingPart:
    def __init__(self, builder) -> None:
        self.build = builder
        self.node = None
        pass


class ZeNode:
    def __init__(self, name, buildingpart, weight) -> None:
        self.name = name
        self.buildingpart = buildingpart
        self.nexts = None  #[[],[],[],[]], Directions: 0 is x, 1 is y, 2 is -x, 3 is -y
        self.weight = weight
        pass
    pass


class ZeGraph: #SINGLETON
    def __init__(self, gameMeshes, gameMaterials) -> None:
        self.nodes = []
        self.allnodes = [1,2,3,4,5,6,7,8,9,10,11]
        self.gm = gameMeshes
        self.gmm = gameMaterials
        self.weightSum = 0

        #create all the building-part build functions
        self.addNode(ZeNode("Playground", BuildingPart(self.Cplayground),10))              #0   TESTING

        self.addNode(ZeNode("WoodFloor", BuildingPart(self.CwoodFloor),20))                #1   WoodFloor
        self.addNode(ZeNode("Sand", BuildingPart(self.Csand),50))                          #2   Sand
        self.addNode(ZeNode("WallI", BuildingPart(self.CwallI),8))                         #3   Wall I
        self.addNode(ZeNode("WallL", BuildingPart(self.CwallL),3))                         #4   Wall L
        self.addNode(ZeNode("WindowI", BuildingPart(self.CwindowI),4))                     #5   Window I
        self.addNode(ZeNode("WindowLDouble", BuildingPart(self.CwindowLDouble),3))         #6   Window DOUBLE
        self.addNode(ZeNode("WindowLL", BuildingPart(self.CwindowLL),4))                   #7   Window LL
        self.addNode(ZeNode("WindowLR", BuildingPart(self.CwindowLR),4))                   #8   Window LR
        self.addNode(ZeNode("Lamp", BuildingPart(self.Clamp),1))                           #9   Lamp
        self.addNode(ZeNode("DoorR", BuildingPart(self.CdoorR),2))                         #10  DoorR
        self.addNode(ZeNode("DoorL", BuildingPart(self.CdoorL),2))                         #11  DoorL

        

        #Directions: 0 is x, 1 is y, 2 is -x, 3 is -y
        self.nodes[0].nexts = [ {1,2,3,4,5,6,7,8,9,10,11},  #0, x
                                {1,2,3,4,5,6,7,8,9,10,11},  #1, y
                                {1,2,3,4,5,6,7,8,9,10,11},  #2, -x
                                {1,2,3,4,5,6,7,8,9,10,11}]  #4, -y

        self.nodes[1].nexts = [ {1,3,4,5,6,7,8,9},  #0, x
                                {1,3,4,5,6,7,8,9},  #1, y
                                {1,3,4,5,6,7,8,9},  #2, -x
                                {1,3,4,5,6,7,8,9}]  #4, -y

        self.nodes[2].nexts = [ {2,3,4,5,6,7,8,10,11},  #0, x
                                {2,3,4,5,6,7,8,10,11},  #1, y
                                {2,3,4,5,6,7,8,10,11},  #2, -x
                                {2,3,4,5,6,7,8,10,11}]  #4, -y

        self.nodes[3].nexts = [ {3,4,5,6,7,8,10,11},  #0, x
                                {2},  #1, y
                                {3,4,5,6,7,8,10,11},  #2, -x
                                {1,3,4,5,6,7,8,9,10,11}]  #4, -y

        self.nodes[4].nexts = [ {3,4,5,6,7,8,10,11},  #0, x
                                {2},  #1, y
                                {2},  #2, -x
                                {3,4,5,6,7,8,10,11}]  #4, -y

        self.nodes[5].nexts = [ {3,4,5,6,7,8,10,11},  #0, x
                                {2},  #1, y
                                {3,4,5,6,7,8,10,11},  #2, -x
                                {1,3,4,5,6,7,8,9,10,11}]  #4, -y

        self.nodes[6].nexts = [ {3,4,5,6,7,8,10,11},  #0, x
                                {2},  #1, y
                                {2},  #2, -x
                                {3,4,5,6,7,8,10,11}]  #4, -y

        self.nodes[7].nexts = [ {3,4,5,6,7,8,10,11},  #0, x
                                {2},  #1, y
                                {2},  #2, -x
                                {3,4,5,6,7,8,10,11}]  #4, -y      

        self.nodes[8].nexts = [ {3,4,5,6,7,8,10,11},  #0, x
                                {2},  #1, y
                                {2},  #2, -x
                                {3,4,5,6,7,8,10,11}]  #4, -y                  

        self.nodes[9].nexts = [ {1,3,4,5,6,7,8,9},  #0, x
                                {1,3,4,5,6,7,8,9},  #1, y
                                {1,3,4,5,6,7,8,9},  #2, -x
                                {1,3,4,5,6,7,8,9}]  #4, -y
        
        self.nodes[10].nexts = [{11},  #0, x
                                {2},  #1, y
                                {1,3,4,5,6,7,8,9},  #2, -x
                                {3,4,5,6,7,8}]  #4, -y
        
        self.nodes[11].nexts = [{3,4,5,6,7,8},  #0, x
                                {2},  #1, y
                                {10},  #2, -x
                                {1,3,4,5,6,7,8,9}]  #4, -y

        pass

    def addNode(self, theNode):
        self.nodes.append(theNode)
        self.weightSum += theNode.weight
        pass

    pass

    def possiblilites(self, towards = [(0,0), (0,0),(0,0),(0,0)]):
        """
        returns a list in form of [(node, dir), (node, dir)...], where
        node is a possible node to place in the tile surrounded by
        towards (towards[0] being in the 0 direction), and dir is the
        direction of the possible that should be pointing to towards[0]
        """
        res = self.nodes[towards[0][0]].nexts[towards[0][1]].copy()
        """#print(res)
        #print("intersection with")
        #print(self.nodes[towards[1][0]].nexts[towards[1][1]])
        #print(self.nodes[towards[2][0]].nexts[towards[2][1]])
        #print(self.nodes[towards[3][0]].nexts[towards[3][1]])"""

        res = res.intersection(self.nodes[towards[1][0]].nexts[towards[1][1]],
                        self.nodes[towards[2][0]].nexts[towards[2][1]],
                        self.nodes[towards[3][0]].nexts[towards[3][1]])

        ##print(res)

        res2 = []
        weights = []
        tempweightsum = 0
        ##print("for res 0")
        for p in res:
            ##print("for res", p)
            ##print("towards 0 and nexts[0]", towards[0][0], self.nodes[p].nexts[0])
            ##print("towards 1 and nexts[1]", towards[1][0], self.nodes[p].nexts[1])
            ##print("towards 2 and nexts[2]", towards[2][0], self.nodes[p].nexts[2])
            ##print("towards 3 and nexts[3]", towards[3][0], self.nodes[p].nexts[3])
            #res2.append((p,randint(0,3)))
            #continue

            if ((towards[0][0] in self.nodes[p].nexts[0] or towards[0][0] == 0)
                and (towards[1][0] in self.nodes[p].nexts[1] or towards[1][0] == 0)
                and (towards[2][0] in self.nodes[p].nexts[2] or towards[2][0] == 0)
                and (towards[3][0] in self.nodes[p].nexts[3] or towards[3][0] == 0)):
                res2.append((p, 0))
                tempweightsum += self.nodes[p].weight
                weights.append(tempweightsum)
                continue

            if ((towards[1][0] in self.nodes[p].nexts[0] or towards[1][0] == 0)
                and (towards[2][0] in self.nodes[p].nexts[1] or towards[2][0] == 0)
                and (towards[3][0] in self.nodes[p].nexts[2] or towards[3][0] == 0)
                and (towards[0][0] in self.nodes[p].nexts[3] or towards[0][0] == 0)):
                res2.append((p, 3))
                tempweightsum += self.nodes[p].weight
                weights.append(tempweightsum)
                continue

            if ((towards[2][0] in self.nodes[p].nexts[0] or towards[2][0] == 0)
                and (towards[3][0] in self.nodes[p].nexts[1] or towards[3][0] == 0)
                and (towards[0][0] in self.nodes[p].nexts[2] or towards[0][0] == 0)
                and (towards[1][0] in self.nodes[p].nexts[3] or towards[1][0] == 0)):
                res2.append((p, 2))
                tempweightsum += self.nodes[p].weight
                weights.append(tempweightsum)
                continue

            if ((towards[3][0] in self.nodes[p].nexts[0] or towards[3][0] == 0)
                and (towards[0][0] in self.nodes[p].nexts[1] or towards[0][0] == 0)
                and (towards[1][0] in self.nodes[p].nexts[2] or towards[1][0] == 0)
                and (towards[2][0] in self.nodes[p].nexts[3] or towards[2][0] == 0)):
                res2.append((p, 1))
                tempweightsum += self.nodes[p].weight
                weights.append(tempweightsum)
                continue

        if len(res2) == 0: 
            res2.append((0,0))
            weights.append(10)
        #print(res2, weights)
        return res2, weights

    def entropy(self, node):
        return 1
        pass

    #Building part building functions
    def Cplayground(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[2], #FLOOR
                    material = self.gmm[0] #WOOD
                )

        tete.setChild(go.GameObject(
            name = "post",
            position = [-0.5,0.5,0],
            mesh = self.gm[11], #POST
            material = self.gmm[5] #POST
         ))
        tete.setChild(go.GameObject(
            name = "post",
            position = [0.5,0.5,0],
            mesh = self.gm[11], #POST
            material = self.gmm[5] #POST
         ))
        tete.setChild(go.GameObject(
            name = "post",
            position = [0.5,-0.5,0],
            mesh = self.gm[11], #POST
            material = self.gmm[5] #POST
         ))
        tete.setChild(go.GameObject(
            name = "post",
            position = [-0.5,-0.5,0],
            mesh = self.gm[11], #POST
            material = self.gmm[5] #POST
         ))

        tete.setChild(go.GameObject(
            name = "wall",
            position = [0,-0.04,0],
            eulers = [0,0,0],
            mesh = self.gm[3], #WALL
            material = self.gmm[1] #WALL
        ))
        tete.setChild(go.GameObject(
            name = "wall",
            position = [0.04,0,0],
            eulers = [0,-90,0],
            mesh = self.gm[3], #WALL
            material = self.gmm[1] #WALL
        ))
        tete.setChild(go.GameObject(
            name = "wall",
            position = [0,0.04,0],
            eulers = [0,-180,0],
            mesh = self.gm[3], #WALL
            material = self.gmm[1] #WALL
        ))
        tete.setChild(go.GameObject(
            name = "wall",
            position = [-0.04,0,0],
            eulers = [0,90,0],
            mesh = self.gm[3], #WALL
            material = self.gmm[1] #WALL
        ))
        

        return tete


    def CwoodFloor(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[0], #FLOOR
                    material = self.gmm[0] #WOOD
                )
        return tete

    def Csand(self):
        tete = go.GameObject(
                    name = "sand",
                    mesh = self.gm[14], #SAND
                    material = self.gmm[7] #SAND
                )
        return tete

    def CwallI(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[2], #FLOOR I
                    material = self.gmm[0] #WOOD
                )
        tete.setChild(go.GameObject(
            name = "wall",
            position = [0,-0.04,0],
            eulers = [0,0,0],
            mesh = self.gm[3], #WALL
            material = self.gmm[1] #WINDOW
        ))

        return tete

    def CwallL(self):
        tete = go.GameObject(
                    name = "floor",
                    position = [0,0,0],
                    eulers = [0,0,0],
                    mesh = self.gm[1], #FLOOR
                    material = self.gmm[0] #WOOD
                )
                #Post
        tete.setChild(go.GameObject(
            name = "post",
            position = [-0.5,0.5,0],
            mesh = self.gm[11], #POST
            material = self.gmm[5] #POST
         ))

        tete.setChild(go.GameObject(
            name = "wall",
            position = [0,-0.04,0],
            eulers = [0,0,0],
            mesh = self.gm[3], #WALL
            material = self.gmm[1] #WALL
        ))
        tete.setChild(go.GameObject(
            name = "wall",
            position = [0.04,0,0],
            eulers = [0,-90,0],
            mesh = self.gm[3], #WALL
            material = self.gmm[1] #WALL
        ))
        return tete
        

    def CwindowI(self):
        windowI = go.GameObject(
                    name = "floor",
                    mesh = self.gm[2], #FLOOR
                    material = self.gmm[0] #WOOD
                )
        windowI.setChild(go.GameObject(
                    name = "wall",
                    position = [0,-0.04,0],
                    mesh = self.gm[4], #WALL WITH WINDOW HOLE
                    material = self.gmm[1] #WALL
                ))
        windowI.setChild(go.GameObject(
            name = "windowL",
            position = [-0.5,0,1.1],
            eulers = [0,30,0],
            mesh = self.gm[5], #WINDOW
            material = self.gmm[4] #WINDOW
        ))
        windowI.setChild(go.GameObject(
            name = "windowR",
            position = [0.5,0,1.1],
            eulers = [0,-30,0],
            mesh = self.gm[5], #WINDOW
            material = self.gmm[4] #WINDOW
        ))
        windowI.setChild(go.GameObject(
            name = "window bars",
            position = [0,0,0],
            mesh = self.gm[9], #WINDOW BARS
            material = self.gmm[2] #METAL
        ))
        windowI.setChild(go.GameObject(
            name = "window base",
            position = [0,-0.15,0.8],
            mesh = self.gm[12], #WINDOW BASE
            material = self.gmm[8] #STONE
        ))
        
        return windowI

    def CwindowLDouble(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[1], #FLOOR
                    material = self.gmm[0] #WOOD
                )
                #Post
        tete.setChild(go.GameObject(
            name = "post",
            position = [-0.5,0.5,0],
            mesh = self.gm[11], #POST
            material = self.gmm[5] #POST
         ))
        #First wall
        tete.setChild(go.GameObject(
            name = "wall",
            position = [0,-0.04,0],
            mesh = self.gm[4], #WALL WITH WINDOW HOLE
            material = self.gmm[1] #WALL
         ))
        tete.setChild(go.GameObject(
            name = "windowL",
            position = [-0.05,0,1.1],
            eulers = [0,-30,0],
            mesh = self.gm[5], #WINDOW
            material = self.gmm[4] #WINDOW
        ))
        tete.setChild(go.GameObject(
            name = "windowR",
            position = [0.5,0,1.1],
            eulers = [0,-30,0],
            mesh = self.gm[5], #WINDOW
            material = self.gmm[4] #WINDOW
        ))
        tete.setChild(go.GameObject(
            name = "window bars",
            position = [0,0,0],
            mesh = self.gm[9], #WINDOW BARS
            material = self.gmm[2] #METAL
        ))
        tete.setChild(go.GameObject(
            name = "window base",
            position = [0,-0.15,0.8],
            mesh = self.gm[12], #WINDOW BASE
            material = self.gmm[8] #STONE
        ))

        #Second Wall
        tete.setChild(go.GameObject(
            name = "wall",
            position = [0.04,0,0],
            eulers = [0,-90,0],
            mesh = self.gm[4], #WALL WITH WINDOW HOLE
            material = self.gmm[1] #WALL
         ))
        tete.setChild(go.GameObject(
            name = "windowL",
            position = [0,-0.5,1.1],
            eulers = [0,30-90,0],
            mesh = self.gm[5], #WINDOW
            material = self.gmm[4] #WINDOW
        ))
        tete.setChild(go.GameObject(
            name = "windowR",
            position = [0,0.1,1.1],
            eulers = [0,25-90,0],
            mesh = self.gm[5], #WINDOW
            material = self.gmm[4] #WINDOW
        ))
        tete.setChild(go.GameObject(
            name = "window bars",
            position = [0,0,0],
            eulers = [0,-90,0],
            mesh = self.gm[9], #WINDOW BARS
            material = self.gmm[2] #METAL
        ))
        tete.setChild(go.GameObject(
            name = "window base",
            position = [0.15,0,0.8],
            eulers = [0,-90,0],
            mesh = self.gm[12], #WINDOW BASE
            material = self.gmm[8] #STONE
        ))
        return tete

    def CwindowLL(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[1], #FLOOR
                    material = self.gmm[0] #WOOD
                )

        #Post
        tete.setChild(go.GameObject(
            name = "post",
            position = [-0.5,0.5,0],
            mesh = self.gm[11], #POST
            material = self.gmm[5] #POST
         ))
        #First wall

        tete.setChild(go.GameObject(
            name = "wall",
            position = [0,-0.04,0],
            mesh = self.gm[4], #WALL WITH WINDOW HOLE
            material = self.gmm[1] #WALL
         ))
        tete.setChild(go.GameObject(
            name = "windowL",
            position = [-0.25,-0.1,1.1],
            eulers = [0,0,0],
            mesh = self.gm[5], #WINDOW
            material = self.gmm[4] #WINDOW
        ))
        tete.setChild(go.GameObject(
            name = "windowR",
            position = [0.48,0,1.1],
            eulers = [0,-30,0],
            mesh = self.gm[5], #WINDOW
            material = self.gmm[4] #WINDOW
        ))
        tete.setChild(go.GameObject(
            name = "window bars",
            position = [0,0,0],
            mesh = self.gm[9], #WINDOW BARS
            material = self.gmm[2] #METAL
        ))
        tete.setChild(go.GameObject(
            name = "window base",
            position = [0,-0.15,0.8],
            mesh = self.gm[12], #WINDOW BASE
            material = self.gmm[8] #STONE
        ))

        #Second Wall
        tete.setChild(go.GameObject(
            name = "wall",
            position = [0.04,0,0],
            eulers = [0,-90,0],
            mesh = self.gm[3], #WALL WITH WINDOW HOLE
            material = self.gmm[1] #WALL
         ))
        return tete

    def CwindowLR(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[1], #FLOOR
                    material = self.gmm[0] #WOOD
                )
        #Post
        tete.setChild(go.GameObject(
            name = "post",
            position = [-0.5,0.5,0],
            mesh = self.gm[11], #POST
            material = self.gmm[5] #POST
         ))


        #First wall
        tete.setChild(go.GameObject(
            name = "wall",
            position = [0,-0.04,0],
            mesh = self.gm[3], #WALL WITH WINDOW HOLE
            material = self.gmm[1] #WALL
         ))

        #Second Wall
        tete.setChild(go.GameObject(
            name = "wall",
            position = [0.04,0,0],
            eulers = [0,-90,0],
            mesh = self.gm[4], #WALL WITH WINDOW HOLE
            material = self.gmm[1] #WALL
         ))
        tete.setChild(go.GameObject(
            name = "windowL",
            position = [0,-0.5,1.1],
            eulers = [0,30-90,0],
            mesh = self.gm[5], #WINDOW
            material = self.gmm[4] #WINDOW
        ))
        tete.setChild(go.GameObject(
            name = "windowR",
            position = [0,0.1,1.1],
            eulers = [0,25-90,0],
            mesh = self.gm[5], #WINDOW
            material = self.gmm[4] #WINDOW
        ))
        tete.setChild(go.GameObject(
            name = "window bars",
            position = [0,0,0],
            eulers = [0,-90,0],
            mesh = self.gm[9], #WINDOW BARS
            material = self.gmm[2] #METAL
        ))
        tete.setChild(go.GameObject(
            name = "window base",
            position = [0.15,0,0.8],
            eulers = [0,-90,0],
            mesh = self.gm[12], #WINDOW BASE
            material = self.gmm[8] #STONE
        ))
        return tete
    
    def Clamp(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[0], #FLOOR
                    material = self.gmm[0] #WOOD
                )
        #Post
        tete.setChild(go.GameObject(
            name = "post",
            position = [0,-0.1,0],
            mesh = self.gm[11], #POST
            material = self.gmm[5] #POST
         ))

        #lamp
        tete.setChild(go.GameObject(
            name = "post",
            position = [0,-0.1,1.5],
            mesh = self.gm[13], #POST
            material = self.gmm[6] #POST
         ))

        return tete

    def CdoorR(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[2], #FLOOR
                    material = self.gmm[0] #WOOD
                )
        #Post
        tete.setChild(go.GameObject(
            name = "post",
            position = [-0.5,0.5,0],
            mesh = self.gm[11], #POST
            material = self.gmm[5] #POST
         ))

        #lamp
        tete.setChild(go.GameObject(
            name = "lamp",
            position = [-0.2,0.5,1.5],
            mesh = self.gm[13], #POST
            material = self.gmm[6] #POST
         ))

        tete.setChild(go.GameObject(
            name = "wall",
            position = [0,-0.04,0],
            eulers = [0,0,0],
            mesh = self.gm[6], #WALL
            material = self.gmm[1] #WINDOW
        ))

        tete.setChild(go.GameObject(
            name = "doorbars",
            position = [0,0.4,1.4],
            eulers = [0,0,0],
            mesh = self.gm[10], #WALL
            material = self.gmm[2] #WINDOW
        ))

        tete.setChild(go.GameObject(
            name = "door",
            position = [0,0.37,0.8],
            eulers = [0,30,0],
            mesh = self.gm[8], #WALL
            material = self.gmm[4] #WINDOW
        ))

        return tete
    
    def CdoorL(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[2], #FLOOR
                    material = self.gmm[0] #WOOD
                )
        #Post
        tete.setChild(go.GameObject(
            name = "post",
            position = [0.5,0.5,0],
            mesh = self.gm[11], #POST
            material = self.gmm[5] #POST
         ))

        #lamp
        tete.setChild(go.GameObject(
            name = "lamp",
            position = [0.2,0.5,1.5],
            mesh = self.gm[13], #POST
            material = self.gmm[6] #POST
         ))

        tete.setChild(go.GameObject(
            name = "wall",
            position = [0,-0.04,0],
            eulers = [0,0,0],
            mesh = self.gm[7], #WALL
            material = self.gmm[1] #WINDOW
        ))

        tete.setChild(go.GameObject(
            name = "doorbars",
            position = [0,0.48,1.4],
            eulers = [0,180,0],
            mesh = self.gm[10], #WALL
            material = self.gmm[2] #WINDOW
        ))

        tete.setChild(go.GameObject(
            name = "door",
            position = [0,0.37,0.8],
            eulers = [0,-30,0],
            mesh = self.gm[8], #WALL
            material = self.gmm[4] #WINDOW
        ))

        return tete
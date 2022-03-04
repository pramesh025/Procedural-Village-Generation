import GameObject as go


class BuildingPart:
    def __init__(self, builder) -> None:
        self.build = builder
        self.node = None
        pass


class ZeNode:
    def __init__(self, name, buildingpart) -> None:
        self.name = name
        self.buildingpart = buildingpart
        self.nexts = [[],[],[],[]] #Directions: 0 is x, 1 is y, 2 is -x, 3 is -y
        pass
    pass


class ZeGraph: #SINGLETON
    def __init__(self, gameMeshes, gameMaterials) -> None:
        self.nodes = []

        self.gm = gameMeshes
        self.gmm = gameMaterials

        #create all the building-part build functions
        self.addNode(ZeNode("Playground", BuildingPart(self.Cplayground)))  #0

        self.addNode(ZeNode("WoodFloor", BuildingPart(self.CwoodFloor)))    #1
        self.addNode(ZeNode("WindowI", BuildingPart(self.CwindowI)))        #2




        pass

    def addNode(self, theNode):
        self.nodes.append(theNode)
        pass

    pass

    def entropy(self, node):
        return 1
        pass

    #Building part building functions
    def Cplayground(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[0], #FLOOR
                    material = self.gmm[0] #WOOD
                )
        return tete


    def CwoodFloor(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[0], #FLOOR
                    material = self.gmm[0] #WOOD
                )
        return tete
        

    def CwindowI(self):
        windowI = go.GameObject(
                    name = "floor",
                    mesh = self.gm[0], #FLOOR
                    material = self.gmm[0] #WOOD
                )
        windowI.setChild(go.GameObject(
                    name = "wall",
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



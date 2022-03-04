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
        self.addNode(ZeNode("WallI", BuildingPart(self.CwallI)))            #3
        self.addNode(ZeNode("WallL", BuildingPart(self.CwallL)))            #4




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
                    mesh = self.gm[1], #FLOOR
                    material = self.gmm[0] #WOOD
                )

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
            position = [0,0.05,1.1],
            eulers = [0,30-90,0],
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


    def CwoodFloor(self):
        tete = go.GameObject(
                    name = "floor",
                    mesh = self.gm[0], #FLOOR
                    material = self.gmm[0] #WOOD
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



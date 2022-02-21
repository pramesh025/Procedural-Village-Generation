import numpy as np

class physics:
    def __init__(self,position):
        self.gravity = 9.81
        self.position = np.array(position,dtype=np.float32)


    def pull_down(self,amount):
        # if(self.position[2] > 0):
        print(self.position)
        self.position[2] -= amount*self.gravity
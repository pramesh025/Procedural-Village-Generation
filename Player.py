
from OpenGL.GL import *
import numpy as np
from pygame import Vector3


class Player:
    def __init__(self, position, eulers):
        self.position = Vector3(position)
        self.eulers = Vector3(eulers)
        self.moveSpeed = 1
        self.global_up = Vector3(0, 0, 1)
        self.isGravity = True
        self.gravity = Vector3(0, 0, -2.5)
    
    def setProperties(self, position, eulers):
        self.position = Vector3(position)
        self.eulers = Vector3(eulers)
        self.moveSpeed = 1
        self.global_up = Vector3(0, 0, 1)
        self.isGravity = True

    def rotate(self, vector, angle):
        pass


    def move(self, direction, amount):
        walkDirection = (direction + self.eulers[1]) % 360
        self.position[0] += amount * self.moveSpeed * np.cos(np.radians(walkDirection),dtype=np.float32)
        self.position[1] += amount * self.moveSpeed * np.sin(np.radians(walkDirection),dtype=np.float32)
        if(self.isGravity):
            self.pull_down(amount)

    def increment_direction(self, theta_increase, phi_increase):
        self.eulers[1] = (self.eulers[1] + theta_increase) % 360
        self.eulers[0] = min(max(self.eulers[0] + phi_increase,-89),89)

    def pull_down(self,amount):
        if(self.position[2] > -0.1):
            print(self.position)
            self.position[2] += amount*self.gravity[2]
    
    def pull_up(self,amount):
        if(self.position[2] < 13):
            print(self.position)
            self.position[2] += amount*1
    
    def jump(self,amount):
        self.position[2] += amount*1
        return

    def get_forwards(self):

        return np.array(
            [
                #x = cos(theta) * cos(phi)
                np.cos(
                    np.radians(
                        self.eulers[1]
                    ),dtype=np.float32
                ) * np.cos(
                    np.radians(
                        self.eulers[0]
                    ),dtype=np.float32
                ),

                #y = sin(theta) * cos(phi)
                np.sin(
                    np.radians(
                        self.eulers[1]
                    ),dtype=np.float32
                ) * np.cos(
                    np.radians(
                        self.eulers[0]
                    ),dtype=np.float32
                ),

                #x = sin(phi)
                np.sin(
                    np.radians(
                        self.eulers[0]
                    ),dtype=np.float32
                )
            ], dtype = np.float32
        )
    
    def get_up(self):

        forwards = self.get_forwards()
        right = np.cross(
            a = forwards,
            b = self.global_up
        )

        return np.cross(
            a = right,
            b = forwards,
        )

    def updateToArray(self):
        self.position = np.array(self.position,dtype=np.float32)


# here lies the backup if the above vector3 start slowing down
        
# class Player:
#     def __init__(self, position, eulers):
#         self.position = np.array(position,dtype=np.float32)
#         self.eulers = np.array(eulers,dtype=np.float32)
#         self.moveSpeed = 1
#         self.global_up = np.array([0, 0, 1], dtype=np.float32)
    
#     def setProperties(self, position, eulers):
#         self.position = np.array(position,dtype=np.float32)
#         self.eulers = np.array(eulers,dtype=np.float32)
#         self.moveSpeed = 1
#         self.global_up = np.array([0, 0, 1], dtype=np.float32)

#     def rotate(self, vector, angle):
#         pass


#     def move(self, direction, amount):
#         walkDirection = (direction + self.eulers[1]) % 360
#         self.position[0] += amount * self.moveSpeed * np.cos(np.radians(walkDirection),dtype=np.float32)
#         self.position[1] += amount * self.moveSpeed * np.sin(np.radians(walkDirection),dtype=np.float32)

#     def increment_direction(self, theta_increase, phi_increase):
#         self.eulers[1] = (self.eulers[1] + theta_increase) % 360
#         self.eulers[0] = min(max(self.eulers[0] + phi_increase,-89),89)

#     def pull_down(self,amount):
#         if(self.position[2] > -0.52):
#             print(self.position)
#             self.position[2] -= amount*1
    
#     def pull_up(self,amount):
#         if(self.position[2] < 13):
#             print(self.position)
#             self.position[2] += amount*1
    

#     def get_forwards(self):

#         return np.array(
#             [
#                 #x = cos(theta) * cos(phi)
#                 np.cos(
#                     np.radians(
#                         self.eulers[1]
#                     ),dtype=np.float32
#                 ) * np.cos(
#                     np.radians(
#                         self.eulers[0]
#                     ),dtype=np.float32
#                 ),

#                 #y = sin(theta) * cos(phi)
#                 np.sin(
#                     np.radians(
#                         self.eulers[1]
#                     ),dtype=np.float32
#                 ) * np.cos(
#                     np.radians(
#                         self.eulers[0]
#                     ),dtype=np.float32
#                 ),

#                 #x = sin(phi)
#                 np.sin(
#                     np.radians(
#                         self.eulers[0]
#                     ),dtype=np.float32
#                 )
#             ], dtype = np.float32
#         )
    
#     def get_up(self):

#         forwards = self.get_forwards()
#         right = np.cross(
#             a = forwards,
#             b = self.global_up
#         )

#         return np.cross(
#             a = right,
#             b = forwards,
#         )

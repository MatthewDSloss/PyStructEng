import numpy as np

DOF_COUNT = 0


class NODE:
    def __init__(self, name: str, x_coord: float, y_coord: float, z_coord: float = 0):
        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.z_coord = z_coord
        self.dofs = [DOF('dx', self.x_coord, self.y_coord, self.z_coord),
                     DOF('dy', self.x_coord, self.y_coord, self.z_coord),
                     DOF('dz', self.x_coord, self.y_coord, self.z_coord),
                     DOF('rx', self.x_coord, self.y_coord, self.z_coord),
                     DOF('ry', self.x_coord, self.y_coord, self.z_coord),
                     DOF('rz', self.x_coord, self.y_coord, self.z_coord)]


class DOF:
    def __init__(self, dof_type: str, x_coord: float, y_coord: float, z_coord: float):
        global DOF_COUNT
        self.dof_type = dof_type
        self.index = DOF_COUNT
        DOF_COUNT += 1
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.z_coord = z_coord


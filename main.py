from typing import Dict, Any

import numpy as np
import sympy as sp

DOF_COUNT: int = 0
MODIFIER: float = 10 ** 6


class NODE:
    def __init__(self, name: str, x_coord: float, y_coord: float, z_coord: float = 0):
        self.node_displacements = []
        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.z_coord = z_coord
        self.dofs = {'dx': DOF('dx', self.x_coord, self.y_coord, self.z_coord),
                     'dy': DOF('dy', self.x_coord, self.y_coord, self.z_coord),
                     'dz': DOF('dz', self.x_coord, self.y_coord, self.z_coord),
                     'rx': DOF('rx', self.x_coord, self.y_coord, self.z_coord),
                     'ry': DOF('ry', self.x_coord, self.y_coord, self.z_coord),
                     'rz': DOF('rz', self.x_coord, self.y_coord, self.z_coord)}

    def __repr__(self):
        return f'Node {self.name}: ({self.x_coord} {self.y_coord} {self.z_coord})'

    def get_active_dofs(self) -> dict:
        return {name: node for (name, node) in self.dofs.items() if node.is_active}

    def activate_dof(self, dof_names: str) -> None:
        if dof_names == 'all':
            self.activate_dof('dx dy dz rx ry rz')
        else:
            for dof in dof_names.split():
                self.dofs[dof].is_active = True

    def deactivate_dof(self, dof_names: str) -> None:
        if dof_names == 'all':
            self.deactivate_dof('dx dy dz rx ry rz')
        else:
            for dof in dof_names.split():
                self.dofs[dof].is_active = False

    def update_nodes(self, displacement_matrix: np.ndarray) -> None:
        for key in {name: node for (name, node) in self.dofs.items() if node.is_active}:
            self.dofs[key].displacement = displacement_matrix[self.dofs[key].index]

    def get_displacements(self):
        for key in self.dofs.keys():
            self.node_displacements.append(self.dofs[key].displacement)


class DOF:
    def __init__(self, dof_type: str, x_coord: float, y_coord: float, z_coord: float):
        global DOF_COUNT
        self.dof_type = dof_type
        self.index = DOF_COUNT
        DOF_COUNT += 1
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.z_coord = z_coord
        self.is_active: bool = False
        self.displacement: float = 0.0

    def __repr__(self):
        return f'{self.index}: {self.dof_type} {self.is_active}'


class MATERIAL:
    def __init__(self, material_curve: sp.Piecewise or sp.Expr, is_moving_origin: bool = False):
        self.s: float = 0.0
        self.v: float = 0.0
        self.material_curve = material_curve
        self.is_moving_origin = is_moving_origin

    def update_material_stiffness(self, v_current: float, tan_or_sec: str = 'tan'):
        self.v = v_current
        self.s = self.material_curve.evalf(subs={v: self.v})
        if tan_or_sec == 'sec':
            return self.s / self.v
        elif tan_or_sec == 'tan':
            return sp.diff(self.material_curve).evalf(subs={v: self.v})


class XYTruss:
    def __init__(self, name: str, node_i: NODE, node_j: NODE, material: MATERIAL, area: float):
        self.name = name
        self.node_i = node_i
        self.node_j = node_j
        self.nodes = [node_i, node_j]
        self.material = material
        self.area = area

        for node in self.nodes:
            node.activate_dof('dx dy')

        dx = node_j.x_coord - node_i.x_coord
        dy = node_j.y_coord - node_i.y_coord
        self.L = np.sqrt(dx ** 2 + dy ** 2)

        self.cos = dx / self.L
        self.sin = dy / self.L

        self.gamma: float = 0.0
        self.updated_L: float = 0.0

class MODEL():
    def __init__(self, name: str)
        self.name = name
        self.elements = {}
        self.nodal_loads = {}


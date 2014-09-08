from __future__ import division # normal division
from second_order_ode import *
from boundary_conditions import *
import numpy
from bvp_ode import *
from bvp_pde import *
from coupled_pde import *
from specie_collector import *
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import math
import sys
import numpy as np

class SpecieCollector(object):
    """docstring for SpecieCollector"""
    def __init__(self):
        self.all ={}
    
    def add_specie(self, specie, D, w, dt, T, bc_x0_type, bc_x0_value, bc_xn_type, bc_xn_value, init_concentrations, x_min, x_max, num_x_nodes):
        self.all[specie] = self.create_single_container(D, w, dt, T, bc_x0_type, bc_x0_value, bc_xn_type, bc_xn_value, init_concentrations, x_min, x_max, num_x_nodes)

    def create_single_container(self, D, w, dt, T, bc_x0_type, bc_x0_value, bc_xn_type, bc_xn_value, init_concentrations, x_min, x_max, num_x_nodes):
        """Create dict for specie"""
        container =  {'D': D, 'w':w, 'dt':dt, 'T':T, 'x_min':x_min, 'x_max':x_max, 
                    'num_x_nodes':num_x_nodes,'bc_x0_type': bc_x0_type, 'bc_x0_value':bc_x0_value,
                    'bc_xn_type':bc_xn_type, 'bc_xn_value': bc_xn_value, 
                    'init_concentrations': init_concentrations }
        container['pde'] = self.create_pde(container)
        return container

    def create_pde(self, specie):
        """Create pde from specie container(dict)
        specie dict {'D': D, 'w':w, 'dt':dt, 'T':T, 'bc_x0_type': bc_x0_type, 'bc_x0_value':bc_x0_value, 'bc_xn_type':bc_xn_type, 'bc_xn_value': bc_xn_value, 'init_concentrations': init_concentrations}"""

        def model_prob_1(x):
            return 0

        ode = SecondOrderOde1D(specie['D'], specie['w'], 0, model_prob_1, 0, specie['x_min'] , specie['x_max'])
        bc = BoundaryConditions1D()
        if specie['bc_x0_type'] == 'Dirichlet': bc.set_x0_dirichlet_bc(specie['bc_x0_value'])
        if specie['bc_x0_type'] == 'Neumann'  : bc.set_x0_neumann_bc(specie['bc_x0_value'])
        if specie['bc_xn_type'] == 'Dirichlet': bc.set_xn_dirichlet_bc(specie['bc_xn_value'])
        if specie['bc_xn_type'] == 'Neumann'  : bc.set_xn_neumann_bc(specie['bc_xn_value'])
        return BvpPde1D(ode, bc, specie['dt'], 0, specie['T'], specie['num_x_nodes'], specie['init_concentrations'])


    def differentiate1Ts(self):
        for specie in self.all:
            self.all[specie]['pde'].differentiate_1TS_pde()

    def reaction_term(self):
        pass

    def create_rate_law_formulas_for_each_specie(self):
        pass
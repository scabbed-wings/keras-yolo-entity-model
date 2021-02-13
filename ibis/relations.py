import numpy as np

class relation:
    def __init__(self, ind_inp, ind_out, ind_box, dist):
        self.ind_inp = ind_inp
        self.ind_out = ind_out
        self.ind_box = ind_box
        self.dist = dist
    
    def __getattribute__(self, name):
        return super().__getattribute__(name)
    

def used_attribute(relations, index):

    for i in relations:
        if(i.ind_inp == index or i.ind_out == index):
            return True
            
    return False


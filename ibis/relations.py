import numpy as np

class relation:
    def __init__(self, ind_inp, ind_out, ind_box, dist):
        self.ind_inp = ind_inp
        self.ind_out = ind_out
        self.ind_box = ind_box
        self.dist = dist
    
    def __getattribute__(self, name):
        return super().__getattribute__(name)
    

def used_attribute(relations, index): #Search if the attribute has been added previously

    for i in relations:
        if(i.ind_inp == index or i.ind_out == index):
            return True
            
    return False

def condition_satisfied(obt_relations, id_box, ind_class, out_classes): #Search if an entity and a relation fulfill their conditions on the entity model
    find = False
    counter = 0
    for elem in obt_relations:
        if ind_class == 1:
            if((elem.ind_inp == id_box or elem.ind_out == id_box) and (out_classes[elem.ind_inp] == 2 or out_classes[elem.ind_out] == 2)):
                find = True
            elif((elem.ind_inp == id_box or elem.ind_out == id_box) and (out_classes[elem.ind_inp] == 1 or out_classes[elem.ind_out])):
                counter += 1
    
    if counter >= 2 and counter <= 3:
        find = True
    elif counter > 3:
        find = -1
    
    return find




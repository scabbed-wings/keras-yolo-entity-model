import numpy as np

class Relation:
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

def add_solution(obt_relations, new_relation, cont_elem):
    change_sol = False
    for i, elem in enumerate(obt_relations):
        j = i=0
        while(j < len(obt_relations)):
            if(elem.ind_box != obt_relations[j].ind_box) and ((elem.ind_inp == obt_relations[j].ind_inp and elem.ind_out == obt_relations[j].ind_out) 
             or (elem.ind_inp == obt_relations[j].ind_out and elem.ind_out == obt_relations[j].ind_inp)):
                if(new_relation.dist < obt_relations[j].dist and not change_sol):
                    obt_relations.pop(j)
                    obt_relations.append(new_relation)
                    change_sol = True
            j += 1
    
    if(not change_sol and len(obt_relations) < cont_elem):
        obt_relations.append(new_relation)
    
    return obt_relations

def delete_max_relation(obt_relations, id_relation):
    ind = -1
    dist = 0
    for i, elem in enumerate(obt_relations):
        if elem.ind_out == id_relation or elem.ind_inp == id_relation:
            if ind == -1:
                ind = i
                dist = elem.dist
            elif elem.dist > dist:
                dist = elem.dist
                ind = i
    
    obt_relations.pop(ind)

    return obt_relations

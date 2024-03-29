import numpy as np
from PIL import Image
import os
import ibis.relations
import ibis.box


def min_dist_array(possible_dist, bbox):
    max_ind = -1
    max_dist = 0

    for i, elem in enumerate(possible_dist):
        if max_ind == -1:
            max_ind = i
            max_dist = elem.dist
        elif elem.dist > max_dist:
            max_ind = i
            max_dist = elem.dist
    
    if bbox.dist < max_dist:
        possible_dist[max_ind] = bbox
    
    return possible_dist

def sort_dist_array(possible_dist):
    for i, elem in enumerate(possible_dist):
        j = i+1
        while(j < len(possible_dist)):
            if possible_dist[i].dist > possible_dist[j].dist:
                aux = possible_dist[j]
                possible_dist[j] = possible_dist[i]
                possible_dist[i] = aux
            j+=1
    
    return possible_dist


def create_relations(out_boxes, out_classes, non_connections, box, obt_relations, im_dim, ind_box):
    box1_pos = ibis.box.init_locations(box)

    possible_inter = []
    possible_dist = []

    
    for elem in non_connections:
        if out_classes[elem] == 0: #Attributees detection
            if not ibis.relations.used_attribute(obt_relations, elem):
                box2 = out_boxes[elem]
                box2_pos = ibis.box.init_locations(box2) #Corner and middle points from the boxes

                #print("Box1: ", box1_pos, " Box2: ", box2_pos)

                if ibis.box.intersection_box(box1_pos, box2_pos) and len(possible_inter) < 5: #Intersection between boxes
                    possible_inter.append(elem)
                else :
                    if len(possible_dist) < 5:
                        dist = ibis.box.box_min_distance(box1_pos, box2_pos)
                        box_aux = ibis.box.Box(0, elem, dist)
                        possible_dist.append(box_aux)
                    else:
                        dist = ibis.box.box_min_distance(box1_pos, box2_pos)
                        box_aux = ibis.box.Box(0, elem, dist)
                        possible_dist = min_dist_array(possible_dist, box_aux)
        else:
            
            box2 = out_boxes[elem]
            box2_pos = ibis.box.init_locations(box2) #Corner and middle points from the boxes

            if ibis.box.intersection_box(box1_pos, box2_pos) and len(possible_inter) < 5: #Intersection between boxes
                possible_inter.append(elem)
            else :
                if len(possible_dist) < 5:
                    dist = ibis.box.box_min_distance(box1_pos, box2_pos)
                    box_aux = ibis.box.Box(out_classes[elem], elem, dist)
                    possible_dist.append(box_aux)
                else:
                    dist = ibis.box.box_min_distance(box1_pos, box2_pos)
                    box_aux = ibis.box.Box(out_classes[elem], elem, dist)
                    possible_dist = min_dist_array(possible_dist, box_aux)
    
    possible_dist = sort_dist_array(possible_dist)
    intr_sol = False

    if len(possible_inter) >= 2: #If there is two intersections with the conection box we add them to the solution
        for i, ind in enumerate(possible_inter):
            j = i+1
            while(j < len(possible_inter) and not intr_sol):
                if (out_classes[ind] != out_classes[possible_inter[j]]) and (not intr_sol) and len(obt_relations) < len(non_connections):
                    #print("First element: ", ind, " Second element: ", possible_inter[j], "Class first: ", out_classes[ind], "Class second: ", out_classes[possible_inter[j]])
                    relation = ibis.relations.Relation(ind, possible_inter[j], ind_box, -1)
                    obt_relations.append(relation)
                    intr_sol = True
                j += 1
    elif len(possible_inter) == 1: #If there is only one box intersecting we look for the nearest compatible box available
        inter_ind = possible_inter[0]
        for elem in possible_dist:
            if(out_classes[inter_ind] != elem.ind_class) and (not intr_sol) and len(obt_relations) < len(non_connections):
                #print("First element: ", inter_ind, " Second element: ", elem.id_box, "Class first: ", out_classes[inter_ind], "Class second: ", elem.ind_class)
                relation = ibis.relations.Relation(inter_ind, elem.id_box, ind_box, elem.dist)
                obt_relations.append(relation)
                intr_sol = True
    else:
        for i, ind in enumerate(possible_dist):
            j = i+1
            while j < len(possible_dist) and not intr_sol:
                if(ind.ind_class != possible_dist[j].ind_class) and (not intr_sol) and (len(obt_relations) < len(non_connections)):
                    #print("First element: ", ind.id_box, " Second element: ", possible_dist[j].id_box, "Class first: ", ind.ind_class, "Class second: ", possible_dist[j].ind_class)
                    relation = ibis.relations.Relation(ind.id_box, possible_dist[j].id_box, ind_box, ind.dist)
                    obt_relations.append(relation)
                    intr_sol = True
                j += 1
    
    return obt_relations

def search_missing(obt_relations, out_boxes, out_classes, non_connections):

    for i, elem in enumerate(non_connections):
        if out_classes[elem] == 1 or out_classes[elem] == 2:
            find = ibis.relations.condition_satisfied(obt_relations, elem, out_classes[elem], out_classes)
            print("First find Case 1: ", find)

            while(not find or find == -1): #Loop to fulfill the condition of entities and relations

                if(find == False):
                    possible_dist = []
                    box1_pos = ibis.box.init_locations(out_boxes[elem])
                    j = 0
                    while(j < len(non_connections)):
                        elem2 = non_connections[j]
                        if out_classes[elem] == 1:
                            if out_classes[elem2] == 2:
                                box2_pos = ibis.box.init_locations(out_boxes[elem2])
                                if len(possible_dist) < 5:
                                    dist = ibis.box.box_min_distance(box1_pos, box2_pos)
                                    box_aux = ibis.box.Box(2, elem2, dist)
                                    possible_dist.append(box_aux)
                                else:
                                    dist = ibis.box.box_min_distance(box1_pos, box2_pos)
                                    box_aux = ibis.box.Box(2, elem2, dist)
                                    possible_dist = min_dist_array(possible_dist, box_aux)
                        else:
                            if out_classes[elem2] == 1:
                                box2_pos = ibis.box.init_locations(out_boxes[elem2])
                                if len(possible_dist) < 5:
                                    dist = ibis.box.box_min_distance(box1_pos, box2_pos)
                                    box_aux = ibis.box.Box(1, elem2, dist)
                                    possible_dist.append(box_aux)
                                else:
                                    dist = ibis.box.box_min_distance(box1_pos, box2_pos)
                                    box_aux = ibis.box.Box(1, elem2, dist)
                                    possible_dist = min_dist_array(possible_dist, box_aux)
                        j += 1
            
                    possible_dist = sort_dist_array(possible_dist)
                    print("Len possible_dist: ", len(possible_dist))
                    new_relation = ibis.relations.Relation(elem, possible_dist[0].id_box, elem, possible_dist[0].dist)
                    obt_relations = ibis.relations.add_solution(obt_relations, new_relation, len(non_connections))
        
                elif find == -1:
                    obt_relations = ibis.relations.delete_max_relation(obt_relations, elem)
        
                find = ibis.relations.condition_satisfied(obt_relations, elem, out_classes[elem], out_classes)
                print("Exit find", find)
        
        elif out_classes[elem] == 0:
            find = ibis.relations.used_attribute(obt_relations, elem)

            while not find: # Loop to fulfill the conditions of the attributes
                possible_dist = []
                box1_pos = ibis.box.init_locations(out_boxes[elem])
                j = 0
                while(j < len(non_connections)):
                    elem2 = non_connections[j]
                    if out_classes[elem2] != 0:
                        box2_pos = ibis.box.init_locations(out_boxes[elem2])
                        if len(possible_dist) < 5:
                            dist = ibis.box.box_min_distance(box1_pos, box2_pos)
                            box_aux = ibis.box.Box(out_classes[elem2], elem2, dist)
                            possible_dist.append(box_aux)
                        else:
                            dist = ibis.box.box_min_distance(box1_pos, box2_pos)
                            box_aux = ibis.box.Box(out_classes[elem2], elem2, dist)
                            possible_dist = min_dist_array(possible_dist, box_aux)
                    j += 1
                
                possible_dist = sort_dist_array(possible_dist)
                new_relation = ibis.relations.Relation(elem, possible_dist[0].id_box, elem, possible_dist[0].dist)
                obt_relations = ibis.relations.add_solution(obt_relations, new_relation, len(non_connections))

                find = ibis.relations.used_attribute(obt_relations, elem)
    
    return obt_relations

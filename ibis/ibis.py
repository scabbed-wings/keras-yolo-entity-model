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


def create_relations(out_boxes, out_classes, out_scores, non_connections, box, obt_relations, im_dim):
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
                    box_aux = ibis.box.Box(0, elem, dist)
                    possible_dist.append(box_aux)
                else:
                    dist = ibis.box.box_min_distance(box1_pos, box2_pos)
                    box_aux = ibis.box.Box(0, elem, dist)
                    possible_dist = min_dist_array(possible_dist, box_aux)
    
    possible_dist = sort_dist_array(possible_dist)

    print("Possible inter", possible_inter)

    
    for i in possible_dist:
        print("Possible Distances: ", i.dist, end=' ')





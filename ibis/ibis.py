import numpy as np
from PIL import Image
import os
import ibis.relations

class Box:
    def __init__(self, ind_class, id_box, dist):
        self.ind_class = ind_class
        self. id_box = id_box
        self.dist = dist
    
    def __getattribute__(self, name):
        return super().__getattribute__(name)
        

def intersection_box(box1_pos, box2_pos): #Intersection between boxes
    if(box1_pos[0] <= box2_pos[0] and box2_pos[0] <= box1_pos[8]):
        if((box1_pos[1] <= box2_pos[1] and box2_pos[1] <= box1_pos[9]) or (box1_pos[1] >= box2_pos[1] and box1_pos[1] <= box2_pos[9])):
            return True
    elif(box2_pos[0] <= box1_pos[0] and box1_pos[0] <= box2_pos[8]):
        if((box2_pos[1] <= box1_pos[1] and box1_pos[1] <= box2_pos[9]) or (box2_pos[1] >= box1_pos[1] and box2_pos[1] <= box1_pos[9])):
            return True
    
    return False

def box_min_distance(box1_pos, box2_pos): #Minimum distance between the points of the boxes
    result = -1
    i = 0
    while(i < 16):
        j = 0
        while(j < 16):
            if result == -1:
                dist = ((box1_pos[i] - box2_pos[j]) ** 2) + ((box1_pos[i+1] -box2_pos[j+1]) ** 2)
                dist ** 0.5
                result = dist
            else:
                dist = ((box1_pos[i] - box2_pos[j]) ** 2) + ((box1_pos[i+1] -box2_pos[j+1]) ** 2)
                dist ** 0.5
                if dist < result:
                    result = dist
            j += 2
        i += 2
    
    return result

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
    box1_pos = [box[1], box[0], box[1] + im_dim[0]/2, box[0], box[3], box[0], box[3], box[0] + im_dim[1]/2,
    box[3], box[2], box[1] + im_dim[0]/2, box[2], box[1], box[2], box[1], box[0] + im_dim[1]/2]

    possible_inter = []
    possible_dist = []

    
    for elem in non_connections:
        if out_classes[elem] == 0: #Attributees detection
            if not ibis.relations.used_attribute(obt_relations, elem):
                box2 = out_boxes[elem]
                box2_pos = [ box2[1], box2[0], box2[1] + im_dim[0]/2, box2[0], box2[3], box2[0], box2[3], box2[0] + im_dim[1]/2,
                box2[3], box2[2], box2[1] + im_dim[0]/2, box2[2], box2[1], box2[2], box2[1], box2[0] + im_dim[1]/2] #Corner and middle points from the boxes

                print("Box1: ", box1_pos, " Box2: ", box2_pos)

                if intersection_box(box1_pos, box2_pos) and len(possible_inter) < 5: #Intersection between boxes
                    possible_inter.append(elem)
                else :
                    if len(possible_dist) < 5:
                        dist = box_min_distance(box1_pos, box2_pos)
                        box_aux = Box(0, elem, dist)
                        possible_dist.append(box_aux)
                    else:
                        dist = box_min_distance(box1_pos, box2_pos)
                        box_aux = Box(0, elem, dist)
                        possible_dist = min_dist_array(possible_dist, box_aux)
        else:
            
            box2 = out_boxes[elem]
            box2_pos = [box2[1], box2[0], box2[1] + im_dim[0]/2, box2[0], box2[3], box2[0], box2[3], box2[0] + im_dim[1]/2,
            box2[3], box2[2], box2[1] + im_dim[0]/2, box2[2], box2[1], box2[2], box2[1], box2[0] + im_dim[1]/2] #Corner and middle points from the boxes

            if intersection_box(box1_pos, box2_pos) and len(possible_inter) < 5: #Intersection between boxes
                possible_inter.append(elem)
            else :
                if len(possible_dist) < 5:
                    dist = box_min_distance(box1_pos, box2_pos)
                    box_aux = Box(0, elem, dist)
                    possible_dist.append(box_aux)
                else:
                    dist = box_min_distance(box1_pos, box2_pos)
                    box_aux = Box(0, elem, dist)
                    possible_dist = min_dist_array(possible_dist, box_aux)
    
    possible_dist = sort_dist_array(possible_dist)

    print("Possible Distances: ", possible_dist)





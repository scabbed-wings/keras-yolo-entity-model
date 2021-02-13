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

def init_locations(box):
    width = box[3] - box[1]
    height = box[2] - box[0]

    bbox = [box[1], box[0], box[1] + width/2, box[0], box[3], box[0], box[3], box[0] + height/2,
    box[3], box[2], box[1] + width/2, box[2], box[1], box[2], box[1], box[0] + height/2]

    return bbox
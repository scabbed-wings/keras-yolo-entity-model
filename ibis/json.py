import ibis.relations
import os

def create_json(obt_relations, non_connections, out_boxes, out_classes):
    ternaries = []

    if os.path.isfile("model.json"):
        os.remove("model.json")
    
    file_object = open("model.json", 'a')
    file_object.write("{\n")
    
    #Writing entities
    file_object.write("\t\"Entities\":  [\n")
    for i, elem in enumerate(non_connections):
        if out_classes[elem] == 1:
            file_object.write("\t\t{\n")
            top, left, bottom, right = out_boxes[elem]
            x,y= left + (right -left)/2, top + (bottom - top)/2
            file_object.write("\t\t\t\"x\":  \"" + str(x) +"\",\n")
            file_object.write("\t\t\t\"y\":  \"" + str(y) +"\",\n")
            file_object.write("\t\t\t\"name\":  \"Entity" + str(elem) +"\",\n")
            file_object.write("\t\t\t\"type\":  \"Normal\",\n")
            file_object.write("\t\t\t\"id\":  \"" + str(elem) +"\"\n")
            if ibis.relations.there_is_more(i, 1, non_connections, out_classes):
                file_object.write("\t\t},\n")
            else:
                file_object.write("\t\t}\n")
    file_object.write("\t], \n")

    #Writing relations
    file_object.write("\t\"Relations\":  [\n")
    for elem in non_connections:
        if out_classes[elem] == 2:
            if ibis.relations.is_ternary(elem, obt_relations):
                ternaries.append(elem)
            else:
                file_object.write("\t\t{\n")
                top, left, bottom, right = out_boxes[elem]
                x,y= left + (right -left)/2, top + (bottom - top)/2
                contr = True
                file_object.write("\t\t\t\"name\":  \"Relation" + str(elem) +"\",\n")
                file_object.write("\t\t\t\"type\":  \"Normal\",\n")
                for elem2 in obt_relations:
                    if elem2.ind_inp == elem and contr:
                        if out_classes[elem2.ind_out] == 1:
                            file_object.write("\t\t\t\"enter\":  \"" + str(elem2.ind_out)+"\",\n")
                            contr = False
                    elif elem2.ind_out == elem and contr:
                        if out_classes[elem2.ind_inp] == 1:
                            file_object.write("\t\t\t\"enter\":  \"" + str(elem2.ind_inp)+"\",\n")
                            contr = False
                    elif elem2.ind_inp == elem:
                        if out_classes[elem2.ind_out] == 1:
                            file_object.write("\t\t\t\"exit\":  \"" + str(elem2.ind_out)+"\",\n")
                    elif elem2.ind_out == elem:
                        if out_classes[elem2.ind_inp] == 1:
                            file_object.write("\t\t\t\"exit\":  \"" + str(elem2.ind_inp)+"\",\n")
                
                file_object.write("\t\t\t\"id\":  \"" + str(elem) +"\",\n")
                file_object.write("\t\t\t\"x\":  \"" + str(x) +"\",\n")
                file_object.write("\t\t\t\"y\":  \"" + str(y) +"\",\n")
                file_object.write("\t\t\t\"enterCard\": \"(0,N)\",\n")
                file_object.write("\t\t\t\"exitCard\": \"(0,N)\"\n")

                if ibis.relations.there_is_more(i, 2, non_connections, out_classes):
                    file_object.write("\t\t},\n")
                else:
                    file_object.write("\t\t}\n")
    file_object.write("\t],\n")


    #Writing attributes

    file_object.write("\t\"Attributes\":  [\n")
    for elem in non_connections:
        if out_classes[elem] == 0:
            file_object.write("\t\t{\n")
            top, left, bottom, right = out_boxes[elem]
            x,y= left + (right -left)/2, top + (bottom - top)/2
            file_object.write("\t\t\t\"name\":  \"Attribute"+ str(elem)+ "\",\n")
            file_object.write("\t\t\t\"key\":  \"false\",\n")
            file_object.write("\t\t\t\"type\":  \"Normal\",\n")
            file_object.write("\t\t\t\"isCompound\":  \"false\",\n")
            file_object.write("\t\t\t\"isChild\":  \"false\",\n")
            file_object.write("\t\t\t\"id\":  \"" + str(elem) +"\",\n")

            for elem2 in obt_relations:
                if elem2.ind_inp == elem:
                    file_object.write("\t\t\t\"element\": \""+ str(elem2.ind_out)+ "\",\n")
                elif elem2.ind_out == elem:
                    file_object.write("\t\t\t\"element\": \""+ str(elem2.ind_inp)+ "\",\n")

            file_object.write("\t\t\t\"x\":  \"" + str(x) +"\",\n")
            file_object.write("\t\t\t\"y\":  \"" + str(y) +"\"\n")
            if ibis.relations.there_is_more(i, 0, non_connections, out_classes):
                file_object.write("\t\t},\n")
            else:
                file_object.write("\t\t}\n")
    file_object.write("\t],\n")

    #Writing Ternaries
    file_object.write("\t\"Ternaries\":  [\n")
    for i, elem in enumerate(ternaries):
        file_object.write("\t\t{\n")
        count = 0
        top, left, bottom, right = out_boxes[elem]
        x,y= left + (right -left)/2, top + (bottom - top)/2
        file_object.write("\t\t\t\"name\":  \"TernaryRelation"+ str(elem)+ "\",\n")
        file_object.write("\t\t\t\"id\":  \"" + str(elem) +"\"\n")
        file_object.write("\t\t\t\"x\":  \"" + str(x) +"\",\n")
        file_object.write("\t\t\t\"y\":  \"" + str(y) +"\",\n")
        for elem in obt_relations:
            if elem2.ind_inp == elem and count == 0:
                file_object.write("\t\t\t\"first\": \""+ str(elem2.ind_out) +"\",\n")
                count += 1
            elif elem2.ind_out == elem and count == 0:
                file_object.write("\t\t\t\"first\": \""+ str(elem2.ind_inp) +"\",\n")
                count += 1
            elif elem2.ind_inp == elem and count == 1:
                file_object.write("\t\t\t\"second\": \""+ str(elem2.ind_out) +"\",\n")
                count += 1
            elif elem2.ind_out == elem and count == 1:
                file_object.write("\t\t\t\"second\": \""+ str(elem2.ind_inp) +"\",\n")
                count += 1
            elif elem2.ind_inp == elem and count == 2:
                file_object.write("\t\t\t\"third\": \""+ str(elem2.ind_out) +"\",\n")
                count += 1
            elif elem2.ind_out == elem and count == 2:
                file_object.write("\t\t\t\"third\": \""+ str(elem2.ind_inp) +"\",\n")
                count += 1
        file_object.write("\t\t\t\"cardFirst\": \"1\",\n")
        file_object.write("\t\t\t\"cardSecond\": \"N\",\n")
        file_object.write("\t\t\t\"cardThird\": \"M\",\n")
        
        if (i+1) < len(ternaries):
             file_object.write("\t\t},\n")
        else:
            file_object.write("\t\t}\n")
    file_object.write("\t]\n")
    file_object.write("}")
    file_object.close()







    


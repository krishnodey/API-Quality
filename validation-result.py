'''
#Create each individual file for each Validator


import pandas as pd
import csv

excel_path = ".\Validation\CANAI Validation-Responses.xlsx"

shimul = pd.read_excel(excel_path, sheet_name="Galib")

data = shimul['Data'].tolist()
antipattern = shimul['Antipattern'].tolist()

#shimul[['dumm','ID', 'Method','URI', 'Desription+Parameter']] = shimul['Data'].str.split('\t', expand=True)
uri_id = []
http_method = []
uris = []
description = []
for d in data:
    #print(d)
    id, method, uri, des= d.strip().split(">>")
    uri_id.append(id)
    http_method.append(method)
    uris.append(uri)
    description.append(des)
    #print(f"{uri_id}, {http_method}, {uris}, {description}")



amro = []
non_std =[]
crudy = []
unversioned = []
pluralized = []
non_descriptive = []
contextless = []
non_hier = []
lesscohisive = []
inconsistent = []
for ap in antipattern:
    app = ap.split(",")
    am,std,crd,unver, plu, des, contex, hier, perti, con = 0,0,0,0,0,0,0,0,0,0
    for a in app:
        a = a.strip()
        if a == 'Amorphous antipattern':
            am = 1
        elif a == 'Non-standard URI Design':
            std = 1
        elif a == 'CRUDy URIs':
            crd = 1
        elif a == 'Unversioned URI':
            unver = 1
        elif a == 'Pluralised Nodes':
            plu = 1
        elif a == 'Non Descriptive URIs':
            des = 1
        elif a == 'Contextless Resource Names':
            contex = 1
        elif a == 'Non-hierarchical Nodes':
            hier = 1
        elif a == 'Non-pertinent Documentation':
            perti = 1
        elif a == 'Inconsistent Documentation':
            con = 1
    amro.append(am)
    non_std.append(std)
    crudy.append(crd)
    unversioned.append(unver)
    pluralized.append(plu)
    non_descriptive.append(des)
    contextless.append(contex)
    non_hier.append(hier)
    lesscohisive.append(perti)
    inconsistent.append(con)

#print(uri_id)
#print(f"{len(uri_id)}, {len(http_method)}, {len(uris)}, {len(description)}")
#print(f"{len(amro)}, {len(non_std)}, {len(crudy)}, {len(unversioned)}, {len(pluralized)}, {len(non_descriptive)}, {len(contextless)}, {len(non_hier)}, {len(lesscohisive)}, {len(inconsistent)}")
path = "Validation/galib-validtion.csv"
with open(path, 'w', newline='') as summ_file:
        csv_writer = csv.writer(summ_file)
        header_line = ['ID', 'HTTP Method',	'URI', 'Decription+Parameters','AmorphousURI', 'NonStandardURI',  'CRUDyURI',
                       'UnversionedURI', 'PluralisedNodes', 'NonDescriptiveURI',
                       'ContextlessResource', 'NonHierarchicalNodes',
                       'LessCohisiveDoc', 'InconsistantDoc']
        csv_writer.writerow(header_line)

        for id, method, uris, des, ap1, ap2, ap3, ap4, ap5, ap6, ap7, ap8, ap9, ap10 in zip(uri_id, http_method, uris, description, amro, non_std, crudy, unversioned, pluralized, non_descriptive, contextless, non_hier, lesscohisive, inconsistent):
            data_line= [id, method, uris, des, ap1, ap2, ap3, ap4, ap5, ap6, ap7, ap8, ap9, ap10]
            #print(f"{id}, {method}, {uris}, {des}, {ap1}, {ap2}, {ap3}, {ap4}, {ap5}, {ap6}, {ap7}, {ap8}, {ap9}, {ap10}")
            csv_writer.writerow(data_line)'''


#Majority Voting
import csv
from collections import Counter

file1 = "Validation/arid-validtion.csv"
file2 = "Validation/galib-validtion.csv"
file3 = "Validation/shimul-validtion.csv"

with open(file1, "r") as f1, open(file2, "r") as f2, open(file3, "r") as f3:
    arid = csv.reader(f1)
    galib = csv.reader(f2)
    shimul = csv.reader(f3)
    next(arid)
    next(galib)
    next(shimul)
    
    #print(f"{len(arid), {len(galib)}, {len(shimul)}}")
    lst1 = []
    lst2 = []
    lst3 = []
    for ln1 in arid:
        lst1.append(ln1)
    
    for ln1 in galib:
        lst2.append(ln1)
    
    for ln1 in shimul:
        lst3.append(ln1)
        
print(f"{len(lst1), {len(lst2)}, {len(lst3)}}")
path = "Validation/merged_file.csv"
with open(path, 'w', newline='') as summ_file:
        csv_writer = csv.writer(summ_file)
        header_line = ['ID', 'HTTP Method',	'URI', 'Decription+Parameters','AmorphousURI', 'NonStandardURI',  'CRUDyURI',
                       'UnversionedURI', 'PluralisedNodes', 'NonDescriptiveURI',
                       'ContextlessResource', 'NonHierarchicalNodes',
                       'LessCohisiveDoc', 'InconsistentDoc']
        csv_writer.writerow(header_line)

        for ar, gl, sh in zip(lst1, lst2, lst3):
            if ar[0].strip() == gl[0].strip() == sh[0].strip():
                for i in range(4,14):
                    votes = [ar[i].strip(), gl[i].strip(), sh[i].strip()]
                    vote_counts = Counter(votes)
                    majority_vote = max(vote_counts, key=vote_counts.get, default=None)
                    if i == 4:
                        ap1 = majority_vote
                    elif i == 5:
                        ap2 =majority_vote
                    elif i == 6:
                        ap3 = majority_vote
                    elif i == 7:
                        ap4 = majority_vote
                    elif i == 8:
                        ap5 = majority_vote
                    elif i == 9:
                        ap6 = majority_vote
                    elif i == 10:
                        ap7 = majority_vote
                    elif i == 11:
                        ap8 = majority_vote
                    elif i == 12:
                        ap9 = majority_vote
                    elif i == 13:
                        ap10 = majority_vote

                data_line = [ar[0],ar[1], ar[2], ar[3], ap1, ap2, ap3, ap4, ap5, ap6, ap7, ap8, ap9, ap10]
                csv_writer.writerow(data_line)



#Final Table




'''import csv
majority_file = "Validation/majority_voting_file.csv"
validation_file= "Result-Database/validation_data.csv"

with open(majority_file, 'r') as f1, open(validation_file, 'r') as f2:
    major = csv.reader(f1)
    valid = csv.reader(f2)
    next(major)
    next(valid)
    
    lst1 = []
    lst2 = []
    for ln1 in major:
        lst1.append(ln1)
    
    for ln1 in valid:
        lst2.append(ln1)

val_count = [0,0,0,0,0,0,0,0,0,0]
for v in lst2:
    if int(v[6].strip()) == 1:
        val_count[0] += 1
    if int(v[9].strip()) == 1:
        val_count[1] += 1
    if int(v[12].strip()) == 1:
        val_count[2] += 1
    if int(v[15].strip()) == 1:
        val_count[3] += 1
    if int(v[18].strip()) == 1:
        val_count[4] += 1
    if int(v[21].strip()) == 1:
        val_count[5] += 1
    if int(v[24].strip()) == 1:
        val_count[6] += 1
    if int(v[27].strip()) == 1:
        val_count[7] += 1
    if int(v[30].strip()) == 1:
        val_count[8] += 1
    if int(v[33].strip()) == 1:
        val_count[9] += 1

print(val_count)
m_count = [0,0,0,0,0,0,0,0,0,0]

for v in lst1:
    if int(v[4].strip()) == 1:
        m_count[0] += 1
    if int(v[5].strip()) == 1:
        m_count[1] += 1
    if int(v[6].strip()) == 1:
        m_count[2] += 1
    if int(v[7].strip()) == 1:
        m_count[3] += 1
    if int(v[8].strip()) == 1:
        m_count[4] += 1
    if int(v[9].strip()) == 1:
        m_count[5] += 1
    if int(v[10].strip()) == 1:
        m_count[6] += 1
    if int(v[11].strip()) == 1:
        m_count[7] += 1
    if int(v[12].strip()) == 1:
        m_count[8] += 1
    if int(v[13].strip()) == 1:
        m_count[9] += 1

print(m_count)

anipatterns = ['AmorphousURI', 'NonStandardURI',  'CRUDyURI', 'UnversionedURI', 'PluralisedNodes', 'NonDescriptiveURI', 'ContextlessResource', 'NonHierarchicalNodes', 'LessCohisiveDoc', 'InconsistentDoc']

path = "Validation/accuracy_file.csv"
with open(path, 'w', newline='') as summ_file:
        csv_writer = csv.writer(summ_file)
        header = ['Antipatterns', "P", "N", "TP", "FP", "TN", "FN", "Accuracy"]
        csv_writer.writerow(header)
        for ap, vc, mc in zip(anipatterns, val_count, m_count):

            pos = vc
            neg = 91-pos
            tp = mc
            fp = pos - tp
            tn = vc
            fn = neg - tn
            accuracy = round((tp+tn)/tp+fp+tn+fn,2)

            
            line = [ap, pos, neg, tp, fp, tn, fn, accuracy]
            #print(f"{ap}, {vc}, {91-vc}, {mc}, {max(mc-vc, 0)},{91-mc}, {max((91-mc) - (91-vc), 0)}")
            csv_writer.writerow(line)
'''    
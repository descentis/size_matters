#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 18:49:42 2020

@author: descentis
"""

import random
import matplotlib.pyplot as plt
import kdap
from random import sample

featured = {}
final_list = []

'''
******stratified sampling*******
(sample size of the strata = size of the entire sample / population size*layer size)
'''

knol = kdap.knol()

wikiproject_list = ['GA', 'B', 'C', 'Start', 'Stub']

article_dict = {}
population_size = 0
project_size = []
for project in wikiproject_list:
    article_dict[project] = knol.get_wiki_article_by_class(wiki_class=project)
    population_size += len(article_dict[project])
    project_size.append(len(article_dict[project]))
    
sample_size = 11664

sample_project_list = []

for i in project_size:
    sample_project_list.append(int((sample_size/population_size)*i))

with open('sample.txt', 'a') as myFile:
    myFile.write(str(sample_project_list[0])+' '+str(sample_project_list[1])+ ' '+ str(sample_project_list[2])+' '+str(sample_project_list[3]))
article_list = []

j=0
for key,val in article_dict.items():
    article_list += sample(article_dict[key], sample_project_list[j])
    j+=1

final_list = {}
for each in article_list:
    final_list[each[1].replace('"','')] = 0

fa_list = []    
with open('featured_list.txt', 'r') as myFile:
    for line in myFile:
        line = line.split(' ')
        featured[line[0]] = [line[1],line[2][:-1]]
        fa_list.append([line[1],line[2][:-1]])

print(len(final_list))
non_featured_list = []
with open('non_featured_names.txt', 'r') as myFile:
    for line in myFile:
        if "====" in line:
            break
        for line in myFile:
            #print(line.split(' '))
            line = line.split(' ')
            name = ' '.join(line[:-1])
            try:
                if final_list.get(name) != None:

                    non_featured_list.append(int(line[-1][:-1]))
            except:
                pass

with open('nf_list.txt', 'r') as myFile:
    for line in myFile:
        if "====" in line:
            break
        for line in myFile:
            try:
                line = line[:-1]
                line = line.split(' ')
                name = " ".join(line[3:])
                if final_list.get(name) != None:
                    non_featured_list.append(int(line[1]))
            except:
                pass

'''
temp = random.sample(non_featured_list, len(featured))

non_featured = {}
for i in temp:
    l = i.split(' ')
    non_featured[l[0]] = [l[1], l[2]]
    final_list.append(l[0])
'''

final_set = fa_list + non_featured_list
print(len(non_featured_list))
training_set = random.sample(final_set, int(0.66*len(final_set)))
test_set = random.sample(final_set, len(final_set) - int(0.66*len(final_set)))

# Training Part

count_length = []
f_error_rate = []
nf_error_rate = []
total_error = []
for i in range(0,6000,100):
    f_error = 0
    nf_error = 0
    #total_error = 0
    f_total = 0
    nf_total = 0
    #total = 0
    for article_id in training_set:
        if isinstance(article_id, int):
            nf_total += 1
            if article_id > i:
                nf_error += 1
        else:
            f_total += 1
            if int(article_id[0]) < i:
                f_error += 1
                     
    #if int(nf_error/nf_total) != 1 and int(f_error/f_total) != 0:
    f_error_rate.append(f_error/f_total)
    nf_error_rate.append(nf_error/nf_total)
    total_error.append((f_error+nf_error)/(f_total+nf_total))
    count_length.append(i)
'''

#Testing Part
f_error = 0
nf_error = 0
#total_error = 0
f_total = 0
nf_total = 0
#total = 0

for article_id in test_set:
    if isinstance(article_id, int):
        nf_total += 1
        if article_id > 2500:
            nf_error += 1
    else:
        f_total += 1
        if int(article_id[0]) < 2500:
            f_error += 1
                     

print((f_error+nf_error)/(f_total+nf_total))

'''
plt.plot(count_length, f_error_rate, marker='o', markerfacecolor='blue', markersize=4, color='skyblue', linewidth=2, label="Featured Articles")
plt.plot(count_length, nf_error_rate, marker='', color='olive', linewidth=2, linestyle='dashed', label="Non-featured articles")
plt.plot(count_length, total_error, color='olive', linewidth=2, label="Combined")

plt.legend()

plt.xlabel('Word count threshold', fontsize=14)
plt.ylabel('Error rate', fontsize=14)

plt.savefig("error_rate.png", dpi=800)


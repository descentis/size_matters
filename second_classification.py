#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 17:54:47 2020

@author: descentis
"""
import matplotlib.pyplot as plt
import random
f_list = []
nf_list = []

with open('flist.txt','r') as myFile:
    for line in myFile:
        line = line.split(' ')
        count = int(line[1]) + int(line[2]) + int(line[3]) + int(line[4])
        f_list.append(['FA', count])

count = 0
with open('nflist.txt','r') as myFile:
    for line in myFile:
        line = line.split(' ')
        count = int(line[1]) + int(line[2]) + int(line[3]) + int(line[4])
        nf_list.append(['NF', count])
        
        if count == 11547:
            break
        
        count += 1
        

final_set = f_list + nf_list

#print(len(non_featured_list))
training_set = random.sample(final_set, int(0.66*len(final_set)))
test_set = random.sample(final_set, len(final_set) - int(0.66*len(final_set)))

# Training Part

count_length = []
f_error_rate = []
nf_error_rate = []
total_error = []
for i in range(0,15000,20):
    f_error = 0
    nf_error = 0
    #total_error = 0
    f_total = 0
    nf_total = 0
    #total = 0
    for article_id in training_set:
        if article_id[0] == 'NF':
            nf_total += 1
            if article_id[1] > i:
                nf_error += 1
        else:
            f_total += 1
            if article_id[1] < i:
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
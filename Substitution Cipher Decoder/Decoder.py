import string
from random import shuffle
import re
import requests
import numpy as np
import os
import random


#### Creating matrices for unigrams, bigrams and trigrams ###
unig = np.zeros(26)
big = np.ones((26,26))
trig = np.ones((26,26,26))


### defining functions for unigrams, bigrams and trigrams ###
def unigram(uni):
    ind = ord(uni) - 97
    unig[ind] += 1

def bigram(f,x):
    ind1 = ord(f) - 97
    ind2 = ord(x) - 97
    big[ind1][ind2] +=1

def trigram(f,x,y):
    ind1 = ord(f) - 97
    ind2 = ord(x) - 97
    ind3 = ord(y) - 97
    trig[ind1][ind2][ind3] +=1



### Calculating probablity of unigrams, bigrams and trigrams based on training data ####
def calc_probability(file_loc):
    reg = re.compile('[^a-zA-Z]')
    file_loc = file_loc.replace('\\','/')
    for line in open(file_loc,encoding="utf-8"):
        line = reg.sub(' ', line)
        line = line.rstrip().lower()

        if line:
            words = line.split()
            for word in words:

                unigram(word[0])
                f = word[0]
                w = word[1:]
                for x in w:
                    bigram(f,x)
                    f=x

                if(len(word)>2):
                    x = word[1]

                    for y in word[2:]:
                        trigram(f,x,y)
                        f=x
                        x=y

    unig_sum = np.sum(unig)
    # print(unig_sum)
    big_sum = []
    for l in range(26):
        big_sum.append(np.sum(big[l]))

    for iter in range(26):
        unig[iter] /= unig_sum



    for iter in range(26):
        for iter2 in range(26):
            big[iter][iter2] /= big_sum[iter]


    trig_sum = np.zeros((26,26))

    for l in range(26):
        for k in range(26):
            trig_sum[l][k] = np.sum(trig[l][k])

    for l in range(26):
        for k in range(26):
            for m in range(26):
                trig[l][l][m] /= trig_sum[l][k]


### Getting probability of a word
def word_probab(xyz):
    prob = 0
    reg = re.compile('[^a-z]')
    xyz = reg.sub('',xyz)
    if isinstance(xyz,str) == True:
        prob = np.log(unig[ord(xyz[0])-97])
        f= xyz[0]
        for l in xyz[1:]:
            prob += np.log(big[ord(f) - 97][ord(l)-97])
            f = l

        if(len(xyz)>2):
            s = xyz[1]
            for l in xyz[2:]:
                prob +=  np.log(trig[ord(f) - 97][ord(s)-97][ord(l)-97])
                f=s
                s=l

    else:
        prob = 0
    return(prob)


### Getting probablity of sequence of words ###
def line_probab(lines):
    probl = 0
    if lines:
        for words in lines.split():
            probl += word_probab(words)
    else:
        probl=0

    return probl

### Creating an encoding word map ###
def dna_word_map(dna):
    alphabet = list(string.ascii_lowercase)
    word_map = {}

    for x,y in zip(alphabet,dna):
        word_map[x] = y

    return word_map

### Defining function to calculate total probability of a word or sequence ###
def score_calc(message,word_map):
    new_message = ""
    for words in message.split():
        for letter in words:
            if letter in word_map.keys():
                new_message += word_map[letter]
            else:
                new_message += letter
        new_message += " "


    return line_probab(new_message)


### Defining genetic algorithm ###
def genetic_evolve(word_map_list,num):
    dna_pool = []
    for x in word_map_list:
        parent = x['map']
        parent_dna = []

        for a in parent.keys():
            parent_dna.append(parent[a])

        for v in range(num):

            offspring_dna = []
            offspring = parent
            # print(offspring)
            score = float('-inf')
            count = 0

            l1 = random.choice(string.ascii_letters.lower())
            l2 = random.choice(string.ascii_letters.lower())

            temp = offspring[l1]
            offspring[l1] = offspring[l2]
            offspring[l2] = temp
            count += 1
            # print(offspring)
            for b in offspring.keys():
                offspring_dna.append(offspring[b])


            dna_pool.append(offspring_dna)
        dna_pool.append(parent_dna)

    return dna_pool


### Defining function to keep best scores ###
def survival_of_fittest(dna_pool,message):
    word_map_list = []
    for dna in dna_pool:
        word_map = dna_word_map(dna)
        mapper = {}
        score = score_calc(message, word_map)

        mapper['map'] = word_map
        mapper['score'] = score
        print(score)

        word_map_list.append(mapper)
        word_map_list = sorted(word_map_list, key=lambda i: i['score'], reverse=True)

    return word_map_list[:5]

### Decoder Function ###
def decoder(message):
    reg = re.compile('[^a-zA-Z]')
    message = message.lower()
    message = reg.sub(' ',message)
    decoded = ""
    dna_pool = []
    for l in range(20):
        dna = list(string.ascii_lowercase)
        shuffle(dna)
        dna_pool.append(dna)

    for i in range(1000):
        word_map_list = survival_of_fittest(dna_pool,message)
        dna_pool = genetic_evolve(word_map_list,3)

    best = word_map_list[0]
    best_map = best['map']

    print("decoded message - ")
    # print(best_map)
    for nwords in message.split():
        for nletter in nwords:
            if nletter in best_map.keys():
                decoded += best_map[nletter]
            else:
                decoded += nletter
        decoded += " "

    print(decoded)

    print("best score - ", best['score'])


file_loc = input("Enter training data location - ")
calc_probability(file_loc)
encoded_message = input("Enter encoded message - ")

decoder(encoded_message)
import os
import re
import string
import textwrap
from collections import Counter
import json
import numpy as np
import random
from tqdm import trange


def text_preprocessing(s):
    sNew = ''
    alphabetic = ['м', 'и', 'ж', 'в', 'е', 'о', 'н', 'з', 'ч', 'а', 'й', 'у', 'д', 'с', 'і', 'т', 'п', 'р', 'б', 'я', 'к', 'щ', 'ц', 'г', 'ш', 'л', 'ь', 'ю', 'є', 'х', 'ї', 'ф']
    for i in s:
        if i.lower() in alphabetic:
            sNew += i.lower()
    sNew = sNew.replace('ґ','г')
    return sNew

def frequency(s, l, probability=False):
    if l == 1:
    # Монограми:
        c = Counter(s)
        if probability:
            length = len(s)
            for key, value in c.items():
                c[key] = value / length
            return c    

        return c
    if l == 2:
    # Бiграми:
        c = Counter(s[i : i + 2] for i in range(len(s) - 1))
        if probability:
            length = sum(c.values())
            for key, value in c.items():
                c[key] = value / length    
            return c
        return c
    return "wrong input"

def entropy(s, l):
    H = 0
    c = frequency(s, l, probability=True)
    for p in c.values():
        H += p * np.log2(p)
    H = (H / l) * (-1)
    return H

def affinity(s,l):
    I = 0
    c = frequency(s,l)
    L = sum(c.values())
    for val in c.values():
        I += val * (val - 1)
    I /= L*(L-1)
    return I

def get_key(val,dict):
    for key, value in dict.items():
        if val == value:
            return key


# Функцiя для отримання N текстiв X довжини L:
def get_N_texts(s, N, L):

    xTexts = []
    i = 0
    j = 0
    
    for i in range(N):
        f = s[j:j+L]
        xTexts.append(f)
        j += 100
    
    return xTexts

# Спотворення тексту (а) Вiженер:
def dist_Vigenere(s,r,ukrDict,isText=False):
    r = 5
    Key = random.sample(range(1,33), r)


    Y = []    
    for i in range(len(s)):
        Y.append(np.mod(ukrDict[s[i]]+Key[np.mod(i, 1)],32))

    if isText:
        yText = ''
        for i in range(len(Y)):
            yText += get_key(Y[i], ukrDict)
        return yText
    return Y
    

# Спотворення тексту (б) Афiнна Пiдстановка:
def dist_Affin(s,l,ukrDict,isText=False):

    if l == 1:
        Keys = random.sample(range(1,33), 2)

        Y = []    
        for i in range(len(s)):
            x = ukrDict[s[i]]
            x = Keys[0] * x + Keys[1]
            x = np.mod(x, 32)
            Y.append(x)
        if isText:
            yText = ''
            for i in trange(len(Y)):
                yText += get_key(Y[i], ukrDict)
            return yText
        return Y

    elif l == 2:
        Keys = []
        Keys.append(random.sample(range(1,33), 2))
        Keys.append(random.sample(range(1,33), 2))
        Y = []
        for i in range(len(s)-1):
            x = s[i:i+2]
            x = [ukrDict[x[0]], ukrDict[x[1]]]
            a = Keys[0]
            b = Keys[1]
            y = [np.mod(a[0]*x[0] + b[0],1024), np.mod(a[1]*x[1]+b[1], 1024)]
            Y.append(y)             
        if isText:
            yText = ''
            for i in trange(len(Y)):
                yText += get_key[0]
            return yText
        return Y
    else:
        return "Wrong input"
    


def main():

# Опрацювання тексту:
    # s = ''
    # with open('lab2/text.txt', 'r') as file:
        
    #     data = file.read()
        
    #     s = text_preprocessing(data)
    
    # with open('lab2/newText.txt', 'w') as file:
    #     file.write(s)
    
    s = ''
    with open('lab2/newText.txt', 'r') as file:
        s = file.read(700_000)
# # Частоти:
#     monoFr = frequency(s, 1)
#     biFr = frequency(s, 2)
# # Ентропiя:
#     monoEn = entropy(s,1)
#     print(monoEn)
#     biEn = entropy(s,2)
#     print(biEn)
# # Iндекс Вiдповiдностi:
#     monoAff = affinity(s,1)
#     print(monoAff)
#     biAff = affinity(s,2)
#     print(biAff)    


    ukrDict = {}
    with open('lab2/ukrAlphabeticNumbered.json') as json_file:
        ukrDict = json.load(json_file)

    X = get_N_texts(s, N=1000, L=1000)
    Y = []
    # r = 5
    # for i in trange(len(X)):
    #     Y.append(dist_Vigenere(X[i],r, ukrDict,isText=True))

    for i in trange(len(X)):
        Y.append(dist_Affin(X[i],2,ukrDict))

    
    exit()



if __name__ == "__main__":
    main()

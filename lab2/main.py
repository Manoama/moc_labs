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
            return {k: v for k, v in sorted(c.items(), key=lambda item: item[1], reverse=True)}    

        return {k: v for k, v in sorted(c.items(), key=lambda item: item[1], reverse=True)}
    if l == 2:
    # Бiграми:
        c = Counter(s[i : i + 2] for i in range(len(s) - 1))
        if probability:
            length = sum(c.values())
            for key, value in c.items():
                c[key] = value / length    
            return {k: v for k, v in sorted(c.items(), key=lambda item: item[1], reverse=True)}
        return {k: v for k, v in sorted(c.items(), key=lambda item: item[1], reverse=True)}
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
    try:
        I /= L*(L-1)
    except:
        I = 0
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
        j += 10
    
    return xTexts

# Спотворення тексту (а) Вiженер:
def dist_Vigenere(s,r,ukrDict,isText=False):
    r = 5
    Key = random.sample(range(1,33), r)


    Y = []    
    for i in range(len(s)):
        Y.append(np.mod(ukrDict[s[i]]+Key[np.mod(i, r)],32))

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

# Спотворення тексту (г) Фiббоначчi:
def dist_Fibonacci(s, l, ukrDict, isText=False):
    
    Y = []
    if l == 1:    
        for i in range(2, len(s)):
            s0 = ukrDict[s[i-1]]
            s1 = ukrDict[s[i-2]]
            y = int(np.mod(s0+s1, 32))
            Y.append(y)
        if isText:
            yText = ''
            for i in trange(len(Y)):
                yText += get_key[0]
            return yText
        return Y
    if l == 2:
        for i in range(3, len(s)):
            s0 = [ukrDict[s[i-1]], ukrDict[s[i-2]]]
            s1 = [ukrDict[s[i-2]], ukrDict[s[i-3]]]
            y = [s0[0]+s1[0], s1[0] + s1[1]]
            y = [int(np.mod(y[0], 32)), int(np.mod(y[1], 32))]
            Y.append(y)
        return Y
    else:
        return "Wrong input"


def criteria_2_0(Afrq,x):
    flag=True
    for a in Afrq: 
        if a not in x:
            return 0 # H1 # у текстi x якоiсь монограми нема 
    return 1 # H0 # у текстi x присутнi всi монограми

def criteria_2_1(Afrq, x, k):
    Aaf = []
    for a in Afrq:
        if a in x:
            Aaf.append(a)
    count = len(set(Afrq).intersection(Aaf))
    if count <= k:
        return 0
    return 1

def criteria_2_2(Afrq, x, sFreq):
    xFreq = frequency(x,2,probability=True)
    for a in Afrq:
        f = 0
        if a in xFreq.keys():
            f = xFreq[a]    
        k = sFreq[a]
        if f < k:
            return 0
    return 1

def criteria_2_3(Afrq, x, K):
    xFreq = frequency(x,2,probability=True)
    F = sum(xFreq.values())
    F = round(F, 6)
    if F < K:
        return 0
    return 1      

def criteria_4_0(x, sAff, k):    
    xAff = affinity(x,2)
    if abs(xAff - sAff) > k:
        return 0
    return 1

def criteria_5_0(x, sFreq, k):
    j = 7
    Bprh = list(sFreq.keys())[-j:]
    boxes = {}
    for b in Bprh:
        boxes[b] = 0
    for a in x:
        if a in boxes:
            boxes[a] += 1
    f = 0
    for val in boxes.values():
        if val == 0:
            f += 1
    if f < k:
        return 0 
    return 1


# def criteria_2_0(Afrq, x):
#     for a in Afrq:
#         if a not in x:








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
        s = file.read(900_000)
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
    N, L = 10_000, 1000
    X = get_N_texts(s, N, L)
    Y = []
# (a)
    # r = 5
    # for i in trange(len(X)):
    #     Y.append(dist_Vigenere(X[i],r, ukrDict,isText=True))

# (б)
    # l = 2
    # for i in trange(len(X)):
    #     Y.append(dist_Affin(X[i],l,ukrDict))

# (в) Рiвномiрно розподiлена послiдовнiсть символiв


# (г)
    # l = 2
    # for i in trange(len(X)):
    #     Y.append(dist_Fibonacci(X[i],l,ukrDict))

# Критерiї:
    # h = 11
    # A = frequency(s,1,probability=True)
    # Afrq = list(A.keys())[:h] # самые частые l-граммы

    # FP = 0 # False Positive
    # FN = 0 # False Negative
    # for x in X:
    #     FP += 1 - criteria_2_0(Afrq, x)
    #     x = dist_Vigenere(x,5,ukrDict,isText=True)
    #     FN += criteria_2_0(Afrq,x)
    # FP /= 2*N
    # FN /= 2*N

    # FP = 0
    # FN = 0
    # for x in X:
    #     FP += 1 - criteria_2_1(Afrq, x, k=h-3)
    #     x = dist_Vigenere(x,5,ukrDict,isText=True)
    #     FN += criteria_2_1(Afrq,x, k=h-3)
    # FP /= 2*N
    # FN /= 2*N

    # FP = 0
    # FN = 0
    # sFreq = frequency(s,1,probability=True)
    # for x in X:
    #     FP += 1 - criteria_2_2(Afrq, x, sFreq)
    #     x = dist_Vigenere(x,5,ukrDict,isText=True)
    #     FN += criteria_2_2(Afrq, x, sFreq)
    # FP /= 2*N
    # FN /= 2*N    
    
    # FP = 0
    # FN = 0
    # sFreq = frequency(s,1,probability=True)
    # print(sFreq.keys())
    # K = round(sum(sFreq.values()), 6)
    # for x in X:
    #     FP += 1 - criteria_2_3(Afrq, x, K)
    #     x = dist_Vigenere(x,5,ukrDict,isText=True)
    #     FN += criteria_2_3(Afrq, x, K)
    # FP /= 2*N
    # FN /= 2*N   
    
    # FP = 0
    # FN = 0
    # sAff = affinity(s,1)
    # k = 0.001
    # for x in X:
    #     FP += 1 - criteria_4_0(x, sAff, k)
    #     x = dist_Vigenere(x,5,ukrDict,isText=True)
    #     FN += criteria_4_0(x, sAff, k)
    # FP /= 2*N
    # FN /= 2*N 

    # FP = 0
    # FN = 0
    # k = 2
    # sFreq = frequency(s,1,probability=True)
    # for x in X:
    #     FP += 1 - criteria_5_0(x, sFreq, k)
    #     x = dist_Vigenere(x,5,ukrDict,isText=True)
    #     FN += criteria_5_0(x, sFreq, k)
    # FP /= 2*N
    # FN /= 2*N  


#############################################################

    # ukrBigrams = {}
    # j = 0
    # for k1 in ukrDict.keys():
    #     for k2 in ukrDict.keys():
    #         ukrBigrams[f'{k1}{k2}'] = j
    #         j += 1

    # h = 100
    # A = frequency(s,2,probability=True)
    # Afrq = list(A.keys())[:h] # самые частые l-граммы
    
    # FP = 0 # False Positive
    # FN = 0 # False Negative
    # for x in X:
    #     FP += 1 - criteria_2_0(Afrq, x)
    #     x = dist_Vigenere(x,5,ukrDict,isText=True)
    #     FN += criteria_2_0(Afrq,x)
    # FP /= 2*N
    # FN /= 2*N
    
    # FP = 0
    # FN = 0
    # for x in X:
    #     FP += 1 - criteria_2_1(Afrq, x, k=h-10)
    #     x = dist_Vigenere(x,5,ukrDict,isText=True)
    #     FN += criteria_2_1(Afrq,x, k=h-10)
    # FP /= 2*N
    # FN /= 2*N

    # FP = 0
    # FN = 0
    # sFreq = frequency(s,2,probability=True)
    # for x in X:
    #     FP += 1 - criteria_2_2(Afrq, x, sFreq)
    #     x = dist_Vigenere(x,5,ukrDict,isText=True)
    #     FN += criteria_2_2(Afrq, x, sFreq)
    # FP /= 2*N
    # FN /= 2*N


#####################################################
# Згенерировать случ. текст (несвязный)
    h = 11
    A = frequency(s,1,probability=True)
    Afrq = list(A.keys())[:h] # самые частые l-граммы
    L = 10_000
    X = ''
    j = random.randint(0,33)
    for i in range(L):
        X += list(ukrDict.keys())[j]
    
    X = dist_Vigenere(X, 10,ukrDict, isText=True)
    res = criteria_2_0(Afrq, X)
    

    
        


    exit()



if __name__ == "__main__":
    main()
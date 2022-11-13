import numpy as np
import re
import string
import os
from collections import Counter



def text_preprocessing(s):
    sNew = ''
    alphabetic = ['м', 'и', 'ж', 'в', 'е', 'о', 'н', 'з', 'ч', 'а', 'й', 'у', 'д', 'с', 'і', 'т', 'п', 'р', 'б', 'я', 'к', 'щ', 'ц', 'г', 'ш', 'л', 'ь', 'ю', 'є', 'х', 'ї', 'ф', 'ґ']
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





def main():

# Опрацювання тексту:
    s = ''
    with open('lab2/text.txt', 'r') as file:
        
        data = file.read()
        
        s = text_preprocessing(data)
    
    with open('lab2/newText.txt', 'w') as file:
        file.write(s)
        
# Частоти:
    monoFr = frequency(s, 1)
    biFr = frequency(s, 2)
# Ентропiя:
    monoEn = entropy(s,1)
    biEn = entropy(s,2)
# Iндекс Вiдповiдностi:
    monoAff = affinity(s,1)
    biAff = affinity(s,2)

    print(monoEn)
    print(biEn)
    print(monoAff)
    print(biAff)


   
    exit()
if __name__ == "__main__":
    main()

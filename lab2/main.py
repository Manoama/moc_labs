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

# def frequency(n):
#     if n == 1:






def main():

# Опрацювання тексту:
    s = ''
    with open('lab2/text.txt', 'r') as file:
        
        data = file.read()
        
        s = text_preprocessing(data)
        
# Частоти:
    # Монограми:
    length = len(s)
    c = Counter(s)
    for key, value in c.items():
        c[key] = value / length    

    print(c)
    # Бiграми:
    c = Counter(s[i : i + 2] for i in range(len(s) - 1))
    for key, value in c.items():
        c[key] = value / length    
    
    print(c)
    
if __name__ == "__main__":
    main()

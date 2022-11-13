import re
import string
import os

def text_preprocessing(s):
    sNew = ''
    alphabetic = ['м', 'и', 'ж', 'в', 'е', 'о', 'н', 'з', 'ч', 'а', 'й', 'у', 'д', 'с', 'і', 'т', 'п', 'р', 'б', 'я', 'к', 'щ', 'ц', 'г', 'ш', 'л', 'ь', 'ю', 'є', 'х', 'ї', 'ф', 'ґ']
    for i in s:
        if i.lower() in alphabetic:
            sNew += i.lower()
    sNew = sNew.replace('ґ','г')
    return sNew



s = ''

with open('lab2/text.txt', 'r') as file:
    data = file.read()
    print(len(data))
    s = text_preprocessing(data)
    print(len(s))




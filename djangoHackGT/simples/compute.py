import re

file = open('crap.txt','r')
data = file.read().replace('\n', '')
cleanString = re.sub('\W+',' ', data)
list = cleanString.split(' ')
dict = {}
file.close()
for x in list:
    if x not in dict:
        dict[x] = 1
    elif x in dict:
        dict[x] = dict[x] + 1
print(dict)

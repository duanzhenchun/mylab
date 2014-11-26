import re

s = '111222333aaaeeefff'
print re.sub('([0-9a-z])\\1','', s)


lst=['abc','dee','eee','dee']
lst2=[]
for i in sorted(lst):
    if lst2 and lst2[-1]== i:
        continue
    lst2.append(i)
print lst2
#['abc', 'dee', 'eee']


#only one unique, others are all pairs
lst = [123, 34343, 123, 23434, 34343]
uniq=reduce(lambda x,y:x^y, lst)
print uniq 

#2 unique
lst = [123, 34343, 123, 23434, 34343, 2]
res = reduce(lambda x,y:x^y, lst)

#find last bit==1 in res
i=1
while res:
    if res&1:
        break
    res=res>>1
    i=i<<1

lsts=[[],[]]
for j in lst:
    lsts[j&i!=0].append(j) 

for lst2 in lsts:
    print reduce(lambda x,y:x^y, lst2)
"""
2
23434
"""    


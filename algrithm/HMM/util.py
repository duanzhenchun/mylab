
def norm_dict(dic):
    total = sum(dic.values()) * 1.0
    if total <= 0:
        return
    for i in dic:
        dic[i] /= total
            
def norm_dict2(dic):
    """
    normalize dict[i][j]
    """
    total = 0.0
    for i in dic:
        total += sum(dic[i].values())
    if total <= 0:
        return
    for i in dic:
        for j in dic[i]:
            dic[i][j] /= total
            

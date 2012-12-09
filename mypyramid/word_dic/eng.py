#encoding:utf-8

def endicmaker(lang):
    import enchant
    dic=enchant.Dict(lang)
    def wrapper(word):
        return dic.check(word)
    return wrapper
iseng=endicmaker('en_US')

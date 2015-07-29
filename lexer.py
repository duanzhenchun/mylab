# simple math expression parser
 
def lexer(s):
    '''token generator, yields a list of tokens'''
    ix = 0
    while ix < len(s):
        if s[ix].isspace(): ix += 1
        elif s[ix] in "+-*/()":
            yield s[ix]; ix += 1
        elif s[ix].isdigit():
            jx = ix + 1
            while jx < len(s) and s[jx].isdigit(): jx += 1
            yield s[ix:jx]; ix = jx
        else:
            raise Exception("invalid char at %d: '%s'" % (ix, s[ix]))
    yield ""
 
if __name__ == '__main__':
    print list(lexer("1 + (2 - 3) * 456"))

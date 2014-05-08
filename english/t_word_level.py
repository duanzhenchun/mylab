from nltk.corpus import wordnet
import re
from stemming.porter2 import stem
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

st = PorterStemmer()
wnl = WordNetLemmatizer()

def word_lem(w):
    return st.stem(wnl.lemmatize(w.lower()))

f=open('all.num')
lst=f.readlines()
dic={}
for l in lst[-1:0:-1]:
    t = l.strip().split(' ')
    w = word_lem(t[1])
    dic[w] = max(dic.get(w,0), int(t[0]))

txt="""She woke with a gasp, not knowing who she was, or where.
The smell of blood was heavy in her nostrils… or was that her nightmare, lingering? She had dreamed of wolves again, of running through some dark pine forest with a great pack at her hells, hard on the scent of prey.

Half-light filled the room, grey and gloomy. Shivering, she sat up in bed and ran a hand across her scalp. Stubble bristled against her palm. I need to shave before Izembaro sees. Mercy, I’m Mercy, and tonight I’ll be raped and murdered. Her true name was Mercedene, but Mercy was all anyone ever called her…

Except in dreams. She took a breath to quiet the howling in her heart, trying to remember more of what she’d dreamt, but most of it had gone already. There had been blood in it, though, and a full moon overhead, and a tree that watched her as she ran."""

k=dic.get(word_lem('fastened'))
Word_pat = re.compile(r"[\w']+|\W+")

def gen_paras(txt):
    for line in txt.split('\n'):
        yield '<p>'
        for w0 in Word_pat.findall(line):
            if not w0.isalpha():
                yield w0
            else:
                w = word_lem(w0)
                if w in dic and dic[w]<= k:      
                    yield word_def(w0)
                else:
                    yield w0
        yield '</p>'


def word_def(w):
    ss = wordnet.synsets(w)
    if not ss:
        return w
    else:
        definition = '%s:\n%s' %(ss[0].name, ss[0].definition)
        return '<span title="%s" >%s</span>' %(definition, w)


def to_html(txt, title=""):
    return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>%s</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf8" />
	<style type="text/css">
		body{text-align:center;}
               .div_txt{text-align:left; width:70%%; margin:0 auto;} 
                span{background-color:yellow}
	</style>
</head>
<body>
<div class="div_txt">
%s
</div>
</body>
</html>""" %(title, txt)

f=open('tmp.html', 'w')
f.write(to_html(''.join(gen_paras(txt))))
f.close()


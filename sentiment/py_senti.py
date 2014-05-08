# coding=utf-8
import jieba.posseg
import os
import sys
import random
import crfsuite
from crf_utils import *
from utils import *
from template_senti import *


def gen_tags():
    folder, fn  = get_data_f_fn()
    docs = list(fn(folder))
    random.shuffle(docs)
    count =200
    for doc, is_pos in docs:
        count -=1
        if count<0:
            break
        for w_pos in jieba.posseg.cut(doc):
            w, pos = w_pos.word, w_pos.flag
            w = w.strip()
            if not w:
                continue
            yield '%s %s %s' %(w, pos, Sen_dic[is_pos])
        yield ''


class Trainer(crfsuite.Trainer):
    def message(self, s):
        sys.stdout.write(s)


def train(fi, model):
    trainer = Trainer()
    for xseq, yseq in instances(fi):
        trainer.append(xseq, yseq, 0)
    #http://www.chokkan.org/software/crfsuite/manual.html#id491233
    # Use L2-regularized SGD and 1st-order dyad features.
    trainer.select('l2sgd', 'crf1d')
    # This demonstrates how to list parameters and obtain their values.
    #for name in trainer.params():
    #    print name, trainer.get(name), trainer.help(name)
    
    # Set the coefficient for L2 regularization
    trainer.set('c2', '0.1')
    trainer.train(model, -1) 


def test(fi, fo, model):
    from sklearn.metrics import f1_score
    tagger = crfsuite.Tagger()
    tagger.open(model)
    y_true, y_pred = [], [] 
    for xseq, yseq0 in instances(fi):
        tagger.set(xseq)
        yseq = tagger.viterbi()
        fo.write('seq prob: %f\n' %tagger.probability(yseq))
        for t, y in enumerate(yseq):
            fo.write('%s, %s:%f\n' % (yseq0[t], y, tagger.marginal(y, t)))
        y_true.append(yseq0[0])
        y_pred.append(y)
        fo.write('\n')
    print [f1_score(y_true, y_pred, pos_label=None, average=ave) for ave in ('micro', 'macro', None)]
    #[0.62865497076023391, 0.42959425965018605, array([ 0.        ,  0.70619236,  0.55186722,  0.46031746])]


def main(ratio=0.8):
    data_src= './data/%s' %(len(sys.argv) > 1 and sys.argv[1] or 'ccf_nlp')
    model = '%s/crf.model' %data_src
    print "model:", model
    data = list(prepare())
    N = len(data)
    ntrain = int(N*ratio)
    print N, ntrain
    train_d, test_d = data[:ntrain], data[ntrain:]
    train(train_d, model)
    tag_out = open('%s/crf.tag' %data_src, 'w')
    test(test_d, tag_out, model)

def prepare():
    F = fields.split(' ')
    for X in readiter(gen_tags(), F, separator):
        feature_extractor(X, templates)
        yield ''.join(gen_features(X, 'y')).encode('utf8')


if __name__ == "__main__":
    main()

# coding=utf-8
import crfsuite

def feature_extractor(X, templates):
    apply_templates(X, templates)
    if X:
        # Append BOS and EOS features manually
        X[0]['F'].append('__BOS__')     # BOS feature
        X[-1]['F'].append('__EOS__')    # EOS feature

def gen_features(X, field=''):
    for x in X:
        if field:
            yield u'%s' % x[field]
        for a in x['F']:
            if isinstance(a, basestring):
                yield '\t%s' % escape(a)
            else:
                yield '\t%s:%f' % (escape(a[0]), a[1])
        yield '\n'
    #yield '\n'


def apply_templates(X, templates):
    """
    Generate features for an item sequence by applying feature templates.
    A feature template consists of a tuple of (name, offset) pairs,
    where name and offset specify a field name and offset from which
    the template extracts a feature value. Generated features are stored
    in the 'F' field of each item in the sequence.

    @type   X:      list of mapping objects
    @param  X:      The item sequence.
    @type   template:   tuple of (str, int)
    @param  template:   The feature template.
    """
    for template in templates:
        name = '|'.join(['%s[%d]' % (f, o) for f, o in template])
        for t in range(len(X)):
            values = []
            for field, offset in template:
                p = t + offset
                if p not in range(len(X)):
                    values = []
                    break
                values.append(X[p][field])
            if values:
                X[t]['F'].append('%s=%s' % (name, '|'.join(values)))

def readiter(fi, names, sep=' '):
    """
    Return an iterator for item sequences read from a file object.
    This function reads a sequence from a file object L{fi}, and
    yields the sequence as a list of mapping objects. Each line
    (item) from the file object is split by the separator character
    L{sep}. Separated values of the item are named by L{names},
    and stored in a mapping object. Every item has a field 'F' that
    is reserved for storing features.

    @type   fi:     file
    @param  fi:     The file object.
    @type   names:  tuple
    @param  names:  The list of field names.
    @type   sep:    str
    @param  sep:    The separator character.
    @rtype          list of mapping objects
    @return         An iterator for sequences.
    """
    X = []
    for line in fi:
        line = line.strip('\n')
        if not line:
            yield X
            X = []
        else:
            fields = line.split(sep)
            if len(fields) < len(names):
                raise ValueError(
                    'Too few fields (%d) for %r\n%s' % (len(fields), names, line))
            item = {'F': []}    # 'F' is reserved for features.
            for i in range(len(names)):
                item[names[i]] = fields[i]
            X.append(item)

def escape(src):
    """
    Escape colon characters from feature names.
    """
    return src.replace(':', '__COLON__')


def instances(fi, to_train=True):
    for line in fi:
        xseq = crfsuite.ItemSequence()
        yseq = crfsuite.StringList()
        lines = line.strip('\n').split('\n')
        for data in lines:
            fields = data.split('\t')
            if not fields[0]:
                print line
            item = crfsuite.Item()
            for field in fields[1:]:
                p = field.rfind(':')
                if p == -1:
                    # Unweighted (weight=1) attribute.
                    item.append(crfsuite.Attribute(field))
                else:
                    # Weighted attribute
                    item.append(crfsuite.Attribute(field[:p], float(field[p+1:])))

            xseq.append(item)
            if to_train:
                yseq.append(fields[0])
        yield xseq, yseq



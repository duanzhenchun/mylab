import sys
from crfutils import apply_templates, readiter, output_features
from crf_senti import templates, feature_extractor


def main():
    crfutils.main(feature_extractor, fields=fields, sep=separator) 
    fi = sys.stdin
    fo = sys.stdout
    F=('w', 'pos', 'y')
    for X in readiter(fi, F, options.separator):
        feature_extractor(X)
        output_features(fo, X, 'y')

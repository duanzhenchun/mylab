WKDIR="./data/ccf_nlp"
python crf_pre.py &&
python crf_senti.py < $WKDIR/prepare.txt > $WKDIR/all.txt &&
split -l 200010 all.txt &&
mv xaa train.txt && mv xab test.txt &&
crfsuite learn -a lbfgs -l -m alpha.model train.txt && 
crfsuite tag -qt -m alpha.model test.txt 
crfsuite dump alpha.model > alpha.out

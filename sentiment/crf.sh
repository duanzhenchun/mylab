DATA_T="ccf_nlp"
WKDIR="./data/$DATA_T"
python crf_pre.py $DATA_T &&
python crf_senti.py < $WKDIR/prepare.txt > $WKDIR/all.txt &&
cd $WKDIR &&
split -l 20116 all.txt &&
mv xaa train.txt && mv xab test.txt &&
crfsuite learn -a lbfgs -l -m alpha.model train.txt && 
crfsuite tag -qt -m alpha.model test.txt 
crfsuite dump alpha.model > alpha.dump

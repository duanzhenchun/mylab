#if size is 0
target=plus
if [[ ! -s $target ]];then exit 0;fi

. ~/my_env/bin/activate
python -c "import trans; trans.modify('$target')"
#if succeed
if [ $? == 0 ];then
    cat $target >> $target.bak
    >$target
fi
deactivate

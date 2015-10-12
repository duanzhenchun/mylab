#!/bin/bash

DEPT_NUM=$1

set -e
#echo DEPT_NUM $LDAP_ARG

#add more
for d1 in $(seq 1 $DEPT_NUM);do
    cat ou.ldif|sed "s#ou_all_#ou=dept${d1}#"|sed "s#ou_#dept${d1}#" > tmp.ldif && ldapadd ${LDAP_ARG} -f tmp.ldif && rm tmp.ldif
    for d2 in $(seq 5);do
        ou_2="dept${d1}${d2}"
        ou_all="ou=${ou_2},ou=dept${d1}"
        echo $ou_2, $ou_all
        cat ou.ldif|sed "s#ou_all_#${ou_all}#"|sed "s#ou_#${ou_2}#" > tmp.ldif && ldapadd ${LDAP_ARG} -f tmp.ldif && rm tmp.ldif
        for p1 in $(seq 4);do
            cat person.ldif|sed "s#name_#person${d1}${d2}${p1}#g"|sed "s#ou_all_#${ou_all}#"|sed "s#ou_#${ou_2}#" > tmp.ldif && ldapadd ${LDAP_ARG} -f tmp.ldif && rm tmp.ldif
        done
    done
done

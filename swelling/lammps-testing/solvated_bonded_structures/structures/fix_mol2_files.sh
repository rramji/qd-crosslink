#!/bin/bash

for i in ./preclean/*.mol2
do
name=`basename --suffix .mol2 $i`
python clean-mol2.py $i $name.tmp.mol2
obabel $name.tmp.mol2 -O $name.mol2 
rm $name.tmp.mol2 
done

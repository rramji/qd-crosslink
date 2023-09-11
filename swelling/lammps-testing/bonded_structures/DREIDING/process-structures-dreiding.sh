#!/bin/bash

ff="DREIDING"

for i in ../structures/*.mol2
do
name=`basename --suffix .mol2 $i`
echo "converting $name.mol2 to bgf"
~/scripts/mol2bgf.pl -m $i -b $name.bgf
echo "adding box to $name.bgf"
~/scripts/addBoxToBGF.pl $name.bgf $name.bgf
echo "typing atoms in $name.bgf with parameters from the $ff force field"
~/scripts/autoType.pl -i $name.bgf -f $ff -s $name.$ff.bgf
echo "creating sample lammps input for $name.dreid.bgf"
~/scripts/createLammpsInput.pl -b $name.$ff.bgf -f $ff -s $name -t "min heat"
mkdir -p $name
mv $name.* $name
mv *.$name* $name
done

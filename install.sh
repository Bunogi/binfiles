#!/bin/bash

set -o xtrace

FILES=".spacemacs .zprofile .zshrc .profile"
targetdir=~

rm -rf $targetdir/bin
ln -s $PWD/bin $targetdir/bin

for i in $FILES
do
	rm $targetdir/$i
       	ln -s $PWD/$i $targetdir/$i
	if [ $? != 0 ]
	then
		exit
	fi
done

rm ~/pkgs/st/config.h &&
cp stconfig.h ~/pkgs/st/config.h &&
cd ~/pkgs/st &&
make && sudo make install





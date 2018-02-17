#!/bin/bash

set -o xtrace

FILES=".spacemacs .zprofile .zshrc .profile .latexmk"
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
ln -s ~/pkgs/st/config.h stconfig.h &&
cd ~/pkgs/st &&
make && sudo make install

rm ~/.config/share/nautilus/scripts/*
for f in $PWD/nautilus/*
do
    b=$(basename "$f")
    ln -s "$f" "$HOME/.local/share/nautilus/scripts/$b"
done

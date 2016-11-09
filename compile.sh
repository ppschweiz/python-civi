#!/bin/bash

CURDIR="$(pwd)"
TARDIR="$CURDIR/tmp/"
TMPDIR="/tmp/tex-compile"
rm -rf $TMPDIR
mkdir $TMPDIR
cp people.csv $TMPDIR/
cd $TMPDIR/
git clone https://github.com/ppschweiz/factura-content 
cp factura-content/* .
cp factura-content/$1/factura.tex .
xelatex factura.tex
xelatex factura.tex
rm -rf $TARDIR
mkdir $TARDIR
cp factura.pdf $TARDIR/
cp factura-content/$1/$2.txt $TARDIR/msg.txt
cp factura-content/$1/$2.html $TARDIR/msg.html
cp factura-content/$1/$2.subject $TARDIR/msg.subject
cd $CURDIR/


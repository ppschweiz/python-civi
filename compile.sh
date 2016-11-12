#!/bin/bash

CURDIR="$(pwd)"
TARDIR="$CURDIR/tmp/"
TMPDIR="/tmp/tex-compile"

rm -rf $TMPDIR &> /dev/null

mkdir $TMPDIR &> /dev/null
if [ $? -ne 0 ]
then
  echo "Error creating $TMPDIR"
  exit 1
fi

cp people.csv $TMPDIR/
if [ $? -ne 0 ]
then
  echo "Error copying peole.csv"
  exit 2
fi

cd $TMPDIR/
if [ $? -ne 0 ]
then
  echo "Error changing to $TMPDIR"
  exit 3
fi

echo "Cloning factura content git..."
git clone https://github.com/ppschweiz/factura-content &> /dev/null
if [ $? -ne 0 ]
then
  echo "Error cloning factura-content"
  exit 4
fi

cp factura-content/*.* .
if [ $? -ne 0 ]
then
  echo "Error copying factura-content"
  exit 5
fi

cp factura-content/$1/factura.tex .
if [ $? -ne 0 ]
then
  echo "Error copying language specific factura"
  exit 6
fi

echo "Xelatex round 1..."
xelatex -interaction nonstopmode -halt-on-error -file-line-error factura.tex > /dev/null
if [ $? -ne 0 ]
then
  echo "Error in xelatex"
  exit 7
fi

echo "Xelatex round 2..."
xelatex -interaction nonstopmode -halt-on-error -file-line-error factura.tex &> /dev/null
if [ $? -ne 0 ]
then
  echo "Error in xelatex"
  exit 8
fi

rm -rf $TARDIR &> /dev/null

mkdir $TARDIR &> /dev/null
if [ $? -ne 0 ]
then
  echo "Error creating $TARDIR"
  exit 9
fi

cp factura.pdf $TARDIR/
if [ $? -ne 0 ]
then
  echo "Error copying factura.pdf"
  exit 10
fi

cp factura-content/$1/$2.txt $TARDIR/msg.txt
if [ $? -ne 0 ]
then
  echo "Error copying msg.txt"
  exit 11
fi

cp factura-content/$1/$2.html $TARDIR/msg.html
if [ $? -ne 0 ]
then
  echo "Error copying msg.html"
  exit 12
fi

cp factura-content/$1/$2.subject $TARDIR/msg.subject
if [ $? -ne 0 ]
then
  echo "Error copying msg.subject"
  exit 13
fi

cd $CURDIR/
if [ $? -ne 0 ]
then
  echo "Error changing to $CURDIR"
  exit 14
fi

exit 0

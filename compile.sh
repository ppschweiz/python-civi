#!/bin/bash

CURDIR="$(pwd)"
TMPDIR='/tmp'
TARGETDIR="$TMPDIR/factura"
COMPILEDIR="$TMPDIR/compile"
CONTENTDIR="$TMPDIR/factura-content"

rm -rf $COMPILEDIR &> /dev/null

mkdir $COMPILEDIR &> /dev/null
if [ $? -ne 0 ]
then
  echo "Error creating $COMPILEDIR"
  exit 1
fi

cd $COMPILEDIR/
if [ $? -ne 0 ]
then
  echo "Error changing to $COMPILEDIR"
  exit 3
fi

cp $CONTENTDIR/*.* .
if [ $? -ne 0 ]
then
  echo "Error copying factura-content"
  exit 5
fi

cp $CONTENTDIR/$1/factura.tex .
if [ $? -ne 0 ]
then
  echo "Error copying language specific factura"
  exit 6
fi

cp $TARGETDIR/people.csv .
if [ $? -ne 0 ]
then
  echo "Error copying member data for factura"
  exit 6
fi

#echo "Xelatex round 1..."
xelatex -interaction nonstopmode -halt-on-error -file-line-error factura.tex > /dev/null
if [ $? -ne 0 ]
then
  echo "Error in xelatex"
  exit 7
fi

#echo "Xelatex round 2..."
xelatex -interaction nonstopmode -halt-on-error -file-line-error factura.tex &> /dev/null
if [ $? -ne 0 ]
then
  echo "Error in xelatex"
  exit 8
fi

cp factura.pdf $TARGETDIR/
if [ $? -ne 0 ]
then
  echo "Error copying factura.pdf"
  exit 10
fi

cd $CURDIR/
if [ $? -ne 0 ]
then
  echo "Error changing to $CURDIR"
  exit 14
fi

exit 0

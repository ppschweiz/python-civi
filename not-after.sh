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

cp factura-content/not-after $CURDIR/ &> /dev/null 
if [ $? -ne 0 ]
then
  echo "Error copying not-after"
  exit 5
fi

cd $CURDIR/
if [ $? -ne 0 ]
then
  echo "Error changing to $CURDIR"
  exit 6
fi

exit 0

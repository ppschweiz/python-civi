#!/bin/bash

CURDIR="$(pwd)"
TMPDIR='/tmp'
CONTENTDIR="$TMPDIR/factura-content"

rm -rf $CONTENTDIR &> /dev/null

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

cd $CURDIR/
if [ $? -ne 0 ]
then
  echo "Error changing to $CURDIR"
  exit 14
fi

exit 0

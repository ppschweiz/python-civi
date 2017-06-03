#!/bin/bash

CURDIR="$(pwd)"
TMPDIR='/tmp'
CONTENTDIR="$TMPDIR/$1-content"

rm -rf $CONTENTDIR &> /dev/null

cd $TMPDIR/
if [ $? -ne 0 ]
then
  echo "Error changing to $TMPDIR"
  exit 3
fi

echo "Cloning $1 content git..."
git clone https://github.com/ppschweiz/$1-content &> /dev/null
if [ $? -ne 0 ]
then
  echo "Error cloning $1-content"
  exit 4
fi

cd $CURDIR/
if [ $? -ne 0 ]
then
  echo "Error changing to $CURDIR"
  exit 14
fi

exit 0

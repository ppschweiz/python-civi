#!/bin/bash

CURDIR="$(pwd)"
TMPDIR='/tmp'
TARGETDIR="$TMPDIR/$1"

rm -rf $TARGETDIR &> /dev/null

mkdir $TARGETDIR &> /dev/null
if [ $? -ne 0 ]
then
  echo "Error creating $TARGETDIR"
  exit 1
fi

exit 0

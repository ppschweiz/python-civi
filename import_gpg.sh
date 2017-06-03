#!/bin/bash

gpg --import $1/*
gpg --keyserver pgp.mit.edu --refresh-keys

exit 0


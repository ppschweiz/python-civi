#!/bin/bash

while :
do
	echo "running at $(date)"

	python3 ./run-facturer.py HOT

	for i in {1..18}
	do
		for j in {1..600}
		do
			sleep 1
		done

		echo "loop $i of 18 at $(date)"
	done
done


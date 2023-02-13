#!/bin/bash

for n in $(cat files.txt )
do
    echo "Working on $n"
    mpremote connect /dev/cu.usbmodem14201 cp :$n .
done

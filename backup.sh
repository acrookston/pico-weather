#!/bin/bash


device=''
pattern='*usbmodem*'

for candidate in $(mpremote connect list)
do
  for detail in $(echo $candidate | tr " " "\n")
  do
    if [[ "$detail" == $pattern ]]; then
      device=$detail
    fi
  done
done


if [ -z "$device" ]
then
  echo "NO DEVICE FOUND"
else
  echo "Found device: $device"
  for n in $(cat files.txt)
  do
      echo "Working on $n"
      mpremote connect $device cp :$n .
  done
fi

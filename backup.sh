#!/bin/bash


fn_backup () {
  for n in $(cat files.txt)
  do
    echo "Working on $n"
    mpremote connect $device cp :$n .
  done
}

fn_install () {
  for n in $(cat files.txt)
  do
    echo "Working on $n"
    mpremote connect $device cp $n :
  done
}

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
  exit 0
fi

echo "Using device: $device"

case $1 in
  "backup")
    fn_backup
    exit;;
  "install")
    fn_install
    exit;;
esac

#!/bin/bash

device=''

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

fn_run () {
  mpremote connect $device run main.py
}

fn_repl () {
  mpremote connect $device repl
}

fn_ls () {
  mpremote connect $device fs ls
}

fn_get_logs () {
  echo "Fetching application.log"
  mpremote connect $device cp :application.log .
  echo "Fetching error.log"
  mpremote connect $device cp :error.log .
}

fn_rm_logs () {
  echo "Fetching application.log"
  mpremote connect $device fs rm application.log
  echo "Fetching error.log"
  mpremote connect $device fs rm error.log
}

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

echo "Found device: $device"

case $1 in
  "backup")
    fn_backup
    exit;;
  "install")
    fn_install
    exit;;
  "device")
    # Already printed
    exit;;
  "run")
    fn_run
    exit;;
  "repl")
    fn_repl
    exit;;
  "ls")
    fn_ls
    exit;;
  "logs")
    fn_get_logs
    exit;;
  "rm-logs")
    fn_rm_logs
    exit;;
esac

# Raspberry Pi (Pico) Weather Station / Home System

This projects is still very much in progress, and I do not get too much time to work on  it these days, however I consider the code I push to this repo to be mostly stable, call it "beta quality".

## Introduction

I started this as a project to explore and figure out some fun stuff with IoT and building a connected home.

The goal is to replace a classic indoor/outdoor temperature station with a connected, more advanced system. Like most people I have a traditional temperature sytem with an indoor base station with a screen and an outdoor wireless sensor.

I want to create a system which has sensors in multiple rooms, including outdoor, garage and greenhouse sensors. It should also be accessible via wifi, i.e. through an app, and it should keep readings over time for statistics and graphs. It could also fetch other information like weather data or public transport schedules.

## The setup

Since I had prior experience with Raspberry Pi I felt comfortable using them. I've got a little experience with ESP32 boards but I'm not very comfortable coding in C.

When I started this project (and still true when writing) Raspberry Pi is extremly hard to get a hold of. Luckily I was able to get my hands on some Raspberry Pi Picos. When I started this, the Pico W did not exist, but if you want to do any sort of wireless work (which this is) I stronlgy recommend getting the Pico W, which I eventually switched to.

My original plan was to have the Raspberry Pi Pico W upload metrics directly to a cloud based data store, but the Pico has very poor SSL support, and since most (all?) cloud based systems use SSL for communication this was a no go. Instead I had a Raspberry Pi 3 lying around since before and I decided to use this as a proxy at first, but instead or writing a https proxy I installed Influx DB directly on Pi 3.

Another challenge was getting the time and date to the Picos since they do not have NTP or the ability to store time. To get around this I installed Nginx on the Pi 3 and wrote a simple php script to deliver the date and time to the Picos.

I also used a 128x64 OLED I2C screen from AZDelivery and of course the DHT22 temperature and humidity sensor, a push button and two 10k ohm resistors. Here is the connection diagram, but the pins are configurable in config.py.

## ![pico-dht22-i2c](/Users/andy/code/pi/pico-dht22-i2c.png)



Vision for what the small screen can display, some of this is in place already:

![pico-screen](/Users/andy/code/pi/pico-screen.png)

## Learnings

### Don't use Pico with ESP01 (ESP8266)

I spent A LOT of time following guides to get the Pico (non-W) to connect to wifi via the ESP01 chip. This seems to work in some cases but the communication or power supply to the EPO01 randomly breaks and is hard to recover. I've left the code for ESP01 in the repo but I do not recommend using it - or maybe somebody can help me fix the issues!

### Pico W can't do HTTPS requests

As I mentioned already the Pico or Pico W can't do HTTPS requests due to bad SSL support. Don't try to design a system which requires the Pico to connect.

# LICENSE

Apache 2.0
# Weightage-Based-Mail-filtering 
 




## Introduction

This project was inspired by the works of author Carl Newport to attempt to solve the problem of wading through dozens of emails to loook for something important, especially for university students who frankly dont have the time or attention span to do so. Coded entirely in python and put together with the software equivalent of duct tape, it uses the unintelligable Gmail API to print a list of gmail urls in order of priority. 

## Working

For now the code pulls a list of recent emails, compares it with a list of keywords to find the number of matches orders, combines it with the list of email ids, then orders that and spits them out in the form of a list of gmail urls. For now there isn't much weightage going on since technically, all  key words have the same weightage. Soon I might implement proper keyword 'weighing' but for now this is good enough

## How to use the repository

### Setup
-Clone the repository and install all relevant libraries\
-Insert your own email in line 22 of gmailstuff.py\
-Run quickstart.py

### Usage
-Run gmailstuff.py \
-open the printed urls 

## Further Work

I've already mentioned that I want to add proper keyword 'weighing' but I really want to recreate the entire thing in tensorflow or numpy for increased efficiency. For now however, I might just work on optimizing the existing code in my freetime

## P.S

This is my first ever github repository and my first proper python project and I'm really proud of it : )


#!/bin/bash

rm -f data-02-option_data.*.csv

cmd-02-create-option-info.py --char A &
cmd-02-create-option-info.py --char B &
cmd-02-create-option-info.py --char C &
cmd-02-create-option-info.py --char D &
wait
cmd-02-create-option-info.py --char E &
cmd-02-create-option-info.py --char F &
cmd-02-create-option-info.py --char G &
cmd-02-create-option-info.py --char H &
wait
cmd-02-create-option-info.py --char I &
cmd-02-create-option-info.py --char J &
cmd-02-create-option-info.py --char K &
cmd-02-create-option-info.py --char L &
wait
cmd-02-create-option-info.py --char M &
cmd-02-create-option-info.py --char N &
cmd-02-create-option-info.py --char O &
cmd-02-create-option-info.py --char P &
wait
cmd-02-create-option-info.py --char Q &
cmd-02-create-option-info.py --char R &
cmd-02-create-option-info.py --char S &
cmd-02-create-option-info.py --char T &
wait
cmd-02-create-option-info.py --char U &
cmd-02-create-option-info.py --char V &
cmd-02-create-option-info.py --char W &
cmd-02-create-option-info.py --char X &
wait
cmd-02-create-option-info.py --char Y &
cmd-02-create-option-info.py --char Z &
wait

cat data-02-option_data.*.csv > data-03-option_data.csv
spd-say "Back To Work!"

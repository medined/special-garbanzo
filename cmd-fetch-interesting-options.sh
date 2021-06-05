#!/bin/bash

rm -f log-*.log
rm -f data-02-option_data.*.csv

cmd-02-create-option-info.py --char A &
cmd-02-create-option-info.py --char C &
cmd-02-create-option-info.py --char S &
wait
cmd-02-create-option-info.py --char M &
cmd-02-create-option-info.py --char G &
cmd-02-create-option-info.py --char P &
wait
cmd-02-create-option-info.py --char T &
cmd-02-create-option-info.py --char F &
cmd-02-create-option-info.py --char R &
wait
cmd-02-create-option-info.py --char N &
cmd-02-create-option-info.py --char H &
cmd-02-create-option-info.py --char B &
wait
cmd-02-create-option-info.py --char L &
cmd-02-create-option-info.py --char I &
cmd-02-create-option-info.py --char V &
wait
cmd-02-create-option-info.py --char E &
cmd-02-create-option-info.py --char D &
cmd-02-create-option-info.py --char J &
wait
cmd-02-create-option-info.py --char K &
cmd-02-create-option-info.py --char O &
cmd-02-create-option-info.py --char Q &
wait
cmd-02-create-option-info.py --char Y &
cmd-02-create-option-info.py --char U &
cmd-02-create-option-info.py --char W &
wait
cmd-02-create-option-info.py --char X &
cmd-02-create-option-info.py --char Z &

# rm tee-fetch-interesting-options.out; time cmd-fetch-interesting-options.sh | tee tee-fetch-interesting-options.out
# grep Many tee-fetch-interesting-options.out
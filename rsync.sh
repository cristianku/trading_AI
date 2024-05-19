#!/bin/bash
rsync -avz -e "ssh"  /Users/cristianku/GitHub/trading_AI/* cristianku@fedora-deep:~/projects/trading_AI --delete



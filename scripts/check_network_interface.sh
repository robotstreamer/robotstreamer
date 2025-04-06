#!/bin/bash
I=wlan0; L=/var/log/net-restart.log
ping -c1 -W1 8.8.8.8 >/dev/null || {
  echo "$(date) - No internet, restarting $I" >> $L
  ip l s $I down; sleep 2; ip l s $I up
  echo "$(date) - Restart complete" >> $L
}


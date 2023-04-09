#!/usr/bin/env bash

echo "create a dmx service ..."
sudo cp dmx.sh /etc/init.d/dmx
sudo cp dmx.service /etc/systemd/system
sudo chmod +x /etc/init.d/dmx
sudo service dmx start
sudo service dmx status
echo "created the dmx service"

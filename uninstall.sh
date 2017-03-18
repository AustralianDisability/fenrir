#!/bin/bash
#Basic install script for fenrir.
cat << EOF
fenrir is going to remove.
every script and settings are lost.
EOF

# ask
read -p "This will remove fenrir and settings. Press ctrl+c to cancel, or enter to continue." continue

# do it
unlink /usr/bin/fenrir
rm -r /opt/fenrir
rm -r /usr/share/fenrir
rm -r /etc/fenrir
rm -r /usr/share/sounds/fenrir
rm /usr/lib/systemd/system/fenrir.service

# success message
cat << EOF
fenrir is removed
EOF

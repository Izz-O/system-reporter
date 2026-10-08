#!/bin/bash

echo "System Information Report"
echo "Hostname: $(hostname)"
echo "Current user: $(whoami)"

echo "OS: $(grep PRETTY_NAME /etc/os-release |  cut -d= -f2  | tr -d '"')" 
echo "Kernel: $9(uname -r)"

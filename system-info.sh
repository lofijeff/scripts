#!/bin/bash

RED="\e[91m"
GREEN="\e[92m"
YELLOW="\e[93m"
BLUE="\e[94m"
PURPLE="\e[95m"
AQUA="\e[96m"
GREY="\e[90m"
RESET="\e[0m"

ICON_TIME=""
ICON_RAM="󰍛"
ICON_CPU=""
ICON_BATTERY=""
ICON_CUP_TEMP=""

TIME=$(date +"%H:%M")

read RAM_USED RAM_TOTAL <<<$(free -m | awk '/Mem:/ { print $3, $2 }')
RAM_PERCENT=$((100 * RAM_USED / RAM_TOTAL))

CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{printf("%.1f", 100 - $8)}')
CPU_TEMP=$(sensors | grep 'Tctl' | awk '{print $2}' | sed 's/+//')

if command -v upower &>/dev/null; then
  BATTERY_PERCENT=$(upower -i $(upower -e | grep BAT) | grep -E "percentage" | awk '{print $2}')
elif command -v acpi &>/dev/null; then
  BATTERY_PERCENT=$(acpi -b | grep -o '[0-9]\+%' | head -n1)
else
  BATTERY_PERCENT="N/A"
fi

printf "${BLUE}"
figlet -f big "$TIME"
printf "${RESET}"

echo -e "${GREEN} ${ICON_RAM} RAM     ${RESET}: ${RAM_PERCENT}%"
echo -e "${YELLOW} ${ICON_CPU} CPU     ${RESET}: ${CPU_USAGE} %"
echo -e "${RED} ${ICON_CUP_TEMP} TEMP    ${RESET}: ${CPU_TEMP}"
echo -e "${PURPLE} ${ICON_BATTERY} Battery ${RESET}: ${BATTERY_PERCENT}"

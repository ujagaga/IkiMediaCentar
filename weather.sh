#!/bin/bash

data="$(inxi -W Kikinda,RS | grep Temperature)"

data1="$(echo $data | cut -d ':' -f 2)"
temperature="$(echo $data1 | cut -d ' ' -f 1)°C"

data2="$(echo $data | cut -d ':' -f 3)"
conditions=${data2::-13}

msg="$temperature $conditions"
echo $msg > /tmp/display
#echo $msg

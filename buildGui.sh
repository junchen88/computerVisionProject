#!/usr/bin/env bash

uiFileName="projectGui.ui"
pyFileName="projectGui.py"

pyuic5 "$uiFileName" > "$pyFileName"

sed -i 's/qwt_plot/qwt/' "$pyFileName"
sed -i 's/qwt_text_label/qwt.text/' "$pyFileName"

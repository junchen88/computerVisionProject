#!/usr/bin/env bash

uiFileName="ControlGuiBase.ui"
pyFileName="ControlGuiBase.py"

pyuic5 "$uiFileName" > "$pyFileName"

sed -i 's/Ui_ControlGuiBase/ControlGuiBase/' "$pyFileName"
sed -i 's/qwt_plot/qwt/' "$pyFileName"
sed -i 's/qwt_text_label/qwt.text/' "$pyFileName"

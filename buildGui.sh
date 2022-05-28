#!/usr/bin/env bash

pyuic5 projectGui.ui > projectGui.py

sed -i 's/qwt_plot/qwt/' projectGui.py 
sed -i 's/qwt_text_label/qwt.text/' projectGui.py

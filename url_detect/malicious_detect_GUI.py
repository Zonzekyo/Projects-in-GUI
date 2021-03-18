#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import PySimpleGUI as sg
from configparser import ConfigParser

def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None       

    retval = p.wait(timeout)
    return (retval, output)


layout = [  [sg.Text('Outputs will be shown here')],
            [sg.Output(size=(70,20)),],
            [sg.Text('Enter URL(s) that wanted to be checked (Click initiate if newer data set is available):')],
            [sg.Button('Initiate'), sg.Input(key='_URL_')],
            [sg.Button('Run')]
         ]

window = sg.Window('Detect Malicious URL(s)', layout)


while True:             # Event Loop
    event, values = window.Read()
    url = values['_URL_']
    if event in (None, 'Exit'):
        break
    elif event == 'Initiate':  
        runCommand(cmd="python3 malicious_url.py", window=window)
    elif event == 'Run':  
        runCommand(cmd="python3 test_url.py "+ url, window=window)
   
window.Close()


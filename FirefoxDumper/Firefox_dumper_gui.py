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

def get_sections(profiles):
    window=None
    """
    Returns hash of profile numbers and profile names.
    """
    sections = {}
    i = 1
    for section in profiles.sections():
        if section.startswith("Profile"):
            sections[str(i)] = profiles.get(section, "Path")
            i += 1
        else:
            continue
    window.Refresh() if window else None
    return sections

def print_sections(basepath, sections):
    """
    Prints all available sections to an textIOWrapper (defaults to sys.stderr)
    """
    print ('List of available profiles:')
    for number in sorted(sections):
        profile = os.path.join(basepath,sections[number])
        print (number + '. ' + profile)
    
def read_profiles(basepath):
    """
    Parse Firefox profiles in provided location.
    If list_profiles is true, will exit after listing available profiles.
    """
    profileini = os.path.join(basepath, "profiles.ini")
    # Read profiles from Firefox profile folder
    profiles = ConfigParser()
    profiles.read(profileini)
    print_sections(basepath, get_sections(profiles))


def list_profiles():
    if os.name == "nt":
        profile_path = os.path.join(os.environ['APPDATA'], "Mozilla", "Firefox")
    elif os.uname()[0] == "Darwin":
        profile_path = "~/Library/Application Support/Firefox"
    else:
        profile_path = "~/.mozilla/firefox"
    basepath = os.path.expanduser(profile_path)
    read_profiles(basepath)


layout = [  [sg.Text('Outputs will be shown here')],
            [sg.Output(size=(250,35)),],
            [sg.Text('Enter the profile directory')],
            [sg.Button('List Profiles'), sg.Input(key='_Profile_')],
            [sg.Button('Export')],
            [sg.Button('Addons'), sg.Button('Search'), sg.Button('Bookmarks'),
            sg.Button('CertOverride'), sg.Button('Cookies'), sg.Button('Downloads'),
            sg.Button('Forms'), sg.Button('History'), sg.Button('Permissions'),
            sg.Button('Keypinning'), sg.Button('Cache'), sg.Button('Preferences'),
            sg.Button('Passwords'), sg.Button('Permissions'),sg.Button('Session'),
            sg.Button('Summary'), sg.Button('Thumbnails')] ]

window = sg.Window('Firefox Dumper', layout)


while True:             
    event, values = window.Read()
    profile = values['_Profile_']
    if event in (None, 'Exit'):
        break
    elif event == 'Export':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Export .", window=window)
    elif event == 'Addons':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Addons", window=window)
    elif event == 'Search':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Search", window=window)
    elif event == 'Bookmarks':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Bookmarks", window=window)
    elif event == 'CertOverride':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Certoverride", window=window)
    elif event == 'Cookies':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Cookies", window=window)
    elif event == 'Downloads':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Downloads", window=window)
    elif event == 'Forms':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Forms", window=window)
    elif event == 'History':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --History", window=window)
    elif event == 'Permissions':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Permissions", window=window)
    elif event == 'Keypinning':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Keypinning", window=window)
    elif event == 'Cache':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --OfflineCache", window=window)
    elif event == 'Preferences':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Preferences", window=window)
    elif event == 'Passwords':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Passwords", window=window)
    elif event == 'Permissions':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Permissions", window=window)
    elif event == 'Session':  
       runCommand(cmd="python3 dumpzilla.py "+ profile +" --Session", window=window)
    elif event == 'Summary':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Summary", window=window)
    elif event == 'Thumbnails':  
        runCommand(cmd="python3 dumpzilla.py "+ profile +" --Thumbnails", window=window)
    elif event == 'List Profiles':
        list_profiles()

window.Close()

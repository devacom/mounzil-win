#!/usr/bin/env python3
# coding: utf-8
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import os
import warnings
import sys
import platform
import shutil

# finding os platform
os_type = platform.system()

if os_type == 'Linux' or os_type == 'FreeBSD' or os_type == 'OpenBSD':
    from setuptools import setup, Command, find_packages
    setuptools_available = True
    print(os_type + " detected!")
else:
    print('This script is only work for GNU/Linux or BSD!')
    sys.exit(1)

# Checking dependencies!
not_installed = ''

# PyQt5 or PySide6
try:
    import PySide6
    print('python3-pyside6 is found')
    pyside6_is_installed = True
except:
    pyside6_is_installed = False

if not(pyside6_is_installed):
    try:
        import PyQt5
        print('python3-pyqt5 is found')
    except:
        print('Error : python3-pyqt5 or pyside6 must be installed!')
        not_installed = not_installed + '(PyQt5 or PySide6) '

# python3-requests
try:
    import requests
    print('python3-requests is found!')
except:
    print('Error : requests is not installed!')
    not_installed = not_installed + 'python3-requests, '

# python3-setproctitle
try:
    import setproctitle
    print('python3-setproctitle is found!')
except:
    print("Warning: setproctitle is not installed!")
    not_installed = not_installed + 'python3-setproctitle, '

# psutil
try:
    import psutil
    print('python3-psutil is found!')
except:
    print("Warning: python3-psutil is not installed!")
    not_installed = not_installed + 'psutil, '

# yt_dlp
try:
    import yt_dlp
    print('yt-dlp is found')
except:
    print('Warning: yt-dlp is not installed!')
    not_installed = not_installed + 'yt-dlp, '

# aria2
answer = os.system('aria2c --version 1>/dev/null')
if answer != 0:
    print("Error aria2 not installed!")
    not_installed = not_installed + 'aria2c, '
else:
    print('aria2 is found!')

# libnotify-bin
answer = os.system('notify-send --version 1>/dev/null')
if answer != 0:
    print("Error libnotify-bin is not installed!")
    not_installed = not_installed + 'libnotify-bin, '
else:
    print('libnotify-bin is found!')

# paplay
answer = os.system('paplay --version 1>/dev/null')
if answer != 0:
    print("Warning: paplay not installed!You need pulseaudio for sound notifications!")
    not_installed = not_installed + 'paplay, '
else:
    print('paplay is found!')

# sound-theme-freedesktop
if os_type == 'Linux':
    notifications_path = '/usr/share/sounds/freedesktop/stereo/'
elif os_type == 'FreeBSD' or os_type == 'OpenBSD':
    notifications_path = '/usr/local/share/sounds/freedesktop/stereo/'

if os.path.isdir(notifications_path):
    print('sound-theme-freedesktop is found!')
else:
    print('Warning: sound-theme-freedesktop is not installed! you need this package for sound notifications!')
    not_installed = not_installed + 'sound-theme-freedesktop'

# ffmpeg
answer = os.system('ffmpeg -version 1>/dev/null')
if answer != 0:
    print("Warning: ffmpeg not installed!")
    not_installed = not_installed + 'ffmpeg, '
else:
    print('ffmpeg is found!')


# show warning , if dependencies not installed!
if not_installed != '':
    print('########################')
    print('####### WARNING ########')
    print('########################')
    print('Some dependencies are not installed .It causes some problems for mounzil! : \n')
    print(not_installed + '\n\n')
    answer = input('Do you want to continue?(y/n)')
    if answer not in ['y', 'Y', 'yes']:
        sys.exit(1)

if sys.argv[1] == "test":
    print('We have not unit test :)')
    sys.exit('0')

DESCRIPTION = 'Mounzil'

if os_type == 'Linux':
    DATA_FILES = [
        ('/usr/share/man/man1/', ['man/mounzil.1.gz']),
        ('/usr/share/applications/', ['xdg/com.github.devacom.mounzil.desktop']),
        ('/usr/share/metainfo/', ['xdg/com.github.devacom.mounzil.appdata.xml']),
        ('/usr/share/icons/hicolor/scalable/apps/', ['resources/mounzil.svg']),
        ('/usr/share/icons/hicolor/scalable/apps/', ['resources/mounzil-tray.svg'])
    ]
elif os_type == 'FreeBSD' or os_type == 'OpenBSD':
    DATA_FILES = [
        ('/usr/local/share/man/man1/', ['man/mounzil.1.gz']),
        ('/usr/local/share/applications/', ['xdg/com.github.devacom.mounzil.desktop']),
        ('/usr/local/share/metainfo/', ['xdg/com.github.devacom.mounzil.appdata.xml']),
        ('/usr/local/share/pixmaps/', ['resources/mounzil.svg']),
        ('/usr/local/share/pixmaps/', ['resources/mounzil-tray.svg'])
    ]


# finding current directory
cwd = os.path.abspath(__file__)
setup_dir = os.path.dirname(cwd)

# clearing __pycache__
src_pycache = os.path.join(setup_dir, 'mounzil', '__pycache__')
gui_pycache = os.path.join(setup_dir, 'mounzil', 'gui', '__pycache__')
scripts_pycache = os.path.join(setup_dir, 'mounzil', 'scripts', '__pycache__')
constants_pycache = os.path.join(setup_dir, 'mounzil', 'constants', '__pycache__')

for folder in [src_pycache, gui_pycache, scripts_pycache, constants_pycache]:
    if os.path.isdir(folder):
        shutil.rmtree(folder)
        print(str(folder)
              + ' is removed!')


# Creating man page file
mounzil_man_page = os.path.join(setup_dir, 'man', 'mounzil.1')
os.system('gzip -f -k -9 "'
          + mounzil_man_page
          + '"')
print('man page file is generated!')

setup(
    name='mounzil',
    version='1.0.0',
    license='GPL3',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    include_package_data=True,
    url='https://github.com/devacom/mounzil',
    author='Taha H. Nouibat',
    author_email='devacom@protonmail.com',
    maintainer='Taha H. Nouibat',
    maintainer_email='devacom@protonmail.com',
    packages=(
        'mounzil', 'mounzil.constants',
        'mounzil.scripts', 'mounzil.gui',
    ),
    data_files=DATA_FILES,
    entry_points={
        'console_scripts': [
            'mounzil = mounzil.__main__'
        ]
    }
)

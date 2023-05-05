# -*- coding: utf-8 -*-

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


# THIS FILE CONTAINING SOME VARIABLES , ... THAT USING FOR INITIALIZING mounzil

from mounzil.scripts.useful_tools import determineConfigFolder, returnDefaultSettings
from mounzil.scripts.browser_integration import browserIntegration
from mounzil.scripts import osCommands
import subprocess
import shutil
import time
import os

try:
    from PySide6.QtCore import QSettings
except:
    from PyQt5.QtCore import QSettings

# initialization

# download manager config folder .
config_folder = determineConfigFolder()

# mounzil tmp folder path
mounzil_tmp = os.path.join(config_folder, 'mounzil_tmp')

# create folders
for folder in [config_folder, mounzil_tmp]:
    osCommands.makeDirs(folder)

# devacom.log file contains mounzil log.
from mounzil.scripts import logger

# refresh logs!
log_file = os.path.join(str(config_folder), 'devacom.log')

# get current time
current_time = time.strftime('%Y/%m/%d %H:%M:%S')

# find number of lines in log_file.
with open(log_file) as f:
    lines = sum(1 for _ in f)

# if number of lines in log_file is more than 300, then keep last 200 lines in log_file.
if lines < 300:
    f = open(log_file, 'a')
    f.writelines('===================================================\n'
                 + 'mounzil Download Manager, '
                 + current_time
                 + '\n')
    f.close()
else:
    # keep last 200 lines
    line_num = lines - 200
    f = open(log_file, 'r')
    f_lines = f.readlines()
    f.close()

    line_counter = 1
    f = open(log_file, 'w')
    for line in f_lines:
        if line_counter > line_num:
            f.writelines(str(line))

        line_counter = line_counter + 1
    f.close()

    f = open(log_file, 'a')
    f.writelines('Mounzil, '
                 + current_time
                 + '\n')
    f.close()

from mounzil.scripts.data_base import mounzilDB, PluginsDB

# create an object for mounzilDB
mounzil_db = mounzilDB()

# create tables
mounzil_db.createTables()

# close connections
mounzil_db.closeConnections()

# create an object for PluginsDB
plugins_db = PluginsDB()

# create tables
plugins_db.createTables()

# delete old links
plugins_db.deleteOldLinks()

# close connections
plugins_db.closeConnections()


# import mounzil_setting
# mounzil is using QSettings for saving windows size and windows
# position and program settings.

mounzil_setting = QSettings('mounzil', 'mounzil')

mounzil_setting.beginGroup('settings')

default_setting_dict = returnDefaultSettings()
# this loop is checking values in mounzil_setting . if value is not
# valid then value replaced by default_setting_dict value
for key in default_setting_dict.keys():

    setting_value = mounzil_setting.value(key, default_setting_dict[key])
    mounzil_setting.setValue(key, setting_value)

# download files is downloading in temporary folder(download_path_temp) and then they will be moved to user download folder(download_path) after completion.
# Check that mount point is available of not!
if not(os.path.exists(mounzil_setting.value('download_path_temp'))):
    mounzil_setting.setValue('download_path_temp', default_setting_dict['download_path_temp'])

if not(os.path.exists(mounzil_setting.value('download_path'))):
    mounzil_setting.setValue('download_path', default_setting_dict['download_path'])


mounzil_setting.sync()

# this section  creates temporary download folder and download folder and
# download sub folders if they did not existed.
download_path_temp = mounzil_setting.value('download_path_temp')
download_path = mounzil_setting.value('download_path')


folder_list = [download_path_temp, download_path]

# add subfolders to folder_list if user checked subfolders check box in setting window.
if mounzil_setting.value('subfolder') == 'yes':
    for folder in ['Audios', 'Videos', 'Others', 'Documents', 'Compressed']:
        folder_list.append(os.path.join(download_path, folder))

# create folders in folder_list
for folder in folder_list:
    osCommands.makeDirs(folder)

mounzil_setting.endGroup()

# Browser integration for Firefox and chromium and google chrome
for browser in ['chrome', 'chromium', 'opera', 'vivaldi', 'firefox', 'brave']:
    json_done, native_done = browserIntegration(browser)

    log_message = browser

    if json_done == True:
        log_message = log_message + ': ' + 'Json file is created successfully.\n'

    else:
        log_message = log_message + ': ' + 'Json ERROR!\n'

    if native_done == True:
        log_message = log_message + 'mounzil executer file is created successfully.\n'

    elif native_done == False:
        log_message = log_message + ': ' + 'mounzil executer file ERROR!\n'

    logger.sendToLog(log_message)

# get locale and set ui direction
locale = str(mounzil_setting.value('settings/locale'))

# right to left languages
rtl_locale_list = ['fa_IR', 'ar']

# left to right languages
ltr_locale_list = ['en_US', 'zh_CN', 'fr_FR', 'pl_PL', 'nl_NL', 'pt_BR', 'es_ES', 'hu', 'tr', 'tr_TR']

if locale in rtl_locale_list:
    mounzil_setting.setValue('ui_direction', 'rtl')
else:
    mounzil_setting.setValue('ui_direction', 'ltr')

# compatibility
mounzil_version = float(mounzil_setting.value('version/version', 1.0))
if mounzil_version < 1.0:
    from mounzil.scripts.compatibility import compatibility
    try:
        compatibility()
    except Exception as e:

        # create an object for mounzilDB
        mounzil_db = mounzilDB()

        # create tables
        mounzil_db.resetDataBase()

        # close connections
        mounzil_db.closeConnections()

        # write error in log
        logger.sendToLog(
            "compatibility ERROR!", "ERROR")
        logger.sendToLog(
            str(e), "ERROR")

    mounzil_version = 2.6

if mounzil_version < 3.1:
    # create an object for mounzilDB
    mounzil_db = mounzilDB()

    # correct data base
    mounzil_db.correctDataBase()

    # close connections
    mounzil_db.closeConnections()

    mounzil_version = 3.1

if mounzil_version < 3.2:
    mounzil_setting.beginGroup('settings')

    for key in default_setting_dict.keys():

        setting_value = default_setting_dict[key]
        mounzil_setting.setValue(key, setting_value)

    mounzil_setting.endGroup()

    mounzil_setting.setValue('version/version', 3.2)

mounzil_setting.sync()

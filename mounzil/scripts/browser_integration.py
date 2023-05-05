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
#

from mounzil.scripts.useful_tools import determineConfigFolder
from mounzil.scripts import osCommands
from mounzil.constants import OS, BROWSER
import subprocess
import platform
import sys
import os

os_type = platform.system()

home_address = str(os.path.expanduser("~"))

# download manager config folder .
config_folder = determineConfigFolder()

# browser can be firefox or chromium or chrome


def browserIntegration(browser):
    # for GNU/Linux
    if os_type == OS.LINUX:
        # find mounzil execution path
        # mounzil execution path
        exec_path = os.path.join(config_folder, 'mounzil_run_shell')

        # Native Messaging Hosts folder path for every browser
        if browser == BROWSER.CHROMIUM:
            native_message_folder = home_address + '/.config/chromium/NativeMessagingHosts'

        elif browser == BROWSER.CHROME:
            native_message_folder = home_address + \
                '/.config/google-chrome/NativeMessagingHosts'

        elif browser == BROWSER.FIREFOX:
            native_message_folder = home_address + \
                '/.mozilla/native-messaging-hosts'

        elif browser == BROWSER.VIVALDI:
            native_message_folder = home_address + \
                '/.config/vivaldi/NativeMessagingHosts'

        elif browser == BROWSER.OPERA:
            native_message_folder = home_address + \
                '/.config/opera/NativeMessagingHosts'

        elif browser == BROWSER.BRAVE:
            native_message_folder = home_address + \
                '/.config/BraveSoftware/Brave-Browser/NativeMessagingHosts'

    # for FreeBSD and OpenBSD
    elif os_type in OS.BSD_FAMILY:
        # find mounzil execution path
        # mounzil execution path
        exec_path = os.path.join(config_folder, 'mounzil_run_shell')

        # Native Messaging Hosts folder path for every browser
        if browser == BROWSER.CHROMIUM:
            native_message_folder = home_address + '/.config/chromium/NativeMessagingHosts'

        elif browser == BROWSER.CHROME:
            native_message_folder = home_address + \
                '/.config/google-chrome/NativeMessagingHosts'

        elif browser == BROWSER.FIREFOX:
            native_message_folder = home_address + \
                '/.mozilla/native-messaging-hosts'
        elif browser == BROWSER.VIVALDI:
            native_message_folder = home_address + \
                '/.config/vivaldi/NativeMessagingHosts'

        elif browser == BROWSER.OPERA:
            native_message_folder = home_address + \
                '/.config/opera/NativeMessagingHosts'

        elif browser == BROWSER.BRAVE:
            native_message_folder = home_address + \
                '/.config/BraveSoftware/Brave-Browser/NativeMessagingHosts'


    # for Mac OSX
    elif os_type == OS.OSX:
        # find mounzil execution path
        # mounzil execution path
        exec_path = os.path.join(config_folder, 'mounzil_run_shell')

        # Native Messaging Hosts folder path for every browser
        if browser == BROWSER.CHROMIUM:
            native_message_folder = home_address + \
                '/Library/Application Support/Chromium/NativeMessagingHosts'

        elif browser == BROWSER.CHROME:
            native_message_folder = home_address + \
                '/Library/Application Support/Google/Chrome/NativeMessagingHosts'

        elif browser == BROWSER.FIREFOX:
            native_message_folder = home_address + \
                '/Library/Application Support/Mozilla/NativeMessagingHosts'

        elif browser == BROWSER.VIVALDI:
            native_message_folder = home_address + \
                '/Library/Application Support/Vivaldi/NativeMessagingHosts'

        elif browser == BROWSER.OPERA:
            native_message_folder = home_address + \
                '/Library/Application Support/Opera/NativeMessagingHosts/'

        elif browser == BROWSER.BRAVE:
            native_message_folder = home_address + \
                '/Library/Application Support/BraveSoftware/Brave-Browser/NativeMessagingHosts/'

    # for MicroSoft Windows os (windows 7 , ...)
    elif os_type == OS.WINDOWS:
        # finding mounzil execution path
        cwd = sys.argv[0]

        current_directory = os.path.dirname(cwd)

        exec_path = os.path.join(
            current_directory, 'mounzil.exe')

        # the execution path in json file for Windows must in form of
        # c:\\Users\\...\\mounzil Download Manager.exe , so we need 2
        # "\" in address
        exec_path = exec_path.replace('\\', r'\\')

        if browser in BROWSER.CHROME_FAMILY:
            native_message_folder = os.path.join(
                home_address, 'AppData\Local\mounzil', 'chrome')
        else:
            native_message_folder = os.path.join(
                home_address, 'AppData\Local\mounzil', 'firefox')

    # WebExtension native hosts file prototype
    webextension_json_connector = {
        "name": "com.mounzil.mdmchromewrapper",
        "type": "stdio",
        "path": str(exec_path),
        "description": "Integrate mounzil with %s using WebExtensions" % (browser)
    }

    # Add chrom* keys
    if browser in BROWSER.CHROME_FAMILY:
        webextension_json_connector["allowed_origins"] = ["chrome-extension://legimlagjjoghkoedakdjhocbeomojao/"]

    # Add firefox keys
    elif browser == BROWSER.FIREFOX:
        webextension_json_connector["allowed_extensions"] = [
            "com.mounzil.mdmchromewrapper@mounzil.github.io",
            "com.mounzil.mdmchromewrapper.offline@mounzil.github.io"
        ]

    # Build final path
    native_message_file = os.path.join(
        native_message_folder, 'com.mounzil.mdmchromewrapper.json')

    osCommands.makeDirs(native_message_folder)

    # Write NMH file
    f = open(native_message_file, 'w')
    f.write(str(webextension_json_connector).replace("'", "\""))
    f.close()

    if os_type != OS.WINDOWS:

        pipe_json = subprocess.Popen(['chmod', '+x', str(native_message_file)],
                                     stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE,
                                     shell=False)

        if pipe_json.wait() == 0:
            json_done = True
        else:
            json_done = False

    else:
        native_done = None
        import winreg
        # add the key to the windows registry
        if browser in BROWSER.CHROME_FAMILY:
            try:
                # create mdmchromewrapper key under NativeMessagingHosts
                winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                 "SOFTWARE\\Google\\Chrome\\NativeMessagingHosts\\com.mounzil.mdmchromewrapper")
                # open a connection to mdmchromewrapper key
                gintKey = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, "SOFTWARE\\Google\\Chrome\\NativeMessagingHosts\\com.mounzil.mdmchromewrapper", 0, winreg.KEY_ALL_ACCESS)
                # set native_message_file as key value
                winreg.SetValueEx(gintKey, '', 0, winreg.REG_SZ, native_message_file)
                # close connection to mdmchromewrapper
                winreg.CloseKey(gintKey)

                json_done = True

            except WindowsError:

                json_done = False

        elif browser == BROWSER.FIREFOX:
            try:
                # create mdmchromewrapper key under NativeMessagingHosts for firefox
                winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                 "SOFTWARE\\Mozilla\\NativeMessagingHosts\\com.mounzil.mdmchromewrapper")
                # open a connection to mdmchromewrapper key for firefox
                fintKey = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, "SOFTWARE\\Mozilla\\NativeMessagingHosts\\com.mounzil.mdmchromewrapper", 0, winreg.KEY_ALL_ACCESS)
                # set native_message_file as key value
                winreg.SetValueEx(fintKey, '', 0, winreg.REG_SZ, native_message_file)
                # close connection to mdmchromewrapper
                winreg.CloseKey(fintKey)

                json_done = True

            except WindowsError:

                json_done = False

    # create mounzil_run_shell file for gnu/linux and BSD and Mac
    # firefox and chromium and ... call mounzil with Native Messaging system.
    # json file calls mounzil_run_shell file.
    if os_type in (OS.UNIX_LIKE + [OS.OSX]):
        # find available shell
        shell_list = ['/bin/bash', '/usr/local/bin/bash', '/bin/sh', '/usr/local/bin/sh', '/bin/ksh', '/bin/tcsh']

        for shell in shell_list:
            if os.path.isfile(shell):
                # define shebang
                shebang = '#!' + shell
                break

        if os_type == OS.OSX:
            # finding mounzil execution path
            cwd = sys.argv[0]

            current_directory = os.path.dirname(cwd)

            mounzil_path = os.path.join(
                current_directory, 'mounzil')
        else:
            mounzil_path = 'mounzil'

        mounzil_run_shell_contents = shebang + '\n' + '"' + mounzil_path + '" "$@"'

        f = open(exec_path, 'w')
        f.writelines(mounzil_run_shell_contents)
        f.close()

        # make mounzil_run_shell executable

        pipe_native = subprocess.Popen(['chmod', '+x', exec_path],
                                       stderr=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stdin=subprocess.PIPE,
                                       shell=False)

        if pipe_native.wait() == 0:
            native_done = True
        else:
            native_done = False

    return json_done, native_done

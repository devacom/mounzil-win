# mounzil MicroSoft Windows package build
windows package build for [Mounzil](https://github.com/devacom/mounzil)

We build stable releases safely and you don't need to build it yourself. You can download Mounzil for  Microsoft Windows from [release page](https://github.com/devacom/mounzil/releases).
If you want to build mounzil for Windows yourself, then this instruction can help you.
# step 1: Preparing
- ## 1-1 clone or download [mounzil](https://github.com/devacom/mounzil)

You can download project form our github page or using git clients. I recommend [git for windows](https://git-scm.com/download/win)

You can download the stable version Source code from [release page](https://github.com/devacom/mounzil/releases) or last git version from the [master branch](https://github.com/devacom/mounzil/archive/master.zip).
After downloading or cloning, extract and enter mounzil path.
you can see this structure for directories now.

```
mounzil
├── man
├── mounzil
│   ├── gui
│   └── scripts
├── resources
│   ├── Breeze
│   ├── Breeze-Dark
│   ├── locales
│   ├── Papirus
│   ├── Papirus-Dark
│   └── Papirus-Light
├── test
└── xdg
```

You also need some file that we put them in this repository and we use them to build mounzil. so clone or download [this repository](https://github.com/devacom/mounzil-windows-package-build)

- ## 1-2 python
mounzil has been written in python so we need python3 to build it, after freezing and building the package there are no more need to python and its library.
Download latest [python3](https://www.python.org/downloads/windows/) and install it.

**remember** the **destination directory** and enable the **“Add Python 3.7 to PATH” option.**

- ## 1-3 dependencies & libraries
Install these libraries with `pip` from windows **cmd** or **powershell** (*you should run pip as Admin*)

`pip install pyqt5 requests pypiwin32 setproctitle psutil youtube_dl pyinstaller`

mounzil is gui for [**Aria2**](https://aria2.github.io) so we need it, you can download latest or specific version according to your system from [Aria2 release page](https://github.com/aria2/aria2/releases/) or use one of Aria2 build ithat I put in this repository at aria2 folder (*we will need it ahead*)
mounzil uses [ffmpeg](https://www.ffmpeg.org/) for mixing videos([more info.](https://github.com/devacom/mounzil/wiki/How-can-I-download-videos-from-youtube)). Download [ffmpeg](https://ffmpeg.zeranoe.com/builds/) yourself or use ffmpeg build in this repository.

- ## 1-4 windows SDK
Download and install the [Windows Software Development Kit (SDK)](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk) for Windows 10. we need it for Application Certification Kit API.

# step 2: test and run
Move **aria2c.exe and ffmpeg.exe** to the test folder next to the test.py according to your system architecture

Open power shell or Windows CMD or [git bash](https://git-scm.com/download/win) and Enter cloned mounzil directory with `cd` command. run mounzil as test with this command.  

`python test/test.py`

- now mounzil should run as a python script. If you get some error you may had mistake. Open  an issue [here](https://github.com/devacom/mounzil-windows-package-build/issues), We will help you :)

# step 3: build
There are 2 methods to build Mounzil

1. Auto:

The easy way to build is to run 'make.bat' from 'packagers\windows' folder.

2. Manual:
 
Place `version.py` and `mounzil.ico` in perseplois folder.

run Windows cmd or powershell (as Admin) and enter mounzil folder so build mounzil by pyinstaller with this command:

```
pyinstaller '.\mounzil\Mounzil.py'  -p "C:\Program Files (x86)\Windows Kits\10
\Redist\ucrt\DLLs\x64" -p C:\python35\Lib\site-packages\PyQt5\Qt\bin\ -w -F -i mounzil.ico -n "Mounzil
" --version-file version.py
```

If you changed **windows SDK** (step 1-4) and **python** (step 1-2) installation directory you should change `-p(path)`

`-w` means it is a windowed app, not a console one.

`-F` Create a one-file bundled executable.

`-i` perseplois icon.

`-n` name of bundled executable.

`--version-file` add mounzil version resource from `version.py` to the exe.

If everything goes well, you have some output like this

![pyinstaller](screen1.png)

 If you get error messages, you made mistake. Open  an issue [here](https://github.com/devacom/mounzil-windows-package-build/issues), We will help you :)

- After this, you have bundled executable file in dist folder, Move `ffmpeg.exe` and `aria2c.exe` next to the `Mounzil.exe`. you can run it and test it, it works perfectly

# step 4: create package installer
You have executable perseplois and you can put it everywhere (next to the and `ffmpeg.exe` and `aria2c.exe`) but we going to create a installer for windows.

- Download and install [Inno Setup](http://www.jrsoftware.org/isdl.php)
- you can create your installation or use our standard one, I put theme in this repository for both 32 and 64 architecture (`.iss files`). you should edit *`[Files]`* section and *LicenseFile, InfoAfterFile, OutputBaseFilename, SetupIconFile, UninstallDisplayIcon* according to your directory name, also I put license, mounzil readme, after installation text and icon in this repository.
- Build and compile installation if everything goes well, you have a mounzil installer.

 Enjoy it. :blush:

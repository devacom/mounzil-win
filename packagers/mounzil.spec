Name:           mounzil
Version:        1.0.0
Release:        1
License:        GPLv3
Source0: 	https://github.com/devacom/mounzil/archive/refs/tags/v%{version}.tar.gz

Summary:        A powerful internet download manager powered by aria2
BuildArch:      noarch
BuildRequires:  python310-devel
BuildRequires:  desktop-file-utils
BuildRequires:  python310-setuptools
BuildRequires:  libappstream-glib8
# libnotify is required for notify-send
Requires:       aria2 libnotify4 python310-qt5 python310-requests
Requires:       python3-setproctitle sound-theme-freedesktop python310-psutil
Requires:       pulseaudio-utils yt-dlp

%description
Mounzil is a download manager and a GUI for aria2 powered by Python.
 - Graphical UI front end for aria2
 - Multi-segment downloading
 - Scheduling downloads
 - Download queue



%prep
%autosetup -p1
chmod a-x xdg/*.desktop
rm 'mounzil/Mounzil.py'
find -type f -exec \
   sed -i '1s=^#!/usr/bin/\(python\|env python.*\)$=#!%{__python3}=' {} \;


%build
%{py3_build}


%install
%{py3_install}
chmod a+x %{buildroot}/%{python3_sitelib}/mounzil/__main__.py

%check
# No valid tests available
#%{__python3} setup.py test
desktop-file-validate %{buildroot}/%{_datadir}/applications/*mounzil.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml


%files
%license LICENSE
%doc README.md

%{_bindir}/%{name}
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/pixmaps/*
%{_mandir}/man1/%{name}.1*
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info
%{_datadir}/metainfo/com.github.devacom.mounzil.appdata.xml

%changelog
* Sat Apr 29 2023 devacom - 1.0.0
- initialize yt-dlp support
- Tweak Settings menu and the program design

* Fri Apr 14 2023 devacom - 1.0.0-1
- Initial pre-release

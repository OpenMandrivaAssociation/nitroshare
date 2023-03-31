%define urlver %(echo %{version}|cut -d. -f1,2)

Summary:	A simple tool for sending files to other machines on a local network
Name:		nitroshare
Version:	0.3.4
Release:	3
License:	MIT
Group:		Networking/File transfer
Url:		https://nitroshare.net
# https://github.com/nitroshare/nitroshare-desktop
Source0:	https://launchpad.net/nitroshare/%{urlver}/%{version}/+download/%{name}-%{version}.tar.gz
# Patch to fix build with new Qt5.11 (QStyle error). https://github.com/nitroshare/nitroshare-desktop/issues/213 (penguin)
Patch0: fix-build-with-qt5.11.patch
BuildRequires:	cmake
BuildRequires: cmake(Qt5Core)
BuildRequires:	qt5-macros
BuildRequires:	qt5-linguist-tools
BuildRequires: qt5-qtbase-devel
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5DBus)
# extra BRs needed for Mate, Gnome and Cinnamon DEs
#BuildRequires:	pkgconfig(appindicator-0.1)
BuildRequires: pkgconfig(appindicator3-0.1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libnotify)

%description
A cross-platform network file transfer application designed to make
transferring any file to any device as painless as possible.

Features:
  * Automatic discovery of devices on the local network.
  * Simple and intuitive user interface.
  * Transfer entire directories.

%files
%doc README.md
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/kservices5/nitroshare_addtoservicemenu.desktop
%{_iconsdir}/hicolor/*/*/%{name}*.svg
%{_iconsdir}/breeze*/*/*/%{name}*.svg
%{_mandir}/man1/%{name}.1*
%{_iconsdir}/gnome/24x24/apps/nitroshare-indicator.png
%{_iconsdir}/ubuntu-mono-dark/apps/22/nitroshare-indicator.png
%{_iconsdir}/ubuntu-mono-dark/apps/24/nitroshare-indicator.svg
%{_iconsdir}/ubuntu-mono-light/apps/22/nitroshare-indicator.png
%{_iconsdir}/ubuntu-mono-light/apps/24/nitroshare-indicator.svg

#----------------------------------------------------

%package nautilus
Summary:	Nautilus extension for Nitroshare
Group:		Graphical desktop/GNOME
Requires:	%{name} = %{EVRD}
Requires:	nautilus-python
BuildArch:	noarch

%description nautilus
The %{name}-nautilus package contains the %{name} extension for the
nautilus file manager.

%files nautilus
%doc README.md
%{_datadir}/nautilus-python/extensions/*

#----------------------------------------------------

%package caja
Summary:	Caja extension for Nitroshare
Group:		Graphical desktop/MATE
Requires:	%{name} = %{EVRD}
# Change from requires to recommends due to missing re/build package for cooker contib.
Recommends:	python-caja
BuildArch:	noarch

%description caja
The %{name}-caja package contains the %{name} extension for the
caja file manager.

%files caja
%doc README.md
%{_datadir}/caja-python/extensions/*

#----------------------------------------------------

%prep
%setup -q
%autopatch -p1

%build
%cmake_qt5

%make

# Caja is GTK2 so fix version of typelib(Gtk;Caja)
sed -i -e "s|'3.0'|'2.0'|g" src/dist/nitroshare_caja.py

%install
%makeinstall_std -C build

rm -rf %{buildroot}%{_datadir}/nemo-python/extensions/*.py*

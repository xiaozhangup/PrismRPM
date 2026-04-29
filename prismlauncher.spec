%bcond_with toolchain_clang
%bcond_with toolchain_gcc

%if %{with toolchain_gcc}
%global toolchain gcc
%else
%global toolchain clang
%endif

# Change these variables if you want to use custom keys
# Leave blank if you want to build Prism Launcher without an MSA ID or CurseForge API key
%global msa_id default
%global curseforge_key default

# Set the Qt version
%global qt_version 6
%global min_qt_version 6.4

# Give the launcher our build platform
%global build_platform unknown

%if 0%{?fedora}
%global build_platform Fedora
%endif

%if 0%{?rhel}
%global build_platform RedHat
%endif

%if 0%{?centos}
%global build_platform CentOS
%endif

Name:             prismlauncher
Version:          11.0.2
Release:          %autorelease
# See COPYING.md for more information
# Each file in the source tree also contains a SPDX-License-Identifier header
License:          GPL-3.0-only AND Apache-2.0 AND LGPL-3.0-only AND LGPL-2.1 AND OFL-1.1 AND MIT
Group:            Amusements/Games
Summary:          Minecraft launcher with ability to manage multiple instances
Source:           https://github.com/PrismLauncher/PrismLauncher/releases/download/%{version}/PrismLauncher-%{version}.tar.gz
URL:              https://prismlauncher.org/

%if "%{toolchain}" == "gcc"
BuildRequires:    gcc-c++
%endif
%if "%{toolchain}" == "clang"
BuildRequires:    clang
BuildRequires:    lld
%endif

# JDKs less than the most recent release & LTS are no longer in the default
# Fedora repositories
# Make sure you have Adoptium's repositories enabled
# https://fedoraproject.org/wiki/Changes/ThirdPartyLegacyJdks
# https://adoptium.net/installation/linux/#_centosrhelfedora_instructions
BuildRequires:    temurin-17-jdk
BuildRequires:    libappstream-glib

BuildRequires:    cmake >= 3.22
BuildRequires:    ninja-build
BuildRequires:    extra-cmake-modules

BuildRequires:    cmake(VulkanHeaders)
BuildRequires:    pkgconfig(gamemode)
BuildRequires:    pkgconfig(libarchive)
BuildRequires:    pkgconfig(libcmark)
BuildRequires:    pkgconfig(libqrencode)
BuildRequires:    pkgconfig(scdoc)
BuildRequires:    pkgconfig(tomlplusplus)
BuildRequires:    pkgconfig(zlib)

BuildRequires:    cmake(Qt%{qt_version}Concurrent) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}Core) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}CoreTools) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}Network) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}NetworkAuth) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}OpenGL) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}Test) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}Widgets) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}Xml) >= %{min_qt_version}

BuildRequires:    desktop-file-utils
BuildRequires:    libappstream-glib

Requires:         qt%{qt_version}-qtimageformats
Requires:         qt%{qt_version}-qtsvg

Requires:         javapackages-filesystem
Recommends:       java-25-openjdk
Recommends:       java-21-openjdk

# Used to gather GPU with `lspci`
Requires:         pciutils
# Needed for LWJGL [2.9.2, 3) https://github.com/LWJGL/lwjgl/issues/128
Recommends:       xrandr
# Needed for using narrator in minecraft
Recommends:       flite
# The launcher supports enabling gamemode
Suggests:         gamemode

%description
A custom launcher for Minecraft that allows you to easily manage
multiple installations of Minecraft at once (Fork of MultiMC)


%prep
%autosetup -n PrismLauncher-%{version}

%build
%cmake \
  -G Ninja \
  %if "%{toolchain}" == "clang"
  -D CMAKE_LINKER_TYPE=LLD \
  %endif
  -DLauncher_QT_VERSION_MAJOR="%{qt_version}" \
  -DLauncher_BUILD_PLATFORM="%{build_platform}" \
  %if 0%{?fedora} > 41
  -DLauncher_ENABLE_JAVA_DOWNLOADER=ON \
  %endif
  %if "%{msa_id}" != "default"
  -DLauncher_MSA_CLIENT_ID="%{msa_id}" \
  %endif
  %if "%{curseforge_key}" != "default"
  -DLauncher_CURSEFORGE_API_KEY="%{curseforge_key}" \
  %endif

%cmake_build


%install
%cmake_install


%check
%ctest

desktop-file-validate %{buildroot}/%{_datadir}/applications/org.prismlauncher.PrismLauncher.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/org.prismlauncher.PrismLauncher.metainfo.xml

%files
%doc README.md
%license LICENSE COPYING.md
%dir %{_datadir}/PrismLauncher
%{_bindir}/prismlauncher
%{_datadir}/PrismLauncher/*
%{_datadir}/applications/org.prismlauncher.PrismLauncher.desktop
%{_datadir}/mime/packages/org.prismlauncher.PrismLauncher.xml
%{_datadir}/icons/hicolor/*/apps/org.prismlauncher.PrismLauncher.*
%{_datadir}/qlogging-categories?/prismlauncher.categories
%{_mandir}/man?/prismlauncher.*
%{_metainfodir}/org.prismlauncher.PrismLauncher.metainfo.xml


%changelog
%autochangelog

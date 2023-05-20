%global kf5_version 5.106.0
%global framework sonnet

Name: opt-kf5-sonnet
Version: 5.106.0
Release: 1%{?dist}
Summary: KDE Frameworks 5 Tier 1 solution for spell checking

License: LGPLv2+
URL:     https://invent.kde.org/frameworks/sonnet
Source0: %{name}-%{version}.tar.bz2

# filter plugin provides
%global __provides_exclude_from ^(%{_opt_qt5_plugindir}/.*\\.so)$

BuildRequires: aspell-devel
#BuildRequires: hspell-devel
#BuildRequires: libvoikko-devel
BuildRequires: opt-extra-cmake-modules >= %{kf5_version}
BuildRequires: hunspell-devel
BuildRequires: opt-kf5-rpm-macros >= %{kf5_version}
BuildRequires: opt-qt5-qtbase-devel
BuildRequires: opt-qt5-qtdeclarative-devel
BuildRequires: opt-qt5-qttools-devel
BuildRequires: zlib-devel
BuildRequires: make

Requires:       %{name}-core%{?_isa} = %{version}-%{release}
Requires:       %{name}-ui%{?_isa} = %{version}-%{release}

%description
KDE Frameworks 5 Tier 1 solution for spell checking.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        core
Summary:        Non-gui part of the Sonnet framework
%{?opt_kf5_default_filter}
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
Requires: opt-qt5-qtbase-gui
Requires: opt-qt5-qtdeclarative

%description    core
Non-gui part of the Sonnet framework provides low-level spell checking tools

%package        ui
Summary:        GUI part of the Sonnet framework
%{?opt_kf5_default_filter}
Requires:       %{name}-core%{?_isa} = %{version}-%{release}

%description    ui
GUI part of the Sonnet framework provides widgets with spell checking support.


%prep
%autosetup -n %{name}-%{version}/upstream -p1

%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

mkdir -p build
pushd build

%_opt_cmake_kf5 ../

%make_build

popd

%install
pushd build
make DESTDIR=%{buildroot} install
popd

%find_lang_kf5 sonnet5_qt


%check
export CTEST_OUTPUT_ON_FAILURE=1
make test ARGS="--output-on-failure --timeout 300" -C %{_target_platform} ||:


%files
%doc README.md
%license LICENSES/*.txt

%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig

%files core
%{_opt_kf5_datadir}/qlogging-categories5/*categories
%{_opt_kf5_libdir}/libKF5SonnetCore.so.*
%dir %{_opt_qt5_plugindir}/kf5/sonnet/
%{_opt_qt5_plugindir}/kf5/sonnet/sonnet_hunspell.so
%{_opt_kf5_bindir}/parsetrigrams
%{_opt_kf5_bindir}/gentrigrams
%{_opt_kf5_qmldir}/org/kde/sonnet/
%{_opt_qt5_plugindir}/kf5/sonnet/sonnet_aspell.so
#{_opt_qt5_plugindir}/kf5/sonnet/sonnet_hspell.so
#{_opt_qt5_plugindir}/kf5/sonnet/sonnet_voikko.so

%post ui -p /sbin/ldconfig
%postun ui -p /sbin/ldconfig

%files ui
%{_opt_kf5_libdir}/libKF5SonnetUi.so.*
%{_opt_kf5_qtplugindir}/designer/*5widgets.so
%{_opt_kf5_datadir}/locale/

%files devel
%{_opt_kf5_includedir}/KF5/Sonnet/
%{_opt_kf5_includedir}/KF5/SonnetCore/
%{_opt_kf5_includedir}/KF5/SonnetUi/
%{_opt_kf5_libdir}/libKF5SonnetCore.so
%{_opt_kf5_libdir}/libKF5SonnetUi.so
%{_opt_kf5_libdir}/cmake/KF5Sonnet/
%{_opt_kf5_archdatadir}/mkspecs/modules/qt_SonnetCore.pri
%{_opt_kf5_archdatadir}/mkspecs/modules/qt_SonnetUi.pri

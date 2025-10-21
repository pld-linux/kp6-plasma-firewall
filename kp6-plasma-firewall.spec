#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.5.0
%define		qtver		5.15.2
%define		kpname		plasma-firewall
%define		kf6ver		5.39.0

Summary:	plasma-firewall
Name:		kp6-%{kpname}
Version:	6.5.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	89ff9da83145b67c0415e8029583c343
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= 5.15.0
BuildRequires:	Qt6DBus-devel >= 5.15.0
BuildRequires:	Qt6Gui-devel >= 5.15.0
BuildRequires:	Qt6Network-devel >= 5.15.2
BuildRequires:	Qt6Qml-devel
BuildRequires:	Qt6Quick-devel >= 5.15.0
BuildRequires:	Qt6Xml-devel >= 5.15.0
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules
BuildRequires:	kf6-kauth-devel >= 5.82
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kconfig-devel >= 5.82
BuildRequires:	kf6-kcoreaddons-devel >= 5.85.0
BuildRequires:	kf6-kdeclarative-devel >= 5.82
BuildRequires:	kf6-ki18n-devel >= 5.82
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Requires:	python3
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Plasma 6 Firewall KCM.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%{_libdir}/libkcm_firewall_core.so
%dir %{_libdir}/qt6/plugins/kf6/plasma_firewall
%{_libdir}/qt6/plugins/kf6/plasma_firewall/firewalldbackend.so
%{_libdir}/qt6/plugins/kf6/plasma_firewall/ufwbackend.so
%attr(755,root,root) %{_prefix}/libexec/kde_ufw_plugin_helper.py
%{_datadir}/dbus-1/system-services/org.kde.ufw.service
%{_datadir}/dbus-1/system.d/org.kde.ufw.conf
%dir %{_datadir}/kcm_ufw
%{_datadir}/kcm_ufw/defaults
%{_datadir}/metainfo/org.kde.plasma.firewall.metainfo.xml
%{_datadir}/polkit-1/actions/org.kde.ufw.policy
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_firewall.so
%{_desktopdir}/kcm_firewall.desktop
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/kde_ufw_plugin_helper

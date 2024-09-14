#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_with	qt5		# build with qt5 version
%bcond_without	qt6		# build without qt6 version
Summary:	Tool for annotating images
Name:		kImageAnnotator
Version:	0.7.1
Release:	1
License:	LGPL 3.0
Group:		X11/Libraries
Source0:	https://github.com/ksnip/kImageAnnotator/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	68990dfe7fe03f1aff5e0e5338b9f3bb
URL:		https://github.com/ksnip/kImageAnnotator/
BuildRequires:	cmake >= 3.20
%{?with_qt5:BuildRequires:	kColorPicker-qt5-devel >= 0.3.1}
%{?with_qt6:BuildRequires:	kColorPicker-qt6-devel >= 0.3.1}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tool for annotating images.

%package qt5
Summary:	Tool for annotating images
Obsoletes:	%{name} < 0.7.1
Conflicts:	%{name}-qt6

%description qt5
Tool for annotating images. Qt5 version.

%package qt5-devel
Summary:	Header files for %{name}-qt5 development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}-qt5
Group:		X11/Development/Libraries
Requires:	%{name}-qt5 = %{version}-%{release}
Requires:	cmake >= 3.20

%description qt5-devel
Header files for %{name}-qt5 development.

%description qt5-devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}-qt5.

%package qt6
Summary:	Tool for annotating images
Conflicts:	%{name}-qt5

%description qt6
Tool for annotating images. Qt6 version.

%package qt6-devel
Summary:	Header files for %{name}-qt6 development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}-qt6
Group:		X11/Development/Libraries
Requires:	%{name}-qt6 = %{version}-%{release}
Requires:	cmake >= 3.20

%description qt6-devel
Header files for %{name}-qt6 development.

%description qt6-devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}-qt6.

%prep
%setup -q

%build
%if %{with qt5}
%cmake -B build-qt5 \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DCMAKE_INSTALL_DATAROOTDIR="share"

%ninja_build -C build-qt5

%if %{with tests}
ctest --test-dir build-qt5
%endif
%endif

%if %{with qt6}
%cmake -B build-qt6 \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DBUILD_WITH_QT6=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DCMAKE_INSTALL_DATAROOTDIR="share"

%ninja_build -C build-qt6

%if %{with tests}
ctest --test-dir build-qt6
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{?with_qt5:%ninja_install -C build-qt5}
%{?with_qt6:%ninja_install -C build-qt6}

%find_lang %{name} --all-name --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	qt5 -p /sbin/ldconfig
%postun	qt5 -p /sbin/ldconfig

%post	qt6 -p /sbin/ldconfig
%postun	qt6 -p /sbin/ldconfig

%if %{with qt5}
%files qt5 -f %{name}.lang
%defattr(644,root,root,755)
%ghost %{_libdir}/libkImageAnnotator.so.0
%attr(755,root,root) %{_libdir}/libkImageAnnotator.so.*.*

%files qt5-devel
%defattr(644,root,root,755)
%{_includedir}/kImageAnnotator-Qt5
%{_libdir}/cmake/kImageAnnotator-Qt5
%{_libdir}/libkImageAnnotator.so
%endif

%if %{with qt6}
%files qt6 -f %{name}.lang
%defattr(644,root,root,755)
%ghost %{_libdir}/libkImageAnnotator.so.0
%attr(755,root,root) %{_libdir}/libkImageAnnotator.so.*.*

%files qt6-devel
%defattr(644,root,root,755)
%{_includedir}/kImageAnnotator-Qt6
%{_libdir}/cmake/kImageAnnotator-Qt6
%{_libdir}/libkImageAnnotator.so
%endif

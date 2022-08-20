#
# Conditional build:
%bcond_with	tests		# build with tests
Summary:	Tool for annotating images
Name:		kImageAnnotator
Version:	0.6.0
Release:	2
License:	LGPL 3.0
Group:		X11/Libraries
Source0:	https://github.com/ksnip/kImageAnnotator/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	129cf1fa60991091da91ef18cc587b65
URL:		https://github.com/ksnip/kImageAnnotator/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kColorPicker-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tool for annotating images.

%package devel
Summary:	Header files for %{name} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cmake >= 3.16

%description devel
Header files for %{name} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DCMAKE_INSTALL_DATAROOTDIR="share" \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{name} --all-name --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkImageAnnotator.so.*.*.*
%ghost %{_libdir}/libkImageAnnotator.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libkImageAnnotator.so
%{_includedir}/kImageAnnotator
%{_libdir}/cmake/kImageAnnotator

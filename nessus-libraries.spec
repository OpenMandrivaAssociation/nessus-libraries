%define major 2
%define libname %mklibname nessus %{major}
%define libnamedev %mklibname nessus -d

Summary:	Libraries needed by the Nessus security scanner
Name:		nessus-libraries
Version:	2.2.10
Release:	%mkrel 1
License:	GPL
Group:		System/Libraries
URL:		http://www.nessus.org
# http://cgi.tenablesecurity.com/nessus3dl.php?file=nessus-libraries-2.2.10.tar.gz&licence_accept=yes&t=5a144975306462c6d49d299ba1d6c0b2
Source0:	%{name}-%{version}.tar.gz
Patch0:		nessus-libraries-2.2.7-nessus-config.diff
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	openssl-devel

%description
Nessus 2.2 is a free, up-to-date, and full featured remote security scanner for
Linux. It is multithreaded, plugin-based, has a nice GTK interface, and
currently performs 410 remote security checks. It has powerful reporting
capabilities (HTML, LaTeX, ASCII text) and not only points out problems,
but suggests a solution for each of them.

This package provides libraries needed by nessus.

%package -n	%{libname}
Summary:	Libraries needed by nessus
Group:		System/Libraries

%description -n	%{libname}
Libraries needed by nessus

%package -n	%{libnamedev}
Summary:	Development libraries and headers for Nessus
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	libnessus-devel = %{version}
Provides:	nessus-libraries-devel = %{version}
Obsoletes:	%{mklibname nessus 2 -d}

%description -n %{libnamedev}
Development libraries and headers for Nessus.

%prep

%setup -q -n %{name}
%patch0 -p0

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

%build
%define __libtoolize /bin/true


CFLAGS="%{optflags}" ac_cv_prog_cc_g=no ac_cv_prog_cxx_g=no \
%configure --prefix=%{_prefix} --enable-cipher --enable-zlib

perl -pi -e 's/-o root / /g; s/-o \$\(installuser\) / /g; y/{}/()/' Makefile
%make

%install
if [ -d %{buildroot} ]; then rm -rf %{buildroot}; fi

%makeinstall

# remove unwanted files
rm -rf %{buildroot}%{_sbindir}/uninstall-nessus
rm -rf %{buildroot}%{_datadir}/doc

# workaround
install -d %{buildroot}/usr/lib/debug

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
if [ -d %{buildroot} ]; then rm -rf %{buildroot}; fi

%files -n %{libname}
%defattr(0644,root,root,755)
%attr(0755,root,root) %{_libdir}/*.so.*
%exclude /usr/lib/debug

%files -n %{libnamedev}
%defattr(0644,root,root,755)
%dir %{_includedir}/nessus
%{_includedir}/nessus/*
%attr(0755,root,root) %{_libdir}/*.so
%{_libdir}/*.*a
%attr(0755,root,root) %{_bindir}/nessus-config
%{_mandir}/man1/*
%exclude /usr/lib/debug

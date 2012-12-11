%define major 2
%define libname %mklibname nessus %{major}
%define libnamedev %mklibname nessus -d

Summary:	Libraries needed by the Nessus security scanner
Name:		nessus-libraries
Version:	2.2.10
Release:	%mkrel 7
License:	GPL
Group:		System/Libraries
URL:		http://www.nessus.org
# http://cgi.tenablesecurity.com/nessus3dl.php?file=nessus-libraries-2.2.10.tar.gz&licence_accept=yes&t=5a144975306462c6d49d299ba1d6c0b2
Source0:	%{name}-%{version}.tar.gz
Patch0:		nessus-libraries-2.2.7-nessus-config.diff
Patch1:		nessus-libraries-2.2.10-link.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	openssl-devel
BuildRequires:	%libnamedev
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch1 -p0

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

%build
CFLAGS="%{optflags}" ac_cv_prog_cc_g=no ac_cv_prog_cxx_g=no \
%configure2_5x --prefix=%{_prefix} --enable-cipher --enable-zlib

perl -pi -e 's/-o root / /g; s/-o \$\(installuser\) / /g; y/{}/()/' Makefile
%make LDFLAGS="%ldflags"

%install
if [ -d %{buildroot} ]; then rm -rf %{buildroot}; fi

%makeinstall_std

# remove unwanted files
rm -rf %{buildroot}%{_sbindir}/uninstall-nessus
rm -rf %{buildroot}%{_datadir}/doc

# workaround
install -d %{buildroot}/usr/lib/debug

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

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


%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.10-7mdv2011.0
+ Revision: 613009
- the mass rebuild of 2010.1 packages

* Sun Apr 18 2010 Funda Wang <fwang@mandriva.org> 2.2.10-6mdv2010.1
+ Revision: 536333
- add nessus-devel for wrongly written makefiles

* Fri Apr 16 2010 Funda Wang <fwang@mandriva.org> 2.2.10-5mdv2010.1
+ Revision: 535301
- fix linkage

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 2.2.10-4mdv2010.0
+ Revision: 430163
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 2.2.10-3mdv2009.0
+ Revision: 253732
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 2.2.10-1mdv2008.1
+ Revision: 140994
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Sep 07 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.10-1mdv2008.0
+ Revision: 81672
- Import nessus-libraries



* Fri Sep 07 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.10-1mdv2008.0
- 2.2.10

* Mon Jun 19 2006 Lenny Cartier <lenny@mandriva.com> 2.2.8-1mdv2006.0
- 2.2.8

* Thu Mar 30 2006 Stew Benedict <sbenedict@mandriva.com> 2.2.7-6mdk
- don't provide nessus-devel - there is a real package with that name

* Thu Mar 16 2006 Marcel Pol <mpol@mandriva.org> 2.2.7-5mdk
- also provide nessus-devel

* Mon Mar 13 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.7-4mdk
- fix debug package

* Thu Mar 09 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.7-3mdk
- fix debug package

* Thu Mar 09 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.7-2mdk
- disable libtoolize

* Thu Mar 09 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.7-1mdk
- 2.2.7
- added P0 to fix the nessus-config script
- lib64 fixes

* Fri Jan 13 2006 Marcel Pol <mpol@mandriva.org> 2.2.6-1mdk
- 2.2.6

* Thu Mar 24 2005 Lenny Cartier <lenny@mandrakesoft.com> 2.2.4-1mdk
- 2.2.4

* Fri Feb 11 2005 Lenny Cartier <lenny@mandrakesoft.com> 2.2.3-1mdk
- 2.2.3

* Fri Jan  7 2005 Stefan van der Eijk <stefan@mandrake.org> 2.2.2a-1mdk
- New release 2.2.2a

* Wed Aug 18 2004 Michael Scherer <misc@mandrake.org> 2.0.12-1mdk 
- 2.0.12
- rpmbuildupdate aware

* Sat Feb 21 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.10a-1mdk
- Release: 2.0.10a.

* Thu Nov 06 2003 Lenny Cartier <lenny@mandrakesoft.com> 2.0.9-1mdk
- 2.0.9

* Fri Sep 05 2003 Laurent Culioli <laurent]pschit.net> 2.0.7-4mdk
- fix obsoletes/provides
- clean specfile

* Sun Aug 31 2003 Marcel Pol <mpol@gmx.net> 2.0.7-3mdk
- rebuild

* Tue Jul 22 2003 Marcel Pol <mpol@gmx.net> 2.0.7-2mdk
- use correct date of upload

* Tue Jun 17 2003 Marcel Pol <mpol@gmx.net> 2.0.7-1mdk
- 2.0.7
- split from nessus package to seperate library package
- remove perl commands to fix nessus-config (not necessary)

* Wed Dec 18 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.2.7-1mdk
- 1.2.7

* Tue Oct  8 2002 Stefan van der Eijk <stefan@eijk.nu> 1.2.6-1mdk
- 1.2.6
- removed README_LINUX (doesn't exist anymore)

* Wed Sep 11 2002 Arnaud Desmons <adesmons@mandrakesoft.com> 1.2.5-3mdk
- Requires nessus-plugins

* Wed Sep 11 2002 Arnaud Desmons <adesmons@mandrakesoft.com> 1.2.5-2mdk
- 1.2.5

* Tue Sep 10 2002 Arnaud Desmons <adesmons@mandrakesoft.com> 1.2.5-1mdk
- 1.2.5

* Thu Jul 25 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.2.3-1mdk
- 1.2.3

* Tue Jun 18 2002 Stefan van der Eijk <stefan@eijk.nu> 1.2.0-2mdk
- BuildRequires

* Fri Apr 19 2002  Lenny Cartier <lenny@mandrakesoft.com> 1.2.0-1mdk
- 1.2.0

* Thu Feb 28 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.1.13-1mdk
- 1.1.13
- xpm2png

* Tue Jan 22 2002 Laurent Culioli <laurent@mandrakesoft.com> 1.1.11-1mdk
- 1.1.11

* Sat Jan 19 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.1.9-3mdk
- rebuild

* Thu Nov 22 2001 Alexander Skwar <ASkwar@Linux-Mandrake.com> 1.1.9-2mdk
- Make rpmlint a little happier

* Wed Nov 21 2001 Alexander Skwar <ASkwar@Linux-Mandrake.com> 1.1.9-1mdk
- 1.1.9
- Actually really set localstatedir to /var/lib instead of to /var/log

* Thu Nov  8 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.1.8-1mdk
- 1.1.8
- call nessus-mkcert at install if certs do not exist
- patch nessus-mkcert to use more sensible locations to store certs/keys (P1)
- make localstatedir /var/lib and not /var/log (???) so that user accounts
  and info go into /var/lib/users and not /var/log/users

* Wed Nov  7 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.1.6-2mdk
- don't use sub shell in %%build
- use %%make
- use service macros
- added the missing nessus-mkcert, nessus-rmuser and nessus-update-plugins
- add a dependency on tar, gzip and lynx for nessus-update-plugins

* Wed Oct 17 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.1.6-1mdk
- 1.1.6

* Mon Sep 17 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.1.4-1mdk
- added by Oden Eriksson <oden.eriksson@kvikkjokk.net> :
	- updated to 1.1.4

* Tue Aug 21 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.0.9-1mdk
- updated to 1.0.9

* Wed Jun  6 2001 Laurent Culioli <laurent@mandrakesoft.com> 1.0.8-1mdk
- updated to 1.0.8

* Wed Mar 07 2001  Lenny Cartier <lenny@mandrakesoft.com> 1.0.7a-1mdk
- upgraded to 1.0.7a

* Tue Jan 30 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.0.7-1mdk
- used srpm from Guillaume Rousse <g.rousse@mandrake-linux.com> :
	- updated to 1.0.7

* Mon Nov 06 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.0.5-1mdk
- used srpm from Alexander Skwar <ASkwar@Linux-Mandrake.com> :
	New version
	Added menu for the client with icons
	Quiet the unpacking of the files

* Wed Jul 26 2000 John Johnson <jjohnson@linux-mandrake.com> 1.0.3-1mdk
- Fixed an error in my spec file that caused the nessusd script in
  /etc/rc.d/init.d to not work properly.

* Wed Jul 12 2000 John Johnsin <jjohnson@linux-mandrake.com> 1.0.3-1mdk
- Updated rpm for version 1.0.3 
- made a few small changes to spec file

* Sat Jun 10 2000 John Johnson <jjohnson@linux-mandrake.com> 1.0.1-1mdk
- updated sources to the new version.

* Mon May 29 2000 Vincent Danen <vdanen@linux-mandrake.com> 1.0.0-2mdk
- bzip sources
- fix group
- various specfile cleanups
- made unrelocatable
- added call to ldconfig in post and postun

* Thu May 18 2000 John Johnson <jjohnson@linux-mandrake.com>
- Made Mandrake rpm

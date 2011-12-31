%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define git_commit 8dc01d7b658dc04c5c500640854c6dba547a3118
%define git_commit_date 20090125


Name:		b43-tools
Version:	0
Release:	0.4.git%{git_commit_date}.1%{?dist}
Summary:	Tools for the Broadcom 43xx series WLAN chip
Group:		System Environment/Base
# assembler — GPLv2
# debug — GPLv3
# disassembler — GPLv2
# ssb_sprom — GPLv2+
License:	GPLv2 and GPLv2+ and GPLv3
URL:		http://bu3sch.de/gitweb?p=b43-tools.git;a=summary
# git clone http://git.bu3sch.de/git/b43-tools.git
# cd b43-tools
# git-archive --format=tar --prefix=%{name}-%{version}/ %{git_commit} | bzip2 > ../%{name}-%{version}.git%{git_commit_date}.tar.bz2
Source0:	%{name}-%{version}.git%{git_commit}.tar.bz2
Patch0:		b43-tools--use_optflags_in_ssb_sprom.diff
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	python-devel


%description
Tools for the Broadcom 43xx series WLAN chip.


%prep
%setup -q
install -p -m 0644 assembler/COPYING COPYING.assembler
install -p -m 0644 assembler/README README.assembler
install -p -m 0644 debug/COPYING COPYING.debug
install -p -m 0644 debug/README README.debug
install -p -m 0644 disassembler/COPYING COPYING.disassembler
install -p -m 0644 ssb_sprom/README README.ssb_sprom
install -p -m 0644 ssb_sprom/COPYING COPYING.ssb_sprom
%patch0 -p0 -b .optflags

%build
CFLAGS="%{optflags}" make %{?_smp_mflags} -C assembler
CFLAGS="%{optflags}" make %{?_smp_mflags} -C disassembler
CFLAGS="%{optflags}" make %{?_smp_mflags} -C ssb_sprom
cd debug && python install.py build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 assembler/b43-asm $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 assembler/b43-asm.bin $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 disassembler/b43-dasm $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 disassembler/b43-ivaldump $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 ssb_sprom/ssb-sprom $RPM_BUILD_ROOT%{_bindir}
cd debug && python install.py install --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.* COPYING.*
%{_bindir}/b43-asm
%{_bindir}/b43-asm.bin
%{_bindir}/b43-beautifier
%{_bindir}/b43-dasm
%{_bindir}/b43-fwdump
%{_bindir}/b43-ivaldump
%{_bindir}/ssb-sprom
%{python_sitelib}/*


%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0-0.4.git20090125.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.4.git20090125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 19 2009 Peter Lemenkov <lemenkov@gmail.com> 0-0.3.git20090125
- Corrected 'License' field
- Since now ssb_sprom honours optflags

* Sat Apr  4 2009 Peter Lemenkov <lemenkov@gmail.com> 0-0.2.git20090125
- Added missing BuildRequire

* Sat Mar 14 2009 Peter Lemenkov <lemenkov@gmail.com> 0-0.1.git20090125
- Initial package for Fedora


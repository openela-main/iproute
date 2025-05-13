## START: Set by rpmautospec
## (rpmautospec version 0.6.5)
## RPMAUTOSPEC: autorelease
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

Summary:            Advanced IP routing and network device configuration tools
Name:               iproute
Version:            6.11.0
Release:            %autorelease
URL:                https://kernel.org/pub/linux/utils/net/%{name}2/
Source0:            https://kernel.org/pub/linux/utils/net/%{name}2/%{name}2-%{version}.tar.xz
Source1:            rt_dsfield.deprecated

License:            GPL-2.0-or-later AND NIST-PD
BuildRequires:      bison
BuildRequires:      elfutils-libelf-devel
BuildRequires:      flex
BuildRequires:      gcc
BuildRequires:      iptables-devel >= 1.4.5
BuildRequires:      libbpf-devel
BuildRequires:      libcap-devel
BuildRequires:      libmnl-devel
BuildRequires:      libselinux-devel
BuildRequires:      make
BuildRequires:      pkgconfig
%if ! 0%{?_module_build}
%if 0%{?fedora}
BuildRequires:      linux-atm-libs-devel
%endif
%endif
Requires:           libbpf
Requires:           psmisc

# Compat symlinks for Requires in other packages.
Provides:           /sbin/ip
%if "%{_sbindir}" == "%{_bindir}"
# We rely on filesystem to create the symlink for us.
Requires:           filesystem(unmerged-sbin-symlinks)
Provides:           /usr/sbin/ip
Provides:           /usr/sbin/ss
%endif

%description
The iproute package contains networking utilities (ip and rtmon, for example)
which are designed to use the advanced networking capabilities of the Linux
kernel.

%package tc
Summary:            Linux Traffic Control utility
License:            GPL-2.0-or-later
Requires:           %{name}%{?_isa} = %{version}-%{release}
Provides:           /sbin/tc

%description tc
The Traffic Control utility manages queueing disciplines, their classes and
attached filters and actions. It is the standard tool to configure QoS in
Linux.

%if ! 0%{?_module_build}
%package doc
Summary:            Documentation for iproute2 utilities with examples
License:            GPL-2.0-or-later
Requires:           %{name} = %{version}-%{release}

%description doc
The iproute documentation contains howtos and examples of settings.
%endif

%package devel
Summary:            iproute development files
License:            GPL-2.0-or-later
Requires:           %{name} = %{version}-%{release}
Provides:           iproute-static = %{version}-%{release}

%description devel
The libnetlink static library.

%prep
%autosetup -p1 -n %{name}2-%{version}

%build
%configure --color auto
echo -e "\nPREFIX=%{_prefix}\nSBINDIR=%{_sbindir}" >> config.mk
%make_build

%install
%make_install

echo '.so man8/tc-cbq.8' > %{buildroot}%{_mandir}/man8/cbq.8

# libnetlink
install -D -m644 include/libnetlink.h %{buildroot}%{_includedir}/libnetlink.h
install -D -m644 lib/libnetlink.a %{buildroot}%{_libdir}/libnetlink.a

# drop these files, iproute-doc package extracts files directly from _builddir
rm -rf '%{buildroot}%{_docdir}'

# append deprecated values to rt_dsfield for compatibility reasons
%if 0%{?rhel}
cat %{SOURCE1} >>%{buildroot}%{_datadir}/iproute2/rt_dsfield
%endif

%files
%dir %{_datadir}/iproute2
%license COPYING
%doc README README.devel
%{_mandir}/man7/*
%exclude %{_mandir}/man7/tc-*
%{_mandir}/man8/*
%exclude %{_mandir}/man8/tc*
%exclude %{_mandir}/man8/cbq*
%attr(644,root,root) %config(noreplace) %{_datadir}/iproute2/*
%{_sbindir}/*
%exclude %{_sbindir}/tc
%exclude %{_sbindir}/routel
%{_datadir}/bash-completion/completions/devlink

%files tc
%license COPYING
%{_mandir}/man7/tc-*
%{_mandir}/man8/tc*
%{_mandir}/man8/cbq*
%dir %{_libdir}/tc/
%{_libdir}/tc/*
%{_sbindir}/tc
%{_datadir}/bash-completion/completions/tc

%if ! 0%{?_module_build}
%files doc
%license COPYING
%doc examples
%endif

%files devel
%license COPYING
%{_mandir}/man3/*
%{_libdir}/libnetlink.a
%{_includedir}/libnetlink.h
%{_includedir}/iproute2/bpf_elf.h

%changelog
* Thu Dec 12 2024 Andrea Claudi <aclaudi@redhat.com> - 6.11.0-1.el9
- New version 6.11.0 (Andrea Claudi) [RHEL-62931]
- Remove old iproute2 source tarballs

* Tue Jan 23 2024 Andrea Claudi <aclaudi@redhat.com> - 6.7.0-2.el9
- rpmautospec not available in build root, revert spec file changes (Andrea Claudi)

* Fri Jan 19 2024 Andrea Claudi <aclaudi@redhat.com> - 6.7.0-1.el9
- New version 6.7.0 (Andrea Claudi) [RHEL-9703]

* Tue Jun 06 2023 Andrea Claudi <aclaudi@redhat.com> - 6.2.0-5.el9
- tc: add missing separator (Andrea Claudi) [RHEL-337]
- u32: fix TC_U32_TERMINAL printing (Andrea Claudi) [RHEL-586]

* Mon Jun 05 2023 Andrea Claudi <aclaudi@redhat.com> - 6.2.0-4.el9
- Fix NVR, %autorelease not working (Andrea Claudi)

* Thu Jun 01 2023 Wen Liang <wenliang@redhat.com> - 6.2.0-3.el9
- mptcp: add support for implicit flag (Wen Liang) [2109135]

* Wed May 03 2023 Andrea Claudi <aclaudi@redhat.com> - 6.2.0-2.el9
- macvlan: Add bclim parameter (Andrea Claudi) [2186945]
- Update kernel headers (Andrea Claudi) [2186945]

* Thu Apr 27 2023 Andrea Claudi <aclaudi@redhat.com> - 6.2.0-1.el9
- New version 6.2.0 (Andrea Claudi) [RHEL-428]

* Sat Jan 28 2023 Andrea Claudi <aclaudi@redhat.com> - 6.1.0-1.el9
- New version 6.1.0 [2155604]

* Fri Jan 06 2023 Viktor Malik <vmalik@redhat.com> - 6.0.0-2.el9
- Rebuild for libbpf 1.0.0 [2158727]

* Thu Oct 06 2022 Andrea Claudi <aclaudi@redhat.com> - 6.0.0-1.el9
- New version 6.0.0 [2132427]

* Wed Jun 15 2022 Andrea Claudi <aclaudi@redhat.com> - 5.18.0-1.el9
- New version 5.18.0 [2074608]

* Thu Nov 25 2021 Andrea Claudi <aclaudi@redhat.com> - 5.15.0-2.el9
- Fix gating.yaml [2009355]

* Wed Nov 24 2021 Andrea Claudi <aclaudi@redhat.com> - 5.15.0-1.el9
- New version 5.15.0 [2009355]

* Wed Aug 18 2021 Andrea Claudi <aclaudi@redhat.com> - 5.13.0-5.el9
- Add build and runtime dependency on libbpf (Andrea Claudi) [1994520]
- Use TC_LIB_DIR environment variable (Andrea Claudi) [1994545]
- Re-add iproute-doc package on the specfile (Andrea Claudi) [1994581]

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 5.13.0-4.el9
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

%define srcname gwdatafind
%define version 1.2.0
%define release 1

Name:      python-%{srcname}
Version:   %{version}
Release:   %{release}%{?dist}
Summary:   The client library for the GWDataFind service
Group:     Development/Libraries
License:   GPLv3+
Url:       https://gwdatafind.readthedocs.io/
Source0:   %pypi_source
Packager:  Duncan Macleod <duncan.macleod@ligo.org>

BuildArch: noarch

# build requirements
BuildRequires: python%{python3_pkgversion}-devel >= 3.6
BuildRequires: python%{python3_pkgversion}-pip
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-wheel

# man pages
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
BuildRequires: argparse-manpage >= 3
%endif
BuildRequires: python%{python3_pkgversion}-igwn-auth-utils >= 0.3.1
BuildRequires: python%{python3_pkgversion}-ligo-segments

# testing dependencies
BuildRequires: man-db
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
BuildRequires: python%{python3_pkgversion}-pytest >= 2.8.0
BuildRequires: python%{python3_pkgversion}-requests-mock
%endif

# -- src.rpm

%description
The DataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors. This is the source package for the
GWDataFind client API.

# -- gwdatafind

%package -n %{srcname}
Summary: %{summary}
Requires: python%{python3_pkgversion}-%{srcname} = %{version}-%{release}
Conflicts: glue < 1.61.0
Conflicts: python2-gwdatafind < 1.0.4-3
%description -n %{srcname}
The DataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors. This package provides the python interface
libraries.

# -- python3x-gwdatafind

%package -n python%{python3_pkgversion}-%{srcname}
Summary:  Python %{python3_version} library for the GWDataFind service
Requires: python%{python3_pkgversion}-igwn-auth-utils >= 0.3.1
Requires: python%{python3_pkgversion}-ligo-segments
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
%description -n python%{python3_pkgversion}-%{srcname}
The DataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors. This package provides the
Python %{python3_version} interface libraries.

# -- build steps

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel gwdatafind-%{version}-*.whl
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
mkdir -vp %{buildroot}%{_mandir}/man1
env PYTHONPATH="%{buildroot}%{python3_sitelib}" \
argparse-manpage \
    --description "discover available GW data" \
    --function command_line \
    --module gwdatafind.__main__ \
    --output %{buildroot}%{_mandir}/man1/gw_data_find.1 \
    --prog gw_data_find \
    --project-name %{srcname} \
    --version %{version} \
    --url %{url} \
;
%endif

%check
export PYTHONPATH="%{buildroot}%{python3_sitelib}"
# sanity checks
%{__python3} -m gwdatafind --help
%{buildroot}%{_bindir}/gw_data_find --help

%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
# test man pages
env MANPATH="%{buildroot}%{_mandir}" man -P cat gw_data_find
# run test suite
%{__python3} -m pytest --pyargs gwdatafind
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %{srcname}
%license LICENSE
%doc README.md
%{_bindir}/gw_data_find
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
%{_mandir}/man1/gw_data_find.1*
%endif

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

# -- changelog

%changelog
* Sat Dec 16 2023 Duncan Macleod <duncan.macleod@ligo.org> 1.2.0-1
- update for 1.2.0
- add python3-devel to BuildRequires
- use argparse-manpage to build manuals, not help2man

* Mon Nov 21 2022 Duncan Macleod <duncan.macleod@ligo.org> 1.1.3-1
- update for 1.1.3

* Thu Sep 29 2022 Duncan Macleod <duncan.macleod@ligo.org> 1.1.2-1
- update for 1.1.2
- update igwn-auth-utils minimum version
- remove extra packages for igwn-auth-utils[requests]

* Mon May 09 2022 Duncan Macleod <duncan.macleod@ligo.org> 1.1.1-1
- update for 1.1.1

* Thu Apr 21 2022 Duncan Macleod <duncan.macleod@ligo.org> 1.1.0-1
- update for 1.1.0
- project now requires python3-igwn-auth-utils/requests

* Fri Jan 28 2022 Duncan Macleod <duncan.macleod@ligo.org> 1.0.5-1
- update for 1.0.5
- rename SRPM to not match any binary RPMs
- drop Python 2 packages
- update summary text to not reference LDR
- separate bindir into separate package

* Fri Jul 12 2019 Duncan Macleod <duncan.macleod@ligo.org> 1.0.4-2
- fixed incorrect installation of /usr/bin/gw_data_find
- use python-srpm-macros to provide python3 versions

* Fri Jan 11 2019 Duncan Macleod <duncan.macleod@ligo.org> 1.0.4-1
- include command-line client, requires matching glue release

* Fri Jan 04 2019 Duncan Macleod <duncan.macleod@ligo.org> 1.0.3-1
- added python3 packages

* Tue Aug 14 2018 Duncan Macleod <duncan.macleod@ligo.org> 1.0.2-1
- bug-fix release

* Tue Aug 14 2018 Duncan Macleod <duncan.macleod@ligo.org> 1.0.1-1
- bug-fix release

* Mon Jul 30 2018 Duncan Macleod <duncan.macleod@ligo.org> 1.0.0-1
- first build

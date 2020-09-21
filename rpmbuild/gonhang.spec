%global pypi_name gonhang
%global debug_package %{nil}
Name:           %{pypi_name}
Version:        0.3.6
Release:        1%{?dist}
Summary:        The Next Generation Light-Weight System Monitor for Linux
License:        MIT
URL:            https://github.com/fredcox/gonhang
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  desktop-file-utils
BuildRequires:  python3-setuptools

Requires:       python3-qt5-base
Requires:       python3-pyqt5-sip
Requires:       python3-psutil
Requires:       python3-humanfriendly
Requires:       python3-requests
Requires:       curl
Requires:       wmctrl
Requires:       hddtemp
Requires:       fira-code-fonts

%description
 GonhaNG is a System Monitor for several important hardware variables.



%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install
# install desktop file
desktop-file-install                                    \
  --dir=%{buildroot}%{_datadir}/applications              \
  $RPM_BUILD_DIR/%{pypi_name}-%{version}/%{pypi_name}/%{pypi_name}.desktop
# install icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
install $RPM_BUILD_DIR/%{pypi_name}-%{version}/%{pypi_name}/images/%{pypi_name}_icon.png \
  %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{pypi_name}_icon.png
# install manual
mkdir -p %{buildroot}%{_datadir}/man/man1/
install -m0644 $RPM_BUILD_DIR/%{pypi_name}-%{version}/%{pypi_name}.1.gz \
  %{buildroot}%{_datadir}/man/man1/%{pypi_name}.1.gz





%files -n %{pypi_name}
%doc README.me
%license LICENSE
%{_bindir}/gonhang
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%{_datadir}/applications/%{pypi_name}.desktop
%{_datadir}/icons/hicolor/48x48/apps/%{pypi_name}_icon.png
%{_mandir}/man1/gonhang.1.gz

%changelog
* Fri Sep 12 2020 Fred Lins <fredcox@gmail.com>
- 0.3.6-1
- release

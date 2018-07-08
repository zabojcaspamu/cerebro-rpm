Name:           cerebro 
Version:        0.8.1
Release:        1 
Summary:        Cerebro is an open source elasticsearch web admin tool .
Group:          Applications/Admin
License:        GPL
URL:            https://github.com/lmenezes/cerebro 
Source0:        https://github.com/lmenezes/cerebro/releases/download/v%{version}/cerebro-%{version}.tgz 
Source1:        cerebro.service 
Source2:        cerebro.sysconfig
Patch1:         cerebro.conf.patch 
BuildRequires:  systemd
#Prefix:         %{_prefix}
#BuildRoot:      %{_tmppath}/%{name}-root

Requires(pre): shadow-utils
Requires: systemd-sysv, java-1.8.0-openjdk, openssl, coreutils

%description
Cerebro is an open source(MIT License) elasticsearch web admin tool built using Scala, Play Framework, AngularJS and Bootstrap.

%pre
getent group cerebro >/dev/null || groupadd -r cerebro
getent passwd cerebro >/dev/null || \
    useradd -r -g cerebro -M -s /sbin/nologin \
    -c "User for cerebro" cerebro
exit 0

%prep
%setup -q 
%patch1 -p1 -b .orig 

%build

%install
mkdir -p %{buildroot}/opt/cerebro
mkdir -p %{buildroot}/opt/cerebro/logs
mkdir -p %{buildroot}/opt/cerebro/data
mkdir -p %{buildroot}/var/run/cerebro
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/sysconfig
cp -a * %{buildroot}/opt/cerebro
%{__install} -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/
%{__install} -p -m 644 %{SOURCE2} %{buildroot}/etc/sysconfig/cerebro

%clean
rm -rf %{buildroot}

%post 
case "$1" in
  1)
    # This is an initial install.
    systemctl enable cerebro.service 2>/dev/null
    systemctl daemon-reload 
    RANDOMSTRING=`openssl rand -base64 32|tr -dc _A-Z-a-z-0-9`
    /usr/bin/sed -i "s/^secret.\+$/secret = \"$RANDOMSTRING\"/" /opt/cerebro/conf/application.conf 
  ;;
  2)
    # This is an upgrade.
    # First delete the registered service.
    # Then add the registered service. In case run levels changed in the init script, the service will be correctly re-added.
    systemctl daemon-reload
  ;;
esac

%preun
case "$1" in
  0)
    # This is an un-installation.
    systemctl stop cerebro.service
    systemctl disable cerebro.service 2>/dev/null
    rm -f /etc/systemd/system/multi-user.target.wants/cerebro.service
    systemctl daemon-reload 
  ;;
  1)
    # This is an upgrade.
    # Do nothing.
    :
  ;;
esac

%postun
case "$1" in
  0)
    # This is an un-installation.
    rm -rf /opt/cerebro
    rm -rf /var/run/cerebro/
    rm -rf /etc/sysconfig/cerebro
    userdel --force cerebro 2> /dev/null; true
    groupdel cerebro 2> /dev/null; true
  ;;
  1)
    # This is an upgrade.
    # Do nothing.
    :
  ;;
esac

%files
#%dir /opt/cerebro
/opt/cerebro
%config /etc/sysconfig/cerebro
%{_unitdir}/cerebro.service
%attr(-, cerebro, cerebro) /opt/cerebro/logs
%attr(-, cerebro, cerebro) /opt/cerebro/data
%attr(-, cerebro, cerebro) /var/run/cerebro

%changelog 
* Fri Feb 16 2018 zabojcaspamu.pl <zabojcaspamu.pl> 
- Cerebro to rpm

Summary:	POP3 daemon from Qualcomm
Summary(pl):	Serwer POP3 tworzony przez Qualcomm
Name:		qpopper
Version:	4.0.4
Release:	0.1
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.qualcomm.com/eudora/servers/unix/popper/%{name}%{version}.tar.gz
Source1:	%{name}.pamd
Source2:	%{name}.inetd
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Patch0:		%{name}4.0.4-ipv6-20020502.diff.gz
URL:		http://www.eudora.com/freeware/
BuildRequires:	pam-devel
BuildRequires:	gdbm-devel
BuildRequires:	autoconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
POP3 server from QUALCOMM, with the following features: lower memory
requirements, thus faster UIDL assists POP clients which "leave mail
on server" in determining which messages are new. Implements some
other extended POP3 commands.

%description -l pl
Qpopper jest serwerem POP3 tworzonym przez QUALCOMM. Wymaga
zdecydowanie mniej zasobów ni¿ inne serwery. Implementuje funkcje
zostawiana wiadomo¶ci na serwerze (a tak¿e inne rozszerzenia POP3
takie jak APOP, czy biuletins oraz XMIT i XLIST).

%package common
Summary:	POP3 daemon from Qualcomm - common files
Summary(pl):	Serwer POP3 tworzony przez Qualcomm - wspólne pliki
Group:		Networking/Daemons
Obsoletes:	qpopper < 0:4.0.4-1

%description common
POP3 server from QUALCOMM, with the following features: lower memory
requirements, thus faster UIDL assists POP clients which "leave mail
on server" in determining which messages are new. Implements some
other extended POP3 commands. Qpopper also supports TLS/SSL.

%description common -l pl
Qpopper jest serwerem POP3 tworzonym przez QUALCOMM. Wymaga
zdecydowanie mniej zasobów ni¿ inne serwery. Implementuje funkcje
zostawiana wiadomo¶ci na serwerze (a tak¿e inne rozszerzenia POP3
takie jak APOP, czy biuletins oraz XMIT i XLIST). Qpopper obs³uguje
tak¿e TLS/SSL.

%package inetd
Summary:	inetd configs for Qpopper
Summary(pl):	Pliki konfiguracyjne do u¿ycia Qpoppera poprzez inetd
Group:		Networking/Daemons
Prereq:		%{name}-common = %{version}
Prereq:		rc-inetd
Provides:	qpopper = %{version}-%{release}
Requires:	inetdaemon
Obsoletes:	qpopper-standalone
Obsoletes:	qpopper6
Obsoletes:	solid-pop3d
Obsoletes:	imap-pop

%description inetd
Qpopper configs for running from inetd.

%description inetd -l pl
Pliki konfiguracyjna Qpoppera do startowania demona poprzez inetd.

%package standalone
Summary:	standalone daemon configs for Qpopper
Summary(pl):	Pliki konfiguracyjne do startowania Qpoppera w trybie standalone
Group:		Networking/Daemons
Prereq:		%{name}-common = %{version}
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
Provides:	qpopper = %{version}-%{release}
Obsoletes:	qpopper-inetd
Obsoletes:	qpopper6
Obsoletes:	solid-pop3d
Obsoletes:	imap-pop

%description standalone
Qpopper configs for running as a standalone daemon.

%description standalone -l pl
Pliki konfiguracyjne Qpoppera do startowania demona w trybie
standalone.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1

%build
rm -f configure
%{__autoconf}
%configure \
	--enable-bulletins=%{_var}/mail/bulletins \
	--enable-bulldb=%{_var}/mail/bulletins \
	--enable-apop=%{_sysconfdir}/qpopper/pop.auth \
	--with-popuid=mail \
	--with-pam=qpopper \
	--enable-log-login \
 	--enable-log-facility=LOG_MAIL \
 	--enable-uw-kludge \
 	--enable-nonauth-file=/etc/qpopper/blacklist \
 	--enable-specialauth \
 	--with-openssl \
	--with-gdbm \
	--enable-ipv6

%{__make}
mv -f popper/popper popper/popper.inetd
%{__make} clean

%configure \
	--enable-bulletins=%{_var}/mail/bulletins \
	--enable-bulldb=%{_var}/mail/bulletins \
	--enable-apop=%{_sysconfdir}/qpopper/pop.auth \
	--with-popuid=mail \
	--with-pam=qpopper \
	--enable-log-login \
 	--enable-log-facility=LOG_MAIL \
 	--enable-uw-kludge \
 	--enable-nonauth-file=/etc/qpopper/blacklist \
 	--enable-specialauth \
 	--with-openssl \
	--with-gdbm \
	--enable-ipv6 \
	--enable-standalone

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT%{_var}/mail/bulletins \
	$RPM_BUILD_ROOT%{_sysconfdir}/{pam.d/,qpopper,security,sysconfig/rc-inetd,rc.d/init.d}

install popper/popper.inetd $RPM_BUILD_ROOT%{_sbindir}/qpopper
install popper/popper $RPM_BUILD_ROOT%{_sbindir}/qpopperd
install popper/popauth $RPM_BUILD_ROOT%{_sbindir}/popauth

install samples/qpopper.config $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/config

install man/popper.8 $RPM_BUILD_ROOT%{_mandir}/man8/qpopper.8
echo ".so popper8" >$RPM_BUILD_ROOT%{_mandir}/man8/qpopperd.8
install man/popauth.8 $RPM_BUILD_ROOT%{_mandir}/man8/popauth.8

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/qpopper
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/qpopper
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/qpopper
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/qpopper

touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.auth
touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.deny
touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.auth.db
touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.auth.dir
touch $RPM_BUILD_ROOT/etc/security/blacklist.qpopper

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo -e `	ls -lFd /usr/sbin/popauth `
if [ ! -f /etc/qpopper/pop.auth ]; then
        popauth -init
fi
if [ ! -f /etc/qpopper/pop.deny ]; then
        echo -e "root \n" > /etc/qpopper/pop.deny
fi

%post inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun inetd
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
fi

%post standalone
/sbin/chkconfig --add qpopper
if [ -f /var/lock/subsys/qpopper ]; then
	/etc/rc.d/init.d/qpopper restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/qpopper start\" to start Qpopper daemon."
fi

%preun standalone
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/qpopper ]; then
		/etc/rc.d/init.d/qpopper stop 1>&2
	fi
	/sbin/chkconfig --del qpopper
fi

%files common
%defattr(644,root,root,755)
%doc doc/* GUIDE.pdf
%dir %{_var}/mail/bulletins
%attr(4755,root,root) %{_sbindir}/popauth
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/qpopper
%attr(770,root,mail) %dir %{_sysconfdir}/qpopper
%attr(660,root,mail) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/qpopper/pop.*
%attr(660,root,mail) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/qpopper/config
%attr(640,root,mail) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.qpopper
%{_mandir}/man8/*

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/qpopper
%attr(0755,root,root) %{_sbindir}/qpopper

%files standalone
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/qpopper
%attr(754,root,root) /etc/rc.d/init.d/qpopper
%attr(0755,root,root) %{_sbindir}/qpopperd

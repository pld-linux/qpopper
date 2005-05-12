#
# Conditional build:
# 	_with_mysql - MySQL auth support

Summary:	POP3 daemon from Qualcomm
Summary(pl):	Serwer POP3 tworzony przez Qualcomm
Summary(ru):	Qpopper - наиболее распространенный POP3 сервер для UNIX
Summary(uk):	Qpopper - найпоширен╕ший POP3 сервер для UNIX
Name:		qpopper
Version:	4.0.5
Release:	6
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.qualcomm.com/eudora/servers/unix/popper/%{name}%{version}.tar.gz
# Source0-md5:	e00853280c9e899711f0b0239d3d8f86
Source1:	%{name}.pamd
Source2:	%{name}.inetd
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Source5:	%{name}-ssl.inetd
Source6:	%{name}-ssl.init
Source7:	%{name}-ssl.sysconfig
Patch0:		%{name}4.0.4-ipv6-20020502.diff.gz
Patch1:		%{name}-config.patch
Patch2:		%{name}-basename.patch
Patch3:		%{name}-man.patch
Patch4:		http://asteroid-b612.org/software/qpopper-mysql/%{name}-mysql-0.6.patch
Patch5:		%{name}-gdbm-compat.patch
Patch6:		%{name}-one_auth_error.patch
Patch7:		%{name}-sendmail.patch
URL:		http://www.eudora.com/freeware/
BuildRequires:	autoconf
BuildRequires:	gdbm-devel
%{?_with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	pam-devel
Requires:	pam >= 0.79.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
POP3 server from QUALCOMM, with the following features: lower memory
requirements, thus faster UIDL assists POP clients which "leave mail
on server" in determining which messages are new. Implements some
other extended POP3 commands.

%description -l pl
Qpopper jest serwerem POP3 tworzonym przez QUALCOMM. Wymaga
zdecydowanie mniej zasobСw ni© inne serwery. Implementuje funkcje
zostawiana wiadomo╤ci na serwerze (a tak©e inne rozszerzenia POP3
takie jak APOP, czy biuletins oraz XMIT i XLIST).

%description -l ru
Qpopper от QUALCOMM поддерживает распространенный протокол POP3
получения почты с сервера, используемый многими почтовыми клиентами.

Эта версия требует меньше памяти и имеет более быстрый UIDL (Unique ID
Listing), который помогает почтовым клиентам, оставляющим почту на
сервере, в определении того, какие сообщения еще не прочитаны. Также
она включает расширенные (опциональные) команды POP3 и бюллетени.

%description -l uk
Qpopper в╕д QUALCOMM п╕дтриму╓ розповсюджений протокол POP3 отримання
пошти з сервера, який використову╓ться багатьма поштовими кл╕╓нтами.

Ця верс╕я вимага╓ менше пам'ят╕ та ма╓ б╕льш швидкий UIDL (Unique ID
Listing), який допомага╓ поштовим кл╕╓нтам, як╕ лишають пошту на
сервер╕, у визначенн╕ як╕ пов╕домлення ще не прочитан╕. Також вона
м╕стить розширен╕ (опц╕ональн╕) команди POP3 та бюлетен╕.

%package common
Summary:	POP3 daemon from Qualcomm - common files
Summary(pl):	Serwer POP3 tworzony przez Qualcomm - wspСlne pliki
Group:		Networking/Daemons
Obsoletes:	qpopper < 0:4.0.4-1

%description common
POP3 server from QUALCOMM, with the following features: lower memory
requirements, thus faster UIDL assists POP clients which "leave mail
on server" in determining which messages are new. Implements some
other extended POP3 commands. Qpopper also supports TLS/SSL.

%description common -l pl
Qpopper jest serwerem POP3 tworzonym przez QUALCOMM. Wymaga
zdecydowanie mniej zasobСw ni© inne serwery. Implementuje funkcje
zostawiana wiadomo╤ci na serwerze (a tak©e inne rozszerzenia POP3
takie jak APOP, czy biuletins oraz XMIT i XLIST). Qpopper obsЁuguje
tak©e TLS/SSL.

%package inetd
Summary:	inetd configs for Qpopper
Summary(pl):	Pliki konfiguracyjne do u©ycia Qpoppera poprzez inetd
Group:		Networking/Daemons
PreReq:		%{name}-common = %{version}-%{release}
PreReq:		rc-inetd
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

%package ssl-inetd
Summary:	inetd configs for Qpopper with SSL (pop3s)
Summary(pl):	Pliki konfiguracyjne do u©ycia Qpoppera poprzez inetd z obslug╠ SSL (pop3s)
Group:		Networking/Daemons
PreReq:		%{name}-common = %{version}-%{release}
PreReq:		%{name}-inetd = %{version}-%{release}
PreReq:		rc-inetd
Requires:	inetdaemon

%description ssl-inetd
Qpopper configs for running from inetd with SSL (pop3s).

%description ssl-inetd -l pl
Pliki konfiguracyjna Qpoppera do startowania demona poprzez inetd z
obsЁug╠ SSL (pop3s).

%package standalone
Summary:	standalone daemon configs for Qpopper
Summary(pl):	Pliki konfiguracyjne do startowania Qpoppera w trybie standalone
Group:		Networking/Daemons
PreReq:		%{name}-common = %{version}
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
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

%package ssl-standalone
Summary:	standalone daemon configs for Qpopper with SSL on separate port (pop3s)
Summary(pl):	Pliki konfiguracyjne do startowania Qpoppera w trybie standalone z obsЁug╠ SSL na oddzielnym porcie (pop3s)
Group:		Networking/Daemons
PreReq:		%{name}-common = %{version}-%{release}
PreReq:		%{name}-standalone = %{version}-%{release}
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig

%description ssl-standalone
Qpopper configs for running as a standalone daemon in SSL mode on
separate port (pop3s).

%description ssl-standalone -l pl
Pliki konfiguracyjne Qpoppera do startowania demona w trybie
standalone z obsЁug╠ SSL na oddzielnym porcie (pop3s).

%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%{?_with_mysql:%patch4 -p1}
%patch6 -p1
%patch7 -p1

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
	--enable-nonauth-file=%{_sysconfdir}/qpopper/blacklist \
	--enable-specialauth \
	--with-openssl \
	--with-gdbm \
%if %{?_with_mysql:1}0
	--enable-mysql \
	--with-mysqlconfig=%{_sysconfdir}/qpopper/mysql-popper.conf \
	--with-mysqlincludepath=%{_includedir}/mysql \
	--with-mysqllibpath=%{_libdir} \
%endif
	--with-sendmail=/usr/sbin/sendmail \
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
	--enable-nonauth-file=%{_sysconfdir}/qpopper/blacklist \
	--enable-specialauth \
	--with-openssl \
	--with-gdbm \
%if %{?_with_mysql:1}0
	--enable-mysql \
	--with-mysqlconfig=%{_sysconfdir}/qpopper/mysql-popper.conf \
	--with-mysqlincludepath=%{_includedir}/mysql \
	--with-mysqllibpath=%{_libdir} \
%endif
	--with-sendmail=/usr/sbin/sendmail \
	--enable-ipv6 \
	--enable-standalone

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT%{_var}/mail/bulletins \
	$RPM_BUILD_ROOT%{_sysconfdir}/{pam.d/,qpopper,security,sysconfig/rc-inetd,rc.d/init.d}

install popper/popauth $RPM_BUILD_ROOT%{_sbindir}/popauth
install popper/popper.inetd $RPM_BUILD_ROOT%{_sbindir}/qpopper
install popper/popper $RPM_BUILD_ROOT%{_sbindir}/qpopperd
ln -sf qpopperd $RPM_BUILD_ROOT%{_sbindir}/qpoppersd

install samples/qpopper.config $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/config
install samples/qpopper.config $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/config-ssl
%{?_with_mysql:install mysql-popper.conf $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/mysql-popper.conf}

install man/popper.8 $RPM_BUILD_ROOT%{_mandir}/man8/qpopper.8
echo ".so popper8" >$RPM_BUILD_ROOT%{_mandir}/man8/qpopperd.8
install man/popauth.8 $RPM_BUILD_ROOT%{_mandir}/man8/popauth.8

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/qpopper
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/qpopper
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/qpopper
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/qpopper
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/qpoppers
install %{SOURCE6} $RPM_BUILD_ROOT/etc/rc.d/init.d/qpoppers
install %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/qpoppers

touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.auth
touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.deny
touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.auth.db
touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.auth.dir
touch $RPM_BUILD_ROOT/etc/security/blacklist.qpopper

%clean
rm -rf $RPM_BUILD_ROOT

%post common
umask 007
echo -e `	ls -lFd /usr/sbin/popauth `
if [ ! -f /etc/qpopper/pop.auth ]; then
	popauth -init
fi
if [ ! -f /etc/qpopper/pop.deny ]; then
	echo -e "root \n" > /etc/qpopper/pop.deny
	chown root:mail /etc/qpopper/pop.deny
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

%post ssl-inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun ssl-inetd
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

%post ssl-standalone
/sbin/chkconfig --add qpoppers
if [ -f /var/lock/subsys/qpoppers ]; then
	/etc/rc.d/init.d/qpoppers restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/qpoppers start\" to start Qpopper SSL daemon."
fi

%preun ssl-standalone
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/qpoppers ]; then
		/etc/rc.d/init.d/qpoppers stop 1>&2
	fi
	/sbin/chkconfig --del qpoppers
fi

%files common
%defattr(644,root,root,755)
%doc doc/* GUIDE.pdf README*
%dir %{_var}/mail/bulletins
%attr(4755,root,root) %{_sbindir}/popauth
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/qpopper
%attr(770,root,mail) %dir %{_sysconfdir}/qpopper
%attr(660,root,mail) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qpopper/pop.*
%if %{?_with_mysql:1}0
%attr(660,root,mail) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qpopper/mysql-popper.conf
%endif
%attr(640,root,mail) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.qpopper
%{_mandir}/man8/*

%files inetd
%defattr(644,root,root,755)
%attr(660,root,mail) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qpopper/config
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/qpopper
%attr(755,root,root) %{_sbindir}/qpopper

%files ssl-inetd
%defattr(644,root,root,755)
%attr(660,root,mail) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qpopper/config-ssl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/qpoppers

%files standalone
%defattr(644,root,root,755)
%attr(660,root,mail) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qpopper/config
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/qpopper
%attr(754,root,root) /etc/rc.d/init.d/qpopper
%attr(755,root,root) %{_sbindir}/qpopperd

%files ssl-standalone
%defattr(644,root,root,755)
%attr(660,root,mail) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qpopper/config-ssl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/qpoppers
%attr(754,root,root) /etc/rc.d/init.d/qpoppers
%attr(755,root,root) %{_sbindir}/qpoppersd

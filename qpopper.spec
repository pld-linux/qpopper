Summary:	POP3 daemon from Qualcomm
Summary(pl):	Serwer POP3 tworzony przez Qualcomm
Name:		qpopper
Version:	3.0.2
Release:	7
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.qualcomm.com/eudora/servers/unix/popper/%{name}%{version}.tar.Z
Source1:	%{name}.pamd
Source2:	%{name}.inetd
Patch0:		%{name}-homemaildir.patch
Patch1:		%{name}3.0-v6-20000922.patch.gz
URL:		http://www.eudora.com/freeware/
Requires:	pam >= 0.66
Requires:	inetdaemon
Prereq:		rc-inetd
BuildRequires:	pam-devel
BuildRequires:	gdbm-devel
BuildRequires:	autoconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	qpopper6
Obsoletes:	solid-pop3d
Obsoletes:	imap-pop

%description
POP3 server from QUALCOMM, with the following features: lower memory
requirements, thus faster UIDL assists POP clients which "leave mail
on server" in determining which messages are new. Implements some
other extended POP3 commands.

This version of qpopper is shadow passwords aware, provied your libc
supports this.

The Linux version also supports the PAM library (so far the PAM
modifications aren't officially supported by Qualcomm. All questions,
complaints etc. according PAM support should be directed to Marek
Habersack <grendel@vip.maestro.com.pl>)

%description -l pl
Qpopper jest serwerem POP3 tworzonym przez QUALCOMM. Wymaga
zdecydowanie mniej zasobów ni¿ inne serwery. Implementuje funkcje
zostawiana wiadomo¶ci na serwerze (a tak¿e inne rozszerzenia POP3
takie jak APOP, czy biuletins oraz XMIT i XLIST). U¿ywa tak¿e
dostarczanych przez bibliotekê libc funkcji `shadow passwords' jak i
(w wersji Linuksowej) PAM (wsparcie dla PAM zosta³o dodane przez:
Marka Habersacka <grendel@vip.maestro.com.pl>).

%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1

%build
rm -f configure
%{__autoconf}
%configure \
	--enable-bulletins=%{_var}/mail/bulletins \
	--enable-apop=%{_sysconfdir}/qpopper/pop.auth \
	--with-apopuid=mail \
	--with-pam=qpopper \
	--enable-log-login \
	--enable-ipv6

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT%{_var}/mail/bulletins \
	$RPM_BUILD_ROOT%{_sysconfdir}/{pam.d/,qpopper,security,sysconfig/rc-inetd}

install popper/popper $RPM_BUILD_ROOT%{_sbindir}/qpopper
install popper/popauth $RPM_BUILD_ROOT%{_sbindir}/popauth

install man/popper.8 $RPM_BUILD_ROOT%{_mandir}/man8/qpopper.8
install man/popauth.8 $RPM_BUILD_ROOT%{_mandir}/man8/popauth.8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/qpopper
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/qpopper

touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.auth
touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.deny
touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.auth.db
touch $RPM_BUILD_ROOT%{_sysconfdir}/qpopper/pop.auth.dir
touch $RPM_BUILD_ROOT/etc/security/blacklist.qpopper

gzip -9nf doc/*

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
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
fi

%files
%defattr(644,root,root,755)
%doc doc/*
%dir %{_var}/mail/bulletins
%attr(0755,root,root) %{_sbindir}/qpopper
%attr(4755,root,root) %{_sbindir}/popauth
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/qpopper
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/qpopper
%attr(770,root,mail) %dir %{_sysconfdir}/qpopper
%attr(660,root,mail) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/qpopper/pop.*
%attr(640,root,mail) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.qpopper
%{_mandir}/man8/*

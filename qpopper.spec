Summary:     POP3 daemon from Qualcomm
Summary(pl): serwer POP3 tworzony przez Qualcomm
Name:        qpopper
Version:     2.53
Release:     4 
Copyright:   BSD
Group:       Networking/Daemons
Group(pl):   Sieciowe/Demony
Source0:     ftp://ftp.qualcomm.com/eudora/servers/unix/popper/%{name}%{version}.tar.Z
Source1:     %{name}.pamd
Patch0:      %{name}%{version}-linux-pam.patch
Patch1:	     %{name}-glibc.patch
Patch2:	     %{name}-massive-kpld.patch
URL:         http://www.eudora.com/freeware/
Requires:    pam >= 0.66
BuildPrereq: pam-devel
BuildPrereq: gdbm-devel
Obsoletes:   qpopper6
BuildRoot:   /tmp/%{name}-%{version}--root

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
Qpopper jest serwerem POP3 tworzonym przez QUALCOMM. Wymaga zdecydowanie 
mniej zasob�w ni� inne serwery. Implementuje funkcje zostawiana wiadomo�ci 
na serwerze (a tak�e inne rozszerzenia POP3 takie jak APOP, czy biuletins 
oraz XMIT i XLIST). U�ywa tak�e dostarczanych przez bibliotek� libc funkcji 
`shadow passwords' jak i (w wersji Linuksowej) PAM (wsparcie dla PAM
zosta�o dodane przez: Marka Habersacka <grendel@vip.maestro.com.pl>). 
 
%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%build
CFLAGS=$RPM_OPT_FLAGS ./configure \
 --prefix=%{_prefix} \
 --enable-bulletins=%{_var}/mail/bulletins \
 --enable-apop=/etc/qpopper/pop.auth \
 --with-apopuid=mail \
 --with-pam
 
make 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install -d $RPM_BUILD_ROOT%{_var}/mail/bulletins
install -d $RPM_BUILD_ROOT/etc/{pam.d/,qpopper,security}
install -s popper $RPM_BUILD_ROOT%{_sbindir}/qpopper

sed -e 's#/usr/etc/popper#/usr/sbin/qpopper#g' < popper.8 \
> $RPM_BUILD_ROOT/%{_mandir}/man8/qpopper.8

install -s popauth $RPM_BUILD_ROOT%{_sbindir}/popauth

install popauth.8 $RPM_BUILD_ROOT%{_mandir}/man8/popauth.8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/qpopper

touch $RPM_BUILD_ROOT/etc/qpopper/pop.auth
touch $RPM_BUILD_ROOT/etc/qpopper/pop.deny
touch $RPM_BUILD_ROOT/etc/qpopper/pop.auth.db
touch $RPM_BUILD_ROOT/etc/qpopper/pop.auth.dir
touch $RPM_BUILD_ROOT/etc/security/blacklist.qpopper

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man8/* doc/*

%post
 	echo -e `	ls -lFd /usr/sbin/popauth `
if [ ! -f /etc/qpopper/pop.auth ]; then
        popauth -init
fi
if [ ! -f /etc/qpopper/pop.deny ]; then
        echo -e "root \n" > /etc/qpopper/pop.deny
fi

if [ -f /etc/inetd.conf ]; then
	echo -e "Add Qpopper entries to /etc/inetd.conf \n"        
        cat /etc/inetd.conf | grep -v "^pop-3" | grep -v "End of inetd.conf" \
                > /tmp/inetd.conf
        echo "# Qualcomm popper" >> /tmp/inetd.conf
        echo "pop-3  stream  tcp     nowait  root  /usr/sbin/tcpd qpopper" >> /tmp/inetd.conf
        echo "# End of inetd.conf" >> /tmp/inetd.conf

        mv /tmp/inetd.conf /etc/inetd.conf
fi

if [ -e /var/run/inetd.pid ]; then
    kill -HUP `cat /var/run/inetd.pid` ;
fi

%preun
if [ -f /etc/inetd.conf ]; then
	echo -e "Removing Qpopper entries from /etc/inetd.conf \n"
        cat /etc/inetd.conf | grep -v "qpopper" | grep -v "Qualcomm popper" \
	> /tmp/inetd.conf
        mv /tmp/inetd.conf /etc/inetd.conf
fi

if [ -e /var/run/inetd.pid ]; then
        kill -HUP `cat /var/run/inetd.pid` ;
fi
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*

%dir %{_var}/mail/bulletins
%attr(0755,root,root) %{_sbindir}/qpopper
%attr(4711,root,root) %{_sbindir}/popauth

%attr(644,root, man) %{_mandir}/man8/*
%attr(640,root,root) %config /etc/pam.d/qpopper
%attr(700,mail,mail) %dir /etc/qpopper
%attr(600,mail,mail) %config(noreplace) %verify(not size mtime md5) /etc/qpopper/pop.*
%attr(640,root,mail) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.qpopper

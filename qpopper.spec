Summary:     POP3 daemon from Qualcomm
Summary(pl): serwer POP3 tworzony przez Qualcomm
Name:        qpopper
Version:     2.53
Release:     3d 
Copyright:   BSD
Group:       Networking/Daemons
Group(pl):   Sieci/Demony
#######      ftp://ftp.qualcomm.com/eudora/servers/unix/popper
Source0:     %{name}%{version}.tar.Z
Source1:     %{name}.pamd
Patch:       %{name}%{version}-linux-pam.patch
URL:         http://www.eudora.com/freeware
Requires:    pam >= 0.66
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
complaints etc. according PAM support should be directed to
Marek Habersack <grendel@vip.maestro.com.pl>)

%description -l pl 
Qpopper jest serwerem POP3 tworzonym przez QUALCOMM. Wymaga zdecydowanie 
mniej zasobów ni¿ inne serwer. Implementuje funkcje zostawiana wiadomo¶ci 
na serwerze (a tak¿e inne rozszerzenia POP3 takie jak APOP, czy biuletins 
oraz XMIT and XLIST). U¿ywa tak dostarczanych przez bibliotekê libc funkcji 
`shadow passwords' jak i (w wersji Linuksowej) PAM (nie wspierane przez 
Qualcomm poprawki zosta³y wykonane przez:
Marka Habersacka <grendel@vip.maestro.com.pl>). 
 
%prep
%setup -q -n %{name}%{version}
%patch -p1

%build
CFLAGS=$RPM_OPT_FLAGS ./configure \
 --prefix=/usr \
 --enable-bulletins=/var/spool/mail/bulletins \
 --enable-apop=/etc/qpopper/pop.auth \
 --with-apopuid=mail \
 --with-pam
 
make 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/{sbin,man/man8}
install -d $RPM_BUILD_ROOT/var/spool/mail/bulletins
install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/qpopper
install -s popper $RPM_BUILD_ROOT/usr/sbin/qpopper

sed -e 's#/usr/etc/popper#/usr/sbin/qpopper#g' < popper.8 \
> $RPM_BUILD_ROOT/usr/man/man8/qpopper.8

install -s popauth $RPM_BUILD_ROOT/usr/sbin/popauth

install popauth.8 $RPM_BUILD_ROOT/usr/man/man8/popauth.8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/qpopper

touch $RPM_BUILD_ROOT/etc/qpopper/pop.auth
touch $RPM_BUILD_ROOT/etc/qpopper/pop.deny
touch $RPM_BUILD_ROOT/etc/qpopper/pop.auth.db
touch $RPM_BUILD_ROOT/etc/qpopper/pop.auth.dir

bzip2 -9 $RPM_BUILD_ROOT/usr/man/man8/* doc/*

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
        cat /etc/inetd.conf | grep -v "pop-3" | grep -v "End of inetd.conf" \
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

%dir /var/spool/mail/bulletins
%attr(0755,root,root) /usr/sbin/qpopper
%attr(4711,root,root) /usr/sbin/popauth

%attr(644,root, man) /usr/man/man8/*
%attr(640,root,root) %config /etc/pam.d/qpopper
%attr(700,mail,mail) %dir /etc/qpopper
%attr(600,mail,mail) %config(noreplace) %verify(not size mtime md5) /etc/qpopper/pop.*

%changelog
* Mon Dec 28 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.53-3d]
- added missing files in /etc/qpopper -- a bug in qpopper ? 

* Tue Sep 8 1998 Ziemek Borowski <ziembor@faq-bot.ziembor.waw.pl>
  [2.53-1d]
- Polish .spec translation
- more detailed %attr for binaries (mail SUID for /usr/sbin/popauth) 
- %post & %postud added (from  Ximenes Zalteca <ximenes@mythic.net> spec:
  http://www.kiva.net/~cdent/pam/)
- %ghost for /etc/pop.auth & /etc/pop.deny 
- todo: qmail subpackage 

* Tue Sep 8 1998 Marek Habersack <grendel@vip.maestro.com.pl>
   [2.53-1PAM]
 - first .spec release of this version 

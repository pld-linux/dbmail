#
%bcond_without	static_libs # don't build static libraries
#
# TODO:
#	- add separate user/group
#	- add subpackages and init / rc-inetd scripts
#	  for dbmail-{pop3,imap,lmtpd}
#	- add cronjob for dbmail-maintenance
#	- review of %{_libdir} content - I'm not sure which files are really needed (I've packed all)
#	- review summaries, descriptions before TRANSLATING them.
#	- review splitting files between subpackages
#	- add bconds for database backends
#
Summary:	Collection of programs for storing and retrieving mail from a SQL database
Summary(pl):	Zestaw programów do zapisywania i odtwarzania poczty z bazy danych SQL
Name:		dbmail
Version:	2.2.1
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.dbmail.org/download/2.2/%{name}-%{version}.tar.gz
# Source0-md5:	0023c5b55bdd2856ed4ec44c729adfdd
Source1:	%{name}-imapd.init
Source2:	%{name}-lmtpd.init
Source3:	%{name}-pop3d.init
URL:		http://www.dbmail.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gmime-devel
BuildRequires:	libtool
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	postgresql-devel
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sqlite3-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DBMAIL is a collection of programs that enables email to be stored in
and retrieved from a database.

Why is it usefull?
==================
Well, for me it's usefull
because a number of reasons.
- It enables me to create mailboxes without the need of system users.
- Mail is more effeciently stored and therefore it can be inserted an
  retrieved much faster than any regular system (DBmail is currently
  able to retrieve aprox. 250 mail messages per second).
- It's more expandable. A database is much easier to access than a
  flat file or a Maildir. We don't need to parse first.
- In my case, I can easily link a mailbox to a certain client which
  enables me to let the client maintaining his/her own mailboxes without
  me needing to technically support it.
- It's scalable. You can run the dbmail programs on different servers
  talking to the same database (cluster).
- It is more secure. There's no need to maintain system users or write
  to the filesystem. All this is done through the database.

%description -l pl
DBMAIL to zestaw programów umo¿liwiaj±cych zapisywanie i odtwarzanie
poczty z bazy danych.

Dlaczego jest to u¿yteczne? Dla autora jest z kilku powodów:
- Umo¿liwia tworzenie skrzynek bez wymagania u¿ytkowników systemowych.
- Poczta jest zapisywana bardziej wydajnie i mo¿e byæ umieszczana oraz
  odtwarzana du¿o szybciej ni¿ w normalnych systemach (DBmail aktualnie
  jest w stanie odczytywaæ oko³o 250 listów na sekundê).
- Jest bardziej rozszerzalne. Dostêp do bazy danych jest ³atwiejszy
  ni¿ do p³askiego pliku lub Maildira. Nie trzeba ich najpierw
  analizowaæ.
- W przypadku autora - mo¿e on ³atwo pod³±czyæ skrzynkê do pewnego
  klienta umo¿liwiaj±c utrzymywanie skrzynek przez klienta bez potrzeby
  technicznego wsparcia administratora.
- Jest skalowalne. Mo¿na uruchamiaæ programy dbmail na ró¿nych
  serwerach komunikuj±cych siê z t± sam± baz± danych (klastrem).
- Jest bardziej bezpieczne. Nie trzeba utrzymywaæ u¿ytkowników
  systemowych ani pisaæ po systemie plików. Wszystkie jest wykonywane w
  bazie danych.

%package imapd
Summary:	imapd daemon for DBMail system
#Summary(pl):
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	dbmail = %{version}-%{release}

%description imapd
dbmail-imapd provides access to the DBMail system to clients
supporting Internet Message Access Protocol, IMAP4r1, as specified in
RFC 3501.

#%%description imapd -l pl


%package lmtpd
Summary:	lmtpd daemon for DBMail system
#Summary(pl):
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	dbmail = %{version}-%{release}

%description lmtpd
dbmail-lmtpd receive messages from an MTA supporting the Lightweight
Mail Transport Protocol, as specified in RFC 2033.

#%%description lmtpd -l pl


%package pop3d
Summary:	pop3d daemon for DBMail system
#Summary(pl):
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	dbmail = %{version}-%{release}

%description pop3d
dbmail-pop3d provides access to the DBMail system to client support-
ing Post Office Protocol, POP3, as specified in RFC 1939.

#%%description pop3d -l pl


%package mailbox2dbmail
Summary:	Copy mail from an mbox file, maildir or mhdir directory to dbmail
Summary(pl):	Kopiowanie poczty z pliku mbox, katalogu maildir lub mhdir do dbmaila
# FIXME: better group
Group:		Applications/Mail
Requires:	%{name} = %{version}-%{release}
Requires:	python-modules >= 2.2

%description mailbox2dbmail
Use this program to copy mail from an mbox file, maildir or mhdir
directory to dbmail. This program uses ./dbmail-smtp for injecting the
emails into DBMail.

%description mailbox2dbmail -l pl
Tego programu mo¿na u¿ywaæ do kopiowania poczty z pliku mbox albo
katalogu maildir lub mhdir do dbmaila. U¿ywa on ./dbmail-smtp do
umieszczania listów w bazie DBMail.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static=%{?with_static_libs:yes}%{!?with_static_libs:no} \
	--with-mysql \
	--with-pgsql \
	--with-sqlite \
	--with-auth-ldap \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},/etc/{rc.d/init.d,sysconfig}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install dbmail.conf $RPM_BUILD_ROOT%{_sysconfdir}
install contrib/mailbox2dbmail/mailbox2dbmail $RPM_BUILD_ROOT%{_bindir}
install contrib/mailbox2dbmail/mailbox2dbmail.1 $RPM_BUILD_ROOT%{_mandir}/man1
for initscript in %{SOURCE1} %{SOURCE2} %{SOURCE3} ; do
	install $initscript $RPM_BUILD_ROOT/etc/rc.d/init.d/`basename $initscript .init`
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
%banner %{name} << EOF
Read %{_docdir}/%{name}-%{version}/*
files, create database, configure %{_sysconfdir}/dbmail.conf, the
SMTP server, and the cron job for dbmail-maintenance.
EOF

%post imapd
/sbin/chkconfig --add dbmail-imapd
%service dbmail-imapd restart

%preun imapd
if [ "$1" = "0" ]; then
	%service -q dbmail-imapd stop
	/sbin/chkconfig --del dbmail-imapd
fi

%post lmtpd
/sbin/chkconfig --add dbmail-lmtpd
%service dbmail-lmtpd restart

%preun lmtpd
if [ "$1" = "0" ]; then
	%service -q dbmail-lmtpd stop
	/sbin/chkconfig --del dbmail-lmtpd
fi

%post pop3d
/sbin/chkconfig --add dbmail-pop3d
%service dbmail-pop3d restart

%preun pop3d
if [ "$1" = "0" ]; then
	%service -q dbmail-pop3d stop
	/sbin/chkconfig --del dbmail-pop3d
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog README* THANKS sql
%attr(755,root,root) %{_sbindir}/dbmail-export
#%%attr(755,root,root) %{_sbindir}/dbmail-sievecmd
%attr(755,root,root) %{_sbindir}/dbmail-smtp
%attr(755,root,root) %{_sbindir}/dbmail-users
%attr(755,root,root) %{_sbindir}/dbmail-util
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/%{name}/lib*.so.*
%attr(755,root,root) %{_libdir}/%{name}/lib*.so
%{_libdir}/%{name}/lib*.la
# -devel? but headers?
#%{_libdir}/*.a
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%{_mandir}/man[15]/dbmail*
%{_mandir}/man8/dbmail-export.8*
%{_mandir}/man8/dbmail-sievecmd.8*
%{_mandir}/man8/dbmail-timsieved.8*
%{_mandir}/man8/dbmail-users.8*
%{_mandir}/man8/dbmail-util.8*

%files imapd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/dbmail-imapd
%attr(754,root,root) /etc/rc.d/init.d/dbmail-imapd
%{_mandir}/man8/dbmail-imapd*

%files lmtpd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/dbmail-lmtpd
%attr(754,root,root) /etc/rc.d/init.d/dbmail-lmtpd
%{_mandir}/man8/dbmail-lmtpd*

%files pop3d
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/dbmail-pop3d
%attr(754,root,root) /etc/rc.d/init.d/dbmail-pop3d
%{_mandir}/man8/dbmail-pop3d*

%files mailbox2dbmail
%defattr(644,root,root,755)
%doc contrib/mailbox2dbmail/README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/mailbox2dbmail*

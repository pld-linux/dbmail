# TODO:
#   - bcond for mysql
#   - add separate user/group
#   - add subpackages and init / rc-inetd scripts
#     for dbmail-{pop3,imap,lmtpd}
#   - add cronjob for dbmail-maintenance
Summary:	Collection of programs for storing and retrieving mail from a SQL database
Summary(pl):	Zestaw program�w do zapisywania i odtwarzania poczty z bazy danych SQL
Name:		dbmail
Version:	2.0.1
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://dbmail.org/download/%{name}-%{version}.tgz
# Source0-md5:	9499c25c977e44777364a9696d8b1b48
URL:		http://www.dbman.org/
BuildRequires:	postgresql-devel
Requires:	postgresql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DBMAIL is a collection of programs that enables email to be stored in
and retrieved from a database.

Why is it usefull?
==================
Well, for me it's usefull because a number of reasons.
- It enables me to create mailboxes without the need of system users.
- Mail is more effeciently stored and therefore it can be inserted
  an retrieved much faster than any regular system (DBmail is
  currently able to retrieve aprox. 250 mail messages per second).
- It's more expandable. A database is much easier to access than
  a flat file or a Maildir. We don't need to parse first.
- In my case, I can easily link a mailbox to a certain client
  which enables me to let the client maintaining his/her own mailboxes
  without me needing to technically support it.
- It's scalable. You can run the dbmail programs on different servers
  talking to the same database (cluster).
- It is more secure. There's no need to maintain system users or write
  to the filesystem. All this is done through the database.

%description -l pl
DBMAIL to zestaw program�w umo�liwiaj�cych zapisywanie i odtwarzanie
poczty z bazy danych.

Dlaczego jest to u�yteczne? Dla autora jest z kilku powod�w:
- Umo�liwia tworzenie skrzynek bez wymagania u�ytkownik�w systemowych.
- Poczta jest zapisywana bardziej wydajnie i mo�e by� umieszczana oraz
  odtwarzana du�o szybciej ni� w normalnych systemach (DBmail
  aktualnie jest w stanie odczytywa� oko�o 250 list�w na sekund�).
- Jest bardziej rozszerzalne. Dost�p do bazy danych jest �atwiejszy
  ni� do p�askiego pliku lub Maildira. Nie trzeba ich najpierw
  analizowa�.
- W przypadku autora - mo�e on �atwo pod��czy� skrzynk� do pewnego
  klienta umo�liwiaj�c utrzymywanie skrzynek przez klienta bez
  potrzeby technicznego wsparcia administratora.
- Jest skalowalne. Mo�na uruchamia� programy dbmail na r�nych
  serwerach komunikuj�cych si� z t� sam� baz� danych (klastrem).
- Jest bardziej bezpieczne. Nie trzeba utrzymywa� u�ytkownik�w
  systemowych ani pisa� po systemie plik�w. Wszystkie jest wykonywane
  w bazie danych.

%package mailbox2dbmail
Summary:	Copy mail from an mbox file, maildir or mhdir directory to dbmail
Summary(pl):	Kopiowanie poczty z pliku mbox, katalogu maildir lub mhdir do dbmaila
# FIXME: better group
Group:		Applications/Mail
Requires:	%{name} = %{version}-%{release}
Requires:	python-modules >= 2.2

%description mailbox2dbmail
Use this program to copy mail from an mbox file, maildir or mhdir
directory to dbmail. This program uses ./dbmail-smtp for injecting
the emails into DBMail.

 %description mailbox2dbmail -l pl
Tego programu mo�na u�ywa� do kopiowania poczty z pliku mbox albo
katalogu maildir lub mhdir do dbmaila. U�ywa on ./dbmail-smtp do
umieszczania list�w w bazie DBMail.

%prep
%setup -q

%build
%configure2_13 \
	--with-pgsql
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D dbmail.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbmail.conf
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp man/* $RPM_BUILD_ROOT%{_mandir}/man1
install contrib/mailbox2dbmail/mailbox2dbmail $RPM_BUILD_ROOT%{_bindir}
install contrib/mailbox2dbmail/mailbox2dbmail.1 $RPM_BUILD_ROOT%{_mandir}/man1
install dbmail-* $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "    *****"
echo "  Read /usr/share/doc/%{name}-%{version}-%{release}/INSTALL*"
echo "  files, create database, configure /etc/dbmail.conf, the"
echo "  SMTP server, and the cron job for dbmail-maintenance."
echo
echo "  This package doesn't provide any init scripts; you'll have"
echo "  to deal with starting the appropiate daemons yourself."
echo "    *****"

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO EXTRAS BUGS INSTALL* sql
%attr(755,root,root) %{_bindir}/dbmail-*
# -devel? but headers?
#%{_libdir}/*.a
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%{_mandir}/man1/dbmail-*

%files mailbox2dbmail
%defattr(644,root,root,755)
%doc contrib/mailbox2dbmail/README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/mailbox2dbmail*

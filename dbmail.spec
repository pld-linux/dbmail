# TODO: bcond for mysql
Summary:	Collection of programs for storing and retrieving mail from a SQL database
#Summary(pl):	
Name:		dbmail
Version:	2.0
%define _rc	rc5
Release:	0.%{_rc}.3
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://dbmail.org/tgz/%{name}-%{version}%{_rc}.tgz
# Source0-md5:	f3cca8eb615af565a388069c1ab68f08
URL:		http://www.dbman.org/
BuildRequires:	postgresql-devel
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
Requires:	postgresql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DBMAIL is a collection of programs that enables email to be
stored in and retrieved from a database.

Why is it usefull?
==================
Well, for me it's usefull because a number of reasons.
- it enables me to create mailboxes without the need of systemusers.
- mail is more effeciently stored and therefore it can be inserted
  an retrieved much faster dan any regular system (DBmail is currently
  able to retrieve aprox. 250 mail messages per second)
- it's more expandable. A database is much easier to access than
  a flat file or a Maildir. We don't need to parse first.
- In my case, i can easily link a mailbox to a certain client
  which enables me to let the client maintaining his/her own mailboxes
  without me needing to technically support it.
- It's scalable. You can run the dbmail programs on different servers
  talking to the same database(cluster).
- It is more secure. There's no need to maintain system users or write
  to the filesystem. All this is done through the database.

# %description -l pl
# TODO

%package mailbox2dbmail
Summary:	Copy mail from an mbox file, maildir or mhdir directory to dbmail
#Summary(pl):	
# FIXME: better group
Group:		Applications/Mail
Requires:	python-modules >= 2.2

%description mailbox2dbmail
Use this program to copy mail from an mbox file, maildir or mhdir
directory to dbmail.  This program uses ./dbmail-smtp for injecting
the emails into DBMail.

# %description mailbox2dbmail -l pl
# TODO

%prep
%setup -q -n %{name}-%{version}%{_rc}

%build
# if ac/am/* rebuilding is necessary, do it in this order and add
# appropriate BuildRequires
#%%{__gettextize}
#%%{__aclocal}
#%%{__autoconf}
#%%{__autoheader}
#%%{__automake}
%configure2_13 \
	--with-pgsql
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D dbmail.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbmail.conf
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp man/*   $RPM_BUILD_ROOT%{_mandir}/man1
install contrib/mailbox2dbmail/mailbox2dbmail   $RPM_BUILD_ROOT%{_bindir}
install contrib/mailbox2dbmail/mailbox2dbmail.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO EXTRAS BUGS INSTALL* sql
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*.a
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%{_mandir}/man1/dbmail-*

%files mailbox2dbmail
%defattr(644,root,root,755)
%doc contrib/mailbox2dbmail/README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/mailbox2dbmail*

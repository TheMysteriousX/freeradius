# FIXME: should pki certs be moved to /etc/pki?
# FIXME: are the group names right?
# FIXME: need to run rpmlint
# FIXME: edit radrelay init.d script, was copied from radiusd init
# FIXME: check each former patch, do we still need any?
Summary: High-performance and highly configurable free RADIUS server
Name: freeradius
Version: 2.0.2
Release: 1%{?dist}
License: GPLv2+ and LGPLv2+
Group: System Environment/Daemons
URL: http://www.freeradius.org/

Source0: ftp://ftp.freeradius.org/pub/radius/%{name}-server-%{version}.tar.bz2
Source100: freeradius-radiusd.init
Source101: freeradius-radrelay.init
Source102: freeradius-logrotate
Source103: freeradius-pam-conf

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf
BuildRequires: gdbm-devel
BuildRequires: libtool
BuildRequires: libtool-ltdl-devel
BuildRequires: net-snmp-devel
BuildRequires: net-snmp-utils
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: zlib-devel

Requires: net-snmp
Requires: net-snmp-utils
Requires(pre): shadow-utils
Requires(post): /sbin/ldconfig /sbin/chkconfig
Requires(postun): /sbin/ldconfig
Requires(preun): /sbin/chkconfig

%description
The FreeRADIUS Server Project is a high performance and highly configurable 
GPL'd free RADIUS server. The server is similar in some respects to 
Livingston's 2.0 server.  While FreeRADIUS started as a variant of the 
Cistron RADIUS server, they don't share a lot in common any more. It now has 
many more features than Cistron or Livingston, and is much more configurable.

FreeRADIUS is an Internet authentication daemon, which implements the RADIUS 
protocol, as defined in RFC 2865 (and others). It allows Network Access 
Servers (NAS boxes) to perform authentication for dial-up users. There are 
also RADIUS clients available for Web servers, firewalls, Unix logins, and 
more.  Using RADIUS allows authentication and authorization for a network to 
be centralized, and minimizes the amount of re-configuration which has to be 
done when adding or deleting new users.

%package libs
Group:        Productivity/Networking/Radius/Servers
Summary:      FreeRADIUS share library

%description libs
The FreeRADIUS shared library

%package utils
Group:        Productivity/Networking/Radius/Clients
Summary:      FreeRADIUS Clients
Requires:     %{name}-libs = %{version}

%description utils
The FreeRADIUS server has a number of features found in other servers,
and additional features not found in any other server. Rather than
doing a feature by feature comparison, we will simply list the features
of the server, and let you decide if they satisfy your needs.

Support for RFC and VSA Attributes Additional server configuration
attributes Selecting a particular configuration Authentication methods

%package dialupadmin
Group:		Productivity/Networking/Radius/Servers
Summary:	Web management for FreeRADIUS
Requires:	http_daemon
Requires:	perl-DateManip
%if 0%{?suse_version} > 1000
Requires:	apache2-mod_php5
Requires:	php5
Requires:	php5-ldap
Requires:	php5-mysql
Requires:	php5-pgsql
%else
Requires:	apache2-mod_php4
Requires:	php4
Requires:	php4-ldap
Requires:	php4-mysql
Requires:	php4-pgsql
Requires:	php4-session
%endif
Autoreqprov:	off

%description dialupadmin
Dialup Admin supports users either in SQL (MySQL or PostgreSQL are
supported) or in LDAP. Apart from the web pages, it also includes a
number of scripts to make the administrator's life a lot easier.


%package devel
Group:        Development/Libraries/C and C++
Summary:      FreeRADIUS Development Files (static libs)
Autoreqprov:  off
Requires:     %{name}-libs = %{version}

%description devel
These are the static libraries for the FreeRADIUS package.


%package ldap
Summary: LDAP bindings for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: openldap
BuildRequires: openldap-devel

%description ldap
This plugin provides the LDAP bindings for the FreeRADIUS server project.

%package krb5
Summary: Kerberos 5 bindings for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: krb5-libs
BuildRequires: krb5-devel

%description krb5
This plugin provides the Kerberos 5 bindings for the FreeRADIUS server project.

%package perl
Summary: Perl bindings for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: perl-libs
BuildRequires: perl-devel

%description perl
This plugin provides the Perl bindings for the FreeRADIUS server project.

%package python
Summary: Python bindings for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: python-libs
BuildRequires: python-devel

%description python
This plugin provides the Python bindings for the FreeRADIUS server project.

%package mysql
Summary: MySQL bindings for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: mysql
BuildRequires: mysql-devel

%description mysql
This plugin provides the MySQL bindings for the FreeRADIUS server project.

%package postgresql
Summary: postgresql bindings for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: postgresql
BuildRequires: postgresql-devel

%description postgresql
This plugin provides the postgresql bindings for the FreeRADIUS server project.

%package unixODBC
Summary: unixODBC bindings for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: unixODBC
BuildRequires: unixODBC-devel

%description unixODBC
This plugin provides the unixODBC bindings for the FreeRADIUS server project.


%prep
%setup -q -n %{name}-server-%{version}

%build
%ifarch s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif

# bad fix for libtool: clear buildroot early, set LDFLAGS to buildroot libdir
rm -rf $RPM_BUILD_ROOT
export LDFLAGS="-L${RPM_BUILD_ROOT}%{_libdir}"

%configure \
	--libdir=%{_libdir}/freeradius \
	--with-gnu-ld \
	--with-threads \
	--with-thread-pool \
 	--disable-ltdl-install \
	--with-docdir=%{_docdir}/freeradius-%{version} \
	--with-rlm-sql_postgresql-include-dir=/usr/include/pgsql \
	--with-rlm-sql-postgresql-lib-dir=%{_libdir} \
	--with-rlm-sql_mysql-include-dir=/usr/include/mysql \
	--with-mysql-lib-dir=%{_libdir}/mysql \
	--with-unixodbc-lib-dir=%{_libdir} \
	--with-rlm-dbm-lib-dir=%{_libdir} \
	--with-rlm-krb5-include-dir=/usr/kerberos/include \
	--without-rlm_eap_ikev2 \
	--without-rlm_sql_iodbc \
	--without-rlm_sql_firebird \
	--without-rlm_sql_db2 \
	--without-rlm_sql_oracle

%if "%{_lib}" == "lib64"
perl -pi -e 's:sys_lib_search_path_spec=.*:sys_lib_search_path_spec="/lib64 /usr/lib64 /usr/local/lib64":' libtool
%endif

make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/run/radiusd
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/{logrotate.d,pam.d,rc.d/init.d}
mkdir -p $RPM_BUILD_ROOT/var/lib/radiusd
# fix for bad libtool bug - can not rebuild dependent libs and bins
#FIXME export LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}
make install R=$RPM_BUILD_ROOT
# modify default configuration
RADDB=$RPM_BUILD_ROOT%{_sysconfdir}/raddb
perl -i -pe 's/^#user =.*$/user = radiusd/'   $RADDB/radiusd.conf
perl -i -pe 's/^#group =.*$/group = radiusd/' $RADDB/radiusd.conf
perl -i -pe 's/^#user =.*$/user = radiusd/'   $RADDB/radrelay.conf
perl -i -pe 's/^#group =.*$/group = radiusd/' $RADDB/radrelay.conf
#ldconfig -n $RPM_BUILD_ROOT/usr/lib/freeradius
# logs
mkdir -p $RPM_BUILD_ROOT/var/log/radius/radacct
touch $RPM_BUILD_ROOT/var/log/radius/{radutmp,radius.log}

install -m 755 %{SOURCE100} $RPM_BUILD_ROOT/%{_initrddir}/radiusd
install -m 755 %{SOURCE101} $RPM_BUILD_ROOT/%{_initrddir}/radrelay
install -m 644 %{SOURCE102} $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/radiusd
install -m 644 %{SOURCE103} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/radiusd

(cd $RPM_BUILD_ROOT/usr/sbin && ln -sf ./radiusd radrelay)
# install dialup_admin
DIALUPADMIN=$RPM_BUILD_ROOT%{_datadir}/dialup_admin
mkdir -p $DIALUPADMIN
cp -r dialup_admin/* $RPM_BUILD_ROOT%{_datadir}/dialup_admin
perl -i -pe 's/^#general_base_dir\:.*$/general_base_dir\: \/usr\/share\/freeradius-dialupadmin/'   $DIALUPADMIN/conf/admin.conf
perl -i -pe 's/^#general_radiusd_base_dir\:.*$/general_radiusd_base_dir\: \//'   $DIALUPADMIN/conf/admin.conf
perl -i -pe 's/^#general_snmpwalk_command\:.*$/general_snmpwalk_command\: \/usr\/bin\/snmpwalk/'   $DIALUPADMIN/conf/admin.conf
perl -i -pe 's/^#general_snmpget_command\:.*$/general_snmpget_command\: \/usr\/bin\/snmpget/'   $DIALUPADMIN/conf/admin.conf
# httpd config
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 suse/admin-httpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/radius.conf
# remove unneeded stuff
rm -rf doc/00-OLD
rm -f $RPM_BUILD_ROOT/usr/sbin/rc.radiusd
rm -rf $RPM_BUILD_ROOT/%{_libdir}/freeradius/*.a
rm -rf $RPM_BUILD_ROOT/%{_libdir}/freeradius/*.la
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/sql/oracle

# remove unsupported config files
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/experimental.conf


%clean
rm -rf $RPM_BUILD_ROOT


%pre
/usr/sbin/useradd -M -o -r -d / -u 95 -c "radiusd user" -s /bin/false radiusd > /dev/null 2>&1 || :


%post
/bin/chown -R radiusd.radiusd %{_sysconfdir}/raddb
/sbin/ldconfig
if [ $1 = 1 ]; then
  /sbin/chkconfig --add radiusd
fi

%preun
if [ $1 = 0 ]; then
  /sbin/service radiusd stop > /dev/null 2>&1
  /sbin/chkconfig --del radiusd
fi


%postun
if [ $1 -ge 1 ]; then
  /sbin/service radiusd condrestart >/dev/null 2>&1 || :
fi
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc %{_docdir}/freeradius-%{version}/
%config(noreplace) %{_sysconfdir}/pam.d/radiusd
%config(noreplace) %{_sysconfdir}/logrotate.d/radiusd
%config(noreplace) %{_initrddir}/radiusd
%config(noreplace) %{_initrddir}/radrelay
%dir %attr(755,radiusd,radiusd) /var/lib/radiusd
# configs
%dir %attr(750,-,radiusd) /etc/raddb
%defattr(-,root,radiusd)
%config(noreplace) /etc/raddb/dictionary
%config(noreplace) /etc/raddb/acct_users
%config(noreplace) /etc/raddb/attrs
%config(noreplace) /etc/raddb/attrs.access_reject
%config(noreplace) /etc/raddb/attrs.accounting_response
%config(noreplace) /etc/raddb/attrs.pre-proxy
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/clients.conf
%config(noreplace) /etc/raddb/hints
%config(noreplace) /etc/raddb/huntgroups
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/sqlippool.conf
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/preproxy_users
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/proxy.conf
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/radiusd.conf
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/snmp.conf
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/sql.conf
#%attr(640,-,radiusd) %config(noreplace) /etc/raddb/radrelay.conf
#%attr(640,-,radiusd) %config(noreplace) /etc/raddb/vmpsd.conf
%dir %attr(640,-,radiusd) /etc/raddb/sql
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/sql/mssql/*
#%attr(640,-,radiusd) %config(noreplace) /etc/raddb/sql/oracle/*
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/users
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/otp.conf
%dir %attr(750,-,radiusd) /etc/raddb/certs
/etc/raddb/certs/Makefile
/etc/raddb/certs/README
/etc/raddb/certs/xpextensions
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/certs/*.cnf
%attr(750,-,radiusd) /etc/raddb/certs/bootstrap
%attr(640,-,radiusd) /etc/raddb/sites-available/*
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/sites-enabled/*
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/eap.conf
%attr(640,-,radiusd) /etc/raddb/example.pl
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/policy.conf
/etc/raddb/policy.txt
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/templates.conf
%attr(700,radiusd,radiusd) %dir /var/run/radiusd/
# binaries
%defattr(-,root,root)
/usr/sbin/check-radiusd-config
/usr/sbin/checkrad
/usr/sbin/radiusd
/usr/sbin/radrelay
/usr/sbin/radwatch
# man-pages
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%doc %{_mandir}/man8/*
# dictionaries
%attr(755,root,root) %dir /usr/share/freeradius
/usr/share/freeradius/*
# logs
%attr(700,radiusd,radiusd) %dir /var/log/radius/
%attr(700,radiusd,radiusd) %dir /var/log/radius/radacct/
%attr(644,radiusd,radiusd) /var/log/radius/radutmp
%config(noreplace) %attr(600,radiusd,radiusd) /var/log/radius/radius.log
# RADIUS Loadable Modules
%attr(755,root,root) %dir %{_libdir}/freeradius
#%attr(755,root,root) %{_libdir}/freeradius/rlm_*.so*
#%{_libdir}/freeradius/rlm_acctlog*.so
%{_libdir}/freeradius/rlm_acct_unique.so
%{_libdir}/freeradius/rlm_acct_unique-%{version}.so
%{_libdir}/freeradius/rlm_acctlog.so
%{_libdir}/freeradius/rlm_acctlog-%{version}.so
%{_libdir}/freeradius/rlm_always.so
%{_libdir}/freeradius/rlm_always-%{version}.so
%{_libdir}/freeradius/rlm_attr_filter.so
%{_libdir}/freeradius/rlm_attr_filter-%{version}.so
%{_libdir}/freeradius/rlm_attr_rewrite.so
%{_libdir}/freeradius/rlm_attr_rewrite-%{version}.so
%{_libdir}/freeradius/rlm_chap.so
%{_libdir}/freeradius/rlm_chap-%{version}.so
%{_libdir}/freeradius/rlm_checkval.so
%{_libdir}/freeradius/rlm_checkval-%{version}.so
%{_libdir}/freeradius/rlm_copy_packet.so
%{_libdir}/freeradius/rlm_copy_packet-%{version}.so
%{_libdir}/freeradius/rlm_counter.so
%{_libdir}/freeradius/rlm_counter-%{version}.so
%{_libdir}/freeradius/rlm_dbm.so
%{_libdir}/freeradius/rlm_dbm-%{version}.so
%{_libdir}/freeradius/rlm_detail.so
%{_libdir}/freeradius/rlm_detail-%{version}.so
%{_libdir}/freeradius/rlm_digest.so
%{_libdir}/freeradius/rlm_digest-%{version}.so
%{_libdir}/freeradius/rlm_eap.so
%{_libdir}/freeradius/rlm_eap-%{version}.so
%{_libdir}/freeradius/rlm_eap_gtc.so
%{_libdir}/freeradius/rlm_eap_gtc-%{version}.so
%{_libdir}/freeradius/rlm_eap_leap.so
%{_libdir}/freeradius/rlm_eap_leap-%{version}.so
%{_libdir}/freeradius/rlm_eap_md5.so
%{_libdir}/freeradius/rlm_eap_md5-%{version}.so
%{_libdir}/freeradius/rlm_eap_mschapv2.so
%{_libdir}/freeradius/rlm_eap_mschapv2-%{version}.so
%{_libdir}/freeradius/rlm_eap_peap.so
%{_libdir}/freeradius/rlm_eap_peap-%{version}.so
%{_libdir}/freeradius/rlm_eap_sim.so
%{_libdir}/freeradius/rlm_eap_sim-%{version}.so
%{_libdir}/freeradius/rlm_eap_tls.so
%{_libdir}/freeradius/rlm_eap_tls-%{version}.so
%{_libdir}/freeradius/rlm_eap_tnc.so
%{_libdir}/freeradius/rlm_eap_tnc-%{version}.so
%{_libdir}/freeradius/rlm_eap_ttls.so
%{_libdir}/freeradius/rlm_eap_ttls-%{version}.so
%{_libdir}/freeradius/rlm_exec.so
%{_libdir}/freeradius/rlm_exec-%{version}.so
%{_libdir}/freeradius/rlm_expiration.so
%{_libdir}/freeradius/rlm_expiration-%{version}.so
%{_libdir}/freeradius/rlm_expr.so
%{_libdir}/freeradius/rlm_expr-%{version}.so
%{_libdir}/freeradius/rlm_fastusers.so
%{_libdir}/freeradius/rlm_fastusers-%{version}.so
%{_libdir}/freeradius/rlm_files.so
%{_libdir}/freeradius/rlm_files-%{version}.so
%{_libdir}/freeradius/rlm_ippool.so
%{_libdir}/freeradius/rlm_ippool-%{version}.so
%{_libdir}/freeradius/rlm_logintime.so
%{_libdir}/freeradius/rlm_logintime-%{version}.so
%{_libdir}/freeradius/rlm_mschap.so
%{_libdir}/freeradius/rlm_mschap-%{version}.so
%{_libdir}/freeradius/rlm_otp.so
%{_libdir}/freeradius/rlm_otp-%{version}.so
%{_libdir}/freeradius/rlm_pam.so
%{_libdir}/freeradius/rlm_pam-%{version}.so
%{_libdir}/freeradius/rlm_pap.so
%{_libdir}/freeradius/rlm_pap-%{version}.so
%{_libdir}/freeradius/rlm_passwd.so
%{_libdir}/freeradius/rlm_passwd-%{version}.so
%{_libdir}/freeradius/rlm_policy.so
%{_libdir}/freeradius/rlm_policy-%{version}.so
%{_libdir}/freeradius/rlm_preprocess.so
%{_libdir}/freeradius/rlm_preprocess-%{version}.so
%{_libdir}/freeradius/rlm_radutmp.so
%{_libdir}/freeradius/rlm_radutmp-%{version}.so
%{_libdir}/freeradius/rlm_realm.so
%{_libdir}/freeradius/rlm_realm-%{version}.so
%{_libdir}/freeradius/rlm_sql.so
%{_libdir}/freeradius/rlm_sql-%{version}.so
%{_libdir}/freeradius/rlm_sql_log.so
%{_libdir}/freeradius/rlm_sql_log-%{version}.so
%{_libdir}/freeradius/rlm_sqlcounter.so
%{_libdir}/freeradius/rlm_sqlcounter-%{version}.so
%{_libdir}/freeradius/rlm_sqlippool.so
%{_libdir}/freeradius/rlm_sqlippool-%{version}.so
%{_libdir}/freeradius/rlm_unix.so
%{_libdir}/freeradius/rlm_unix-%{version}.so

%files utils
/usr/bin/*

%files libs
# RADIU shared libs
%attr(755,root,root) %dir %{_libdir}/freeradius
%attr(755,root,root) %{_libdir}/freeradius/lib*.so*

%files dialupadmin
%defattr(-,root,root)
%dir %{_datadir}/dialup_admin/
%{_datadir}/dialup_admin/Makefile
%{_datadir}/dialup_admin/bin/
%{_datadir}/dialup_admin/doc/
%{_datadir}/dialup_admin/htdocs/
%{_datadir}/dialup_admin/html/
%{_datadir}/dialup_admin/lib/
%{_datadir}/dialup_admin/sql/
%dir %{_datadir}/dialup_admin/conf/
%config(noreplace) %{_datadir}/dialup_admin/conf/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/radius.conf
%{_datadir}/dialup_admin/Changelog
%{_datadir}/dialup_admin/README

%files devel
%defattr(-,root,root)
#%attr(644,root,root) %{_libdir}/freeradius/*.a
#%attr(644,root,root) %{_libdir}/freeradius/*.la
%attr(644,root,root) /usr/include/freeradius/*.h

%files ldap
%defattr(-,root,root,-)
%config(noreplace) /etc/raddb/ldap.attrmap
%{_libdir}/freeradius/rlm_ldap.so
%{_libdir}/freeradius/rlm_ldap-%{version}.so

%files krb5
%defattr(-,root,root,-)
%{_libdir}/freeradius/rlm_krb5.so
%{_libdir}/freeradius/rlm_krb5-%{version}.so

%files perl
%defattr(-,root,root,-)
%{_libdir}/freeradius/rlm_perl.so
%{_libdir}/freeradius/rlm_perl-%{version}.so

%files python
%defattr(-,root,root,-)
%{_libdir}/freeradius/rlm_python.so
%{_libdir}/freeradius/rlm_python-%{version}.so

%files mysql
%defattr(-,root,root,-)
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/sql/mysql/*
%{_libdir}/freeradius/rlm_sql_mysql.so
%{_libdir}/freeradius/rlm_sql_mysql-%{version}.so

%files postgresql
%defattr(-,root,root,-)
%attr(640,-,radiusd) %config(noreplace) /etc/raddb/sql/postgresql/*
%{_libdir}/freeradius/rlm_sql_postgresql.so
%{_libdir}/freeradius/rlm_sql_postgresql-%{version}.so

%files unixODBC
%defattr(-,root,root,-)
%{_libdir}/freeradius/rlm_sql_unixodbc.so
%{_libdir}/freeradius/rlm_sql_unixodbc-%{version}.so

%changelog
* Thu Feb 28 2008  <jdennis@redhat.com> - 2.0.2-1
- upgrade to new 2.0 release
- split into subpackages for more fine grained installation

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.7-4.4.ipa
- Autorebuild for GCC 4.3

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.1.7-3.4.ipa
- Rebuild for deps

* Sat Nov 10 2007  <jdennis@redhat.com> - 1.1.7-3.3.ipa
- add support in rlm_ldap for reading clients from ldap
- fix TLS parameter controling if a cert which fails to validate
  will be accepted (i.e. self-signed),
  rlm_ldap config parameter=tls_require_cert
  ldap LDAP_OPT_X_TLS_REQUIRE_CERT parameter was being passed to
  ldap_set_option() when it should have been ldap_int_tls_config()

* Sat Nov 3 2007  <jdennis@redhat.com> - 1.1.7-3.2.ipa
- add support in rlm_ldap for SASL/GSSAPI binds to the LDAP server

* Mon Sep 17 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-3.1
- made init script fully lsb conform

* Mon Sep 17 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-3
- fixed initscript problem (rhbz#292521)

* Tue Aug 28 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-2
- fixed initscript for LSB (rhbz#243671, rhbz#243928)
- fixed license tag

* Tue Aug  7 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-1
- new versin 1.1.7
- install snmp MIB files
- dropped LDAP_DEPRECATED flag, it is upstream
- marked config files for sub packages as config (rhbz#240400)
- moved db files to /var/lib/raddb (rhbz#199082)

* Fri Jun 15 2007 Thomas Woerner <twoerner@redhat.com> 1.1.6-2
- radiusd expects /etc/raddb to not be world readable or writable
  /etc/raddb now belongs to radiusd, post script sets permissions

* Fri Jun 15 2007 Thomas Woerner <twoerner@redhat.com> 1.1.6-1
- new version 1.1.6

* Fri Mar  9 2007 Thomas Woerner <twoerner@redhat.com> 1.1.5-1
- new version 1.1.5
  - no /etc/raddb/otppasswd.sample anymore
  - build is pie by default, dropped pie patch
- fixed build requirement for perl (perl-devel)

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 1.1.3-3
- remove trailing dot from summary
- fix buildroot
- fix post/postun/preun requirements
- use rpm macros

* Fri Dec  8 2006 Thomas Woerner <twoerner@redhat.com> 1.1.3-2.1
- rebuild for new postgresql library version

* Thu Nov 30 2006 Thomas Woerner <twoerner@redhat.com> 1.1.3-2
- fixed ldap code to not use internals, added LDAP_DEPRECATED compile time flag
  (#210912)

* Tue Aug 15 2006 Thomas Woerner <twoerner@redhat.com> 1.1.3-1
- new version 1.1.3 with lots of upstream bug fixes, some security fixes
  (#205654)

* Tue Aug 15 2006 Thomas Woerner <twoerner@redhat.com> 1.1.2-2
- commented out include for sql.conf in radiusd.conf (#202561)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.1.2-1.1
- rebuild

* Thu Jun  1 2006 Thomas Woerner <twoerner@redhat.com> 1.1.2-1
- new version 1.1.2

* Wed May 31 2006 Thomas Woerner <twoerner@redhat.com> 1.1.1-1
- new version 1.1.1
- fixed incorrect rlm_sql globbing (#189095)
  Thanks to Yanko Kaneti for the fix.
- fixed chown syntax in post script (#182777)
- dropped gcc34, libdir and realloc-return patch
- spec file cleanup with additional libtool build fixes

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 13 2005 Thomas Woerner <twoerner@redhat.com> 1.0.5-1
- new version 1.0.5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> - 1.0.4-5
- Rebuild due to mysql update.

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> - 1.0.4-4
- rebuilt with new openssl
- fixed ignored return value of realloc

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com> - 1.0.4-3
- use include instead of pam_stack in pam config

* Wed Jul 20 2005 Thomas Woerner <twoerner@redhat.com> 1.0.4-2
- added missing build requires for libtool-ltdl-devel (#160877)
- modified file list to get a report for missing plugins

* Tue Jun 28 2005 Thomas Woerner <twoerner@redhat.com> 1.0.4-1
- new version 1.0.4
- droppend radrelay patch (fixed upstream)

* Thu Apr 14 2005 Warren Togami <wtogami@redhat.com> 1.0.2-2
- rebuild against new postgresql-libs

* Mon Apr  4 2005 Thomas Woerner <twoerner@redhat.com> 1.0.2-1
- new version 1.0.2

* Fri Nov 19 2004 Thomas Woerner <twoerner@redhat.com> 1.0.1-3
- rebuild for MySQL 4
- switched over to installed libtool

* Fri Nov  5 2004 Thomas Woerner <twoerner@redhat.com> 1.0.1-2
- Fixed install problem of radeapclient (#138069)

* Wed Oct  6 2004 Thomas Woerner <twoerner@redhat.com> 1.0.1-1
- new version 1.0.1
- applied radrelay CVS patch from Kevin Bonner

* Wed Aug 25 2004 Warren Togami <wtogami@redhat.com> 1.0.0-3
- BuildRequires pam-devel and libtool
- Fix errant text in description
- Other minor cleanups

* Wed Aug 25 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-2.1
- renamed /etc/pam.d/radius to /etc/pam.d/radiusd to match default 
  configuration (#130613)

* Wed Aug 25 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-2
- fixed BuildRequires for openssl-devel (#130606)

* Mon Aug 16 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-1
- 1.0.0 final

* Mon Jul  5 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-0.pre3.2
- added buildrequires for zlib-devel (#127162)
- fixed libdir patch to prefer own libeap instead of installed one (#127168)
- fixed samba account maps in LDAP for samba v3 (#127173)

* Thu Jul  1 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-0.pre3.1
- third "pre" release of version 1.0.0
- rlm_ldap is using SASLv2 (#126507)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun  3 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-4.1
- fixed BuildRequires for gdbm-devel

* Tue Mar 30 2004 Harald Hoyer <harald@redhat.com> - 0.9.3-4
- gcc34 compilation fixes

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-3.2
- added sql scripts for rlm_sql to documentation (#116435)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb  5 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-2.1
- using -fPIC instead of -fpic for s390 ans s390x

* Thu Feb  5 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-2
- radiusd is pie, now

* Tue Nov 25 2003 Thomas Woerner <twoerner@redhat.com> 0.9.3-1
- new version 0.9.3 (bugfix release)

* Fri Nov  7 2003 Thomas Woerner <twoerner@redhat.com> 0.9.2-1
- new version 0.9.2

* Mon Sep 29 2003 Thomas Woerner <twoerner@redhat.com> 0.9.1-1
- new version 0.9.1

* Mon Sep 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.0-2.2
- modify default PAM configuration to remove the directory part of the module
  name, so that 32- and 64-bit libpam (called from 32- or 64-bit radiusd) on
  multilib systems will always load the right module for the architecture
- modify default PAM configuration to use pam_stack

* Mon Sep  1 2003 Thomas Woerner <twoerner@redhat.com> 0.9.0-2.1
- com_err.h moved to /usr/include/et

* Tue Jul 22 2003 Thomas Woerner <twoerner@redhat.com> 0.9.0-1
- 0.9.0 final

* Wed Jul 16 2003 Thomas Woerner <twoerner@redhat.com> 0.9.0-0.9.0
- new version 0.9.0 pre3

* Thu May 22 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-6
- included directory /var/log/radius/radacct for logrotate

* Wed May 21 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-5
- moved log and run dir to files section, cleaned up post

* Wed May 21 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-4
- added missing run dir in post

* Tue May 20 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-3
- fixed module load patch

* Fri May 16 2003 Thomas Woerner <twoerner@redhat.com>
- removed la files, removed devel package
- split into 4 packages: freeradius, freeradius-mysql, freeradius-postgresql,
    freeradius-unixODBC
- fixed requires and buildrequires
- create logging dir in post if it does not exist
- fixed module load without la files

* Thu Apr 17 2003 Thomas Woerner <twoerner@redhat.com> 
- Initial build.

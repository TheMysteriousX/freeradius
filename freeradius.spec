Summary: High-performance and highly configurable free RADIUS server
Name: freeradius
Version: 1.1.7
Release: 2%{?dist}
License: GPLv2+ and LGPLv2+
Group: System Environment/Daemons
URL: http://www.freeradius.org/
Source0: ftp://ftp.freeradius.org/pub/radius/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: net-snmp krb5-libs net-snmp-utils
BuildRequires: net-snmp-devel net-snmp-utils krb5-devel openldap-devel 
BuildRequires: openssl-devel pam-devel
BuildRequires: libtool-ltdl-devel libtool
BuildRequires: gdbm-devel zlib-devel
BuildRequires: perl-devel
Requires(pre): shadow-utils
Requires(post): /sbin/ldconfig /sbin/chkconfig
Requires(postun): /sbin/ldconfig
Requires(preun): /sbin/chkconfig
Patch1: freeradius-1.0.0-ltdl_no_la.patch
Patch3: freeradius-0.9.0-pam-multilib.patch
Patch4: freeradius-0.9.0-com_err.patch
Patch8: freeradius-1.0.0-samba3.patch
Patch10: freeradius-1.1.3-build.patch
Patch11: freeradius-1.1.2-no_sql_inc.patch
Patch12: freeradius-1.1.7-ldap.patch
Patch13: freeradius-1.1.7-db_dir.patch
Patch14: freeradius-1.1.7-lsb.patch

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
%setup -q 
%patch1 -p1 -b .ltdl_no_la
%patch3 -p1 -b .pam-multilib
%patch4 -p1 -b .com_err
%patch8 -p1 -b .samba3
%patch10 -p1 -b .build
%patch11 -p1 -b .no_sql_inc
%patch12 -p1 -b .ldap
%patch13 -p1 -b .db_dir
%patch14 -p1 -b .lsb


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
	--with-rlm-krb5-include-dir=/usr/kerberos/include

%if "%{_lib}" == "lib64"
perl -pi -e 's:sys_lib_search_path_spec=.*:sys_lib_search_path_spec="/lib64 /usr/lib64 /usr/local/lib64":' libtool
%endif

# Makefile not smp save
make #%{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/{logrotate.d,pam.d,rc.d/init.d}
# create database directory
mkdir -p $RPM_BUILD_ROOT/var/lib/radiusd

# fix for bad libtool bug - can not rebuild dependent libs and bins
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}
make install R=$RPM_BUILD_ROOT

RADDB=$RPM_BUILD_ROOT/%{_sysconfdir}/raddb
# set radiusd as default user/group
perl -i -pe 's/^#user =.*$/user = radiusd/' $RADDB/radiusd.conf
perl -i -pe 's/^#group =.*$/group = radiusd/' $RADDB/radiusd.conf
# shadow password file MUST be defined on Linux
perl -i -pe 's/#	shadow =/shadow =/' $RADDB/radiusd.conf

install -m 755 redhat/rc.radiusd-redhat $RPM_BUILD_ROOT/%{_initrddir}/radiusd
install -m 644 redhat/radiusd-logrotate $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/radiusd
install -m 644 redhat/radiusd-pam $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/radiusd

# install SNMP MIB files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/snmp/mibs/
install -m 644 mibs/RADIUS*.txt $RPM_BUILD_ROOT%{_datadir}/snmp/mibs/

# remove unwanted rc.radiusd
rm -f $RPM_BUILD_ROOT%{_prefix}/sbin/rc.radiusd

find $RPM_BUILD_ROOT%{_libdir} -name "*.la" -print | xargs rm -f
find $RPM_BUILD_ROOT%{_libdir} -name "*.a" -print | xargs rm -f

mkdir -p $RPM_BUILD_ROOT/var/log/radius
touch $RPM_BUILD_ROOT/var/log/radius/{radutmp,radwtmp,radius.log}
mkdir -p $RPM_BUILD_ROOT/var/log/radius/radacct
mkdir -p $RPM_BUILD_ROOT/var/run/radiusd

# remove unsupported config files
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/oraclesql.conf
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
for i in /var/log/radius/{radutmp,radwtmp,radius.log}; do
  /bin/touch $i && /bin/chown radiusd $i && /bin/chmod 600 $i
done


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
%dir %attr(0700,radiusd,radiusd) %{_sysconfdir}/raddb
%dir %attr(0700,radiusd,radiusd) %{_sysconfdir}/raddb/certs
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/acct_users
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/attrs
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/certs/*
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/clients
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/clients.conf
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/dictionary
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/eap.conf
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/example.pl
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/hints
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/huntgroups
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/ldap.attrmap
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/naslist
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/naspasswd
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/otp.conf
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/postgresqlippool.conf
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/preproxy_users
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/proxy.conf
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/radiusd.conf
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/realms
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/snmp.conf
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/sqlippool.conf
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/users
%{_bindir}/*
%{_libdir}/libeap*.so
%{_libdir}/libradius*.so
%{_libdir}/rlm_acct_unique*.so
%{_libdir}/rlm_always*.so
%{_libdir}/rlm_attr_filter*.so
%{_libdir}/rlm_attr_rewrite*.so
%{_libdir}/rlm_chap*.so
%{_libdir}/rlm_checkval*.so
%{_libdir}/rlm_counter*.so
%{_libdir}/rlm_dbm*.so
%{_libdir}/rlm_detail*.so
%{_libdir}/rlm_digest*.so
%{_libdir}/rlm_eap-*.so
%{_libdir}/rlm_eap.so
%{_libdir}/rlm_eap_gtc*.so
%{_libdir}/rlm_eap_leap*.so
%{_libdir}/rlm_eap_md5*.so
%{_libdir}/rlm_eap_mschapv2*.so
%{_libdir}/rlm_eap_peap*.so
%{_libdir}/rlm_eap_sim*.so
%{_libdir}/rlm_eap_tls*.so
%{_libdir}/rlm_eap_ttls*.so
%{_libdir}/rlm_exec*.so
%{_libdir}/rlm_expr*.so
%{_libdir}/rlm_fastusers*.so
%{_libdir}/rlm_files*.so
%{_libdir}/rlm_ippool*.so
%{_libdir}/rlm_krb5*.so
%{_libdir}/rlm_ldap*.so
%{_libdir}/rlm_mschap*.so
%{_libdir}/rlm_ns_mta_md5*.so
%{_libdir}/rlm_otp*.so
%{_libdir}/rlm_pam*.so
%{_libdir}/rlm_pap*.so
%{_libdir}/rlm_passwd*.so
%{_libdir}/rlm_perl*.so
%{_libdir}/rlm_preprocess*.so
%{_libdir}/rlm_radutmp*.so
%{_libdir}/rlm_realm*.so
%{_libdir}/rlm_sql-%{version}.so
%{_libdir}/rlm_sql.so
%{_libdir}/rlm_sqlcounter*.so
%{_libdir}/rlm_sqlippool*.so
%{_libdir}/rlm_sql_log*.so
%{_libdir}/rlm_unix*.so
%{_datadir}/freeradius
%{_datadir}/snmp/mibs/RADIUS*.txt
%{_sbindir}/*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*
%attr(0700,radiusd,radiusd) %dir /var/log/radius
%ghost %attr(0600,radiusd,radiusd) /var/log/radius/radutmp
%ghost %attr(0600,radiusd,radiusd) /var/log/radius/radwtmp
%ghost %attr(0600,radiusd,radiusd) /var/log/radius/radius.log
%attr(0700,radiusd,radiusd) %dir /var/log/radius/radacct
%attr(0700,radiusd,radiusd) %dir /var/run/radiusd
# use only for database files:
%attr(0700,radiusd,radiusd) %dir /var/lib/radiusd

%files mysql
%defattr(-,root,root,-)
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/sql.conf
%{_libdir}/*_mysql*.so

%files postgresql
%defattr(-,root,root,-)
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/postgresql.conf
%{_libdir}/*_postgresql*.so

%files unixODBC
%defattr(-,root,root,-)
%config(noreplace) %attr(0600,radiusd,radiusd) %{_sysconfdir}/raddb/mssql.conf
%{_libdir}/*_unixodbc*.so


%changelog
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

# -*- rpm-spec -*-

# This spec file assumes you are building for Fedora 13 or newer,
# or for RHEL 5 or newer. It may need some tweaks for other distros.
# If neither fedora nor rhel was defined, try to guess them from %{dist}
%if !0%{?rhel} && !0%{?fedora}
%{expand:%(echo "%{?dist}" | \
  sed -ne 's/^\.el\([0-9]\+\).*/%%define rhel \1/p')}
%{expand:%(echo "%{?dist}" | \
  sed -ne 's/^\.fc\?\([0-9]\+\).*/%%define fedora \1/p')}
%endif

# Default to skipping autoreconf.  Distros can change just this one line
# (or provide a command-line override) if they backport any patches that
# touch configure.ac or Makefile.am.
%{!?enable_autotools:%define enable_autotools 0}

# A client only build will create a libvirt.so only containing
# the generic RPC driver, and test driver and no libvirtd
# Default to a full server + client build, but with the possibility
# of a command-line or ~/.rpmmacros override for client-only.
%{!?client_only:%define client_only 0}

# Now turn off server build in certain cases

# RHEL-5 builds are client-only for s390, ppc
%if 0%{?rhel} == 5
    %ifnarch %{ix86} x86_64 ia64
        %define client_only        1
    %endif
%endif

# Disable all server side drivers if client only build requested
%if %{client_only}
    %define server_drivers     0
%else
    %define server_drivers     1
%endif

# Always build with dlopen'd modules
%define with_driver_modules 1

# Now set the defaults for all the important features, independent
# of any particular OS

# First the daemon itself
%define with_libvirtd      0%{!?_without_libvirtd:%{server_drivers}}
%define with_avahi         0%{!?_without_avahi:%{server_drivers}}

# Then the hypervisor drivers that run in libvirtd
%define with_xen           0%{!?_without_xen:%{server_drivers}}
%define with_qemu          0%{!?_without_qemu:%{server_drivers}}
%define with_lxc           0%{!?_without_lxc:%{server_drivers}}
%define with_uml           0%{!?_without_uml:%{server_drivers}}
%define with_libxl         0%{!?_without_libxl:%{server_drivers}}
%define with_vbox          0%{!?_without_vbox:%{server_drivers}}

%define with_qemu_tcg      %{with_qemu}

%define qemu_kvm_arches %{ix86} x86_64 aarch64

%if 0%{?fedora}
    %if 0%{?fedora} < 16
        # Fedora doesn't have any QEMU on ppc64 until FC16 - only ppc
        # I think F17 is the first release with the power64 macro
        %ifarch ppc64
            %define with_qemu_tcg 0
        %endif
    %endif
    %if 0%{?fedora} >= 18
        %define qemu_kvm_arches %{ix86} x86_64 %{power64} s390x
    %endif
    %if 0%{?fedora} >= 20
        %define qemu_kvm_arches %{ix86} x86_64 %{power64} s390x %{arm} aarch64
    %endif
%endif

%if 0%{?rhel}
    %define with_qemu_tcg 0
    %define qemu_kvm_arches x86_64
%endif

%ifarch %{qemu_kvm_arches}
    %define with_qemu_kvm      %{with_qemu}
%else
    %define with_qemu_kvm      0
%endif

%if ! %{with_qemu_tcg} && ! %{with_qemu_kvm}
    %define with_qemu 0
%endif

# Then the hypervisor drivers that run outside libvirtd, in libvirt.so
%define with_openvz        0%{!?_without_openvz:1}
%define with_vmware        0%{!?_without_vmware:1}
%define with_phyp          0%{!?_without_phyp:1}
%define with_esx           0%{!?_without_esx:1}
%define with_hyperv        0%{!?_without_hyperv:1}
%define with_xenapi        0%{!?_without_xenapi:1}
%define with_parallels     0%{!?_without_parallels:1}
# No test for bhyve, because it does not build on Linux

# Then the secondary host drivers, which run inside libvirtd
%define with_interface        0%{!?_without_interface:%{server_drivers}}
%define with_network          0%{!?_without_network:%{server_drivers}}
%define with_storage_fs       0%{!?_without_storage_fs:%{server_drivers}}
%define with_storage_lvm      0%{!?_without_storage_lvm:%{server_drivers}}
%define with_storage_iscsi    0%{!?_without_storage_iscsi:%{server_drivers}}
%define with_storage_disk     0%{!?_without_storage_disk:%{server_drivers}}
%define with_storage_mpath    0%{!?_without_storage_mpath:%{server_drivers}}
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
    %define with_storage_rbd      0%{!?_without_storage_rbd:%{server_drivers}}
%else
    %define with_storage_rbd      0
%endif
%if 0%{?fedora} >= 17
    %define with_storage_sheepdog 0%{!?_without_storage_sheepdog:%{server_drivers}}
%else
    %define with_storage_sheepdog 0
%endif
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 6
    %define with_storage_gluster 0%{!?_without_storage_gluster:%{server_drivers}}
%else
    %define with_storage_gluster 0
%endif
%define with_numactl          0%{!?_without_numactl:%{server_drivers}}
%define with_selinux          0%{!?_without_selinux:%{server_drivers}}

# Just hardcode to off, since few people ever have apparmor RPMs installed
%define with_apparmor         0%{!?_without_apparmor:0}

# A few optional bits off by default, we enable later
%define with_polkit        0%{!?_without_polkit:0}
%define with_capng         0%{!?_without_capng:0}
%define with_fuse          0%{!?_without_fuse:0}
%define with_netcf         0%{!?_without_netcf:0}
%define with_udev          0%{!?_without_udev:0}
%define with_hal           0%{!?_without_hal:0}
%define with_yajl          0%{!?_without_yajl:0}
%define with_nwfilter      0%{!?_without_nwfilter:0}
%define with_libpcap       0%{!?_without_libpcap:0}
%define with_macvtap       0%{!?_without_macvtap:0}
%define with_libnl         0%{!?_without_libnl:0}
%define with_dtrace        0%{!?_without_dtrace:0}
%define with_cgconfig      0%{!?_without_cgconfig:0}
%define with_sanlock       0%{!?_without_sanlock:0}
%define with_systemd       0%{!?_without_systemd:0}
%define with_numad         0%{!?_without_numad:0}
%define with_firewalld     0%{!?_without_firewalld:0}
%define with_libssh2       0%{!?_without_libssh2:0}
%define with_wireshark     0%{!?_without_wireshark:0}
%define with_systemd_daemon 0%{!?_without_systemd_daemon:0}
%define with_pm_utils      1

# Non-server/HV driver defaults which are always enabled
%define with_sasl          0%{!?_without_sasl:1}
%define with_audit         0%{!?_without_audit:1}


# Finally set the OS / architecture specific special cases

# Xen is available only on x86_64 and aarch64
%ifnarch %{ix86} x86_64 ia64 aarch64
    %define with_xen 0
    %define with_libxl 0
%endif

# vbox is available only on i386 x86_64
%ifnarch %{ix86} x86_64
    %define with_vbox 0
%endif

# Numactl is not available on s390[x] and ARM
%ifarch s390 s390x %{arm}
    %define with_numactl 0
%endif

# libgfapi is built only on x86_64 on rhel
%ifnarch x86_64
    %if 0%{?rhel} >= 6
        %define with_storage_gluster 0
    %endif
%endif

# librados and librbd are built only on x86_64 on rhel
%ifnarch x86_64
    %if 0%{?rhel} >= 7
        %define with_storage_rbd 0
    %endif
%endif

# RHEL doesn't ship OpenVZ, VBox, UML, PowerHypervisor,
# VMWare, libxenserver (xenapi), libxenlight (Xen 4.1 and newer),
# or HyperV.
%if 0%{?rhel}
    %define with_openvz 0
    %define with_vbox 0
    %define with_uml 0
    %define with_phyp 0
    %define with_vmware 0
    %define with_xenapi 0
    %define with_hyperv 0
    %define with_parallels 0
%endif

# Fedora 17 / RHEL-7 are first where we use systemd. Although earlier
# Fedora has systemd, libvirt still used sysvinit there.
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
    %define with_systemd 1
    %define with_systemd_daemon 1
    %define with_pm_utils 0
%endif

# Fedora 18 / RHEL-7 are first where firewalld support is enabled
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
    %define with_firewalld 1
%endif

# RHEL-5 is too old for LXC
%if 0%{?rhel} == 5
    %define with_lxc 0
%endif

# Fedora doesn't have new enough Xen for libxl until F18
%if 0%{?fedora} && 0%{?fedora} < 18
    %define with_libxl 0
%endif

# fuse is used to provide virtualized /proc for LXC
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
    %define with_fuse      0%{!?_without_fuse:1}
%endif

# RHEL 5 lacks newer tools
%if 0%{?rhel} == 5
    %define with_hal       0%{!?_without_hal:%{server_drivers}}
%else
    %define with_polkit    0%{!?_without_polkit:1}
    %define with_capng     0%{!?_without_capng:1}
    %define with_netcf     0%{!?_without_netcf:%{server_drivers}}
    %define with_udev      0%{!?_without_udev:%{server_drivers}}
    %define with_yajl      0%{!?_without_yajl:%{server_drivers}}
    %define with_dtrace 1
%endif

# interface requires netcf
%if ! 0%{?with_netcf}
    %define with_interface     0
%endif

# Enable sanlock library for lock management with QEMU
# Sanlock is available only on arches where kvm is available for RHEL
%if 0%{?fedora} >= 16
    %define with_sanlock 0%{!?_without_sanlock:%{server_drivers}}
%endif
%if 0%{?rhel} >= 6
    %ifarch %{qemu_kvm_arches}
        %define with_sanlock 0%{!?_without_sanlock:%{server_drivers}}
    %endif
%endif

# Enable libssh2 transport for new enough distros
%if 0%{?fedora} >= 17
    %define with_libssh2 0%{!?_without_libssh2:1}
%endif

# Enable wireshark plugins for all distros shipping libvirt 1.2.2 or newer
%if 0%{?fedora} >= 21
    %define with_wireshark 0%{!?_without_wireshark:1}
%endif

# Disable some drivers when building without libvirt daemon.
# The logic is the same as in configure.ac
%if ! %{with_libvirtd}
    %define with_interface 0
    %define with_network 0
    %define with_qemu 0
    %define with_lxc 0
    %define with_uml 0
    %define with_hal 0
    %define with_udev 0
    %define with_storage_fs 0
    %define with_storage_lvm 0
    %define with_storage_iscsi 0
    %define with_storage_mpath 0
    %define with_storage_rbd 0
    %define with_storage_sheepdog 0
    %define with_storage_gluster 0
    %define with_storage_disk 0
%endif

%if %{with_qemu} || %{with_lxc} || %{with_uml}
    %define with_nwfilter 0%{!?_without_nwfilter:%{server_drivers}}
# Enable libpcap library
    %define with_libpcap  0%{!?_without_libpcap:%{server_drivers}}
    %define with_macvtap  0%{!?_without_macvtap:%{server_drivers}}

# numad is used to manage the CPU and memory placement dynamically,
# it's not available on s390[x] and ARM.
    %if 0%{?fedora} >= 17 || 0%{?rhel} >= 6
        %ifnarch s390 s390x %{arm}
            %define with_numad    0%{!?_without_numad:%{server_drivers}}
        %endif
    %endif
%endif

%if %{with_macvtap}
    %define with_libnl 1
%endif

# Pull in cgroups config system
%if 0%{?fedora} || 0%{?rhel} >= 6
    %if %{with_qemu} || %{with_lxc}
        %define with_cgconfig 0%{!?_without_cgconfig:1}
    %endif
%endif

%if %{with_udev} || %{with_hal}
    %define with_nodedev 1
%else
    %define with_nodedev 0
%endif

%if %{with_storage_fs} || %{with_storage_mpath} || %{with_storage_iscsi} || %{with_storage_lvm} || %{with_storage_disk}
    %define with_storage 1
%else
    %define with_storage 0
%endif


# Force QEMU to run as non-root
%if 0%{?fedora} || 0%{?rhel} >= 6
    %define qemu_user  qemu
    %define qemu_group  qemu
%else
    %define qemu_user  root
    %define qemu_group  root
%endif


# Advertise OVMF and AAVMF from nightly firmware repo
%if 0%{?fedora}
    %define with_loader_nvram --with-loader-nvram="/usr/share/edk2.git/ovmf-x64/OVMF_CODE-pure-efi.fd:/usr/share/edk2.git/ovmf-x64/OVMF_VARS-pure-efi.fd:/usr/share/edk2.git/aarch64/QEMU_EFI-pflash.raw:/usr/share/edk2.git/aarch64/vars-template-pflash.raw"
%endif


# The RHEL-5 Xen package has some feature backports. This
# flag is set to enable use of those special bits on RHEL-5
%if 0%{?rhel} == 5
    %define with_rhel5  1
%else
    %define with_rhel5  0
%endif

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
    %define with_systemd_macros 1
%else
    %define with_systemd_macros 0
%endif


# RHEL releases provide stable tool chains and so it is safe to turn
# compiler warning into errors without being worried about frequent
# changes in reported warnings
%if 0%{?rhel}
    %define enable_werror --enable-werror
%else
    %define enable_werror --disable-werror
%endif


Summary: Library providing a simple virtualization API
Name: libvirt
Version: 1.2.15
Release: 4%{?dist}%{?extra_release}
License: LGPLv2+
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
URL: http://libvirt.org/
ExclusiveArch: x86_64 aarch64

%if %(echo %{version} | grep -o \\. | wc -l) == 3
    %define mainturl stable_updates/
%endif
Source: http://libvirt.org/sources/%{?mainturl}libvirt-%{version}.tar.gz

Patch1: 0001-caps-Don-t-default-to-i686-of-KVM-on-x86_64.patch
Patch2: 0002-disable-paravirt-cpu-test.patch

%if %{with_libvirtd}
Requires: libvirt-daemon = %{version}-%{release}
    %if %{with_network}
Requires: libvirt-daemon-config-network = %{version}-%{release}
    %endif
    %if %{with_nwfilter}
Requires: libvirt-daemon-config-nwfilter = %{version}-%{release}
    %endif
    %if %{with_driver_modules}
        %if %{with_libxl}
Requires: libvirt-daemon-driver-libxl = %{version}-%{release}
        %endif
        %if %{with_lxc}
Requires: libvirt-daemon-driver-lxc = %{version}-%{release}
        %endif
        %if %{with_qemu}
Requires: libvirt-daemon-driver-qemu = %{version}-%{release}
        %endif
        %if %{with_uml}
Requires: libvirt-daemon-driver-uml = %{version}-%{release}
        %endif
        %if %{with_xen}
Requires: libvirt-daemon-driver-xen = %{version}-%{release}
        %endif
        %if %{with_vbox}
Requires: libvirt-daemon-driver-vbox = %{version}-%{release}
        %endif
        %if %{with_nwfilter}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
        %endif

	%if %{with_interface}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
	%endif
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
    %endif
%endif
Requires: libvirt-client = %{version}-%{release}

# All build-time requirements. Run-time requirements are
# listed against each sub-RPM
%if 0%{?enable_autotools}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: libtool
BuildRequires: /usr/bin/pod2man
%endif
BuildRequires: git
BuildRequires: perl
BuildRequires: python
%if %{with_systemd}
BuildRequires: systemd-units
%endif
%if %{with_systemd_daemon}
BuildRequires: systemd-devel
%endif
%if %{with_xen} || %{with_libxl}
BuildRequires: xen-devel
%endif
BuildRequires: libxml2-devel
BuildRequires: xhtml1-dtds
BuildRequires: libxslt
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gettext
BuildRequires: libtasn1-devel
%if (0%{?rhel} && 0%{?rhel} < 7) || (0%{?fedora} && 0%{?fedora} < 19)
BuildRequires: libgcrypt-devel
%endif
BuildRequires: gnutls-devel
BuildRequires: libattr-devel
%if %{with_libvirtd}
# For pool-build probing for existing pools
BuildRequires: libblkid-devel >= 2.17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 6
# for augparse, optionally used in testing
BuildRequires: augeas
%endif
%if %{with_hal}
BuildRequires: hal-devel
%endif
%if %{with_udev}
    %if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
BuildRequires: systemd-devel >= 185
    %else
BuildRequires: libudev-devel >= 145
    %endif
BuildRequires: libpciaccess-devel >= 0.10.9
%endif
%if %{with_yajl}
BuildRequires: yajl-devel
%endif
%if %{with_sanlock}
# make sure libvirt is built with new enough sanlock on
# distros that have it; required for on_lockfailure
    %if 0%{?fedora} >= 17 || 0%{?rhel} >= 6
BuildRequires: sanlock-devel >= 2.4
    %else
BuildRequires: sanlock-devel >= 1.8
    %endif
%endif
%if %{with_libpcap}
BuildRequires: libpcap-devel
%endif
%if %{with_libnl}
    %if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
BuildRequires: libnl3-devel
    %else
BuildRequires: libnl-devel
    %endif
%endif
%if %{with_avahi}
BuildRequires: avahi-devel
%endif
%if %{with_selinux}
BuildRequires: libselinux-devel
%endif
%if %{with_apparmor}
BuildRequires: libapparmor-devel
%endif
%if %{with_network}
BuildRequires: dnsmasq >= 2.41
BuildRequires: iptables
    %if (0%{?fedora} && 0%{?fedora} < 17) || (0%{?rhel} && 0%{?rhel} < 7)
BuildRequires: iptables-ipv6
    %endif
BuildRequires: radvd
%endif
%if %{with_nwfilter}
BuildRequires: ebtables
%endif
BuildRequires: module-init-tools
%if %{with_sasl}
BuildRequires: cyrus-sasl-devel
%endif
%if %{with_polkit}
    %if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
BuildRequires: polkit-devel >= 0.112
    %else
        %if 0%{?fedora} || 0%{?rhel} >= 6
BuildRequires: polkit-devel >= 0.93
        %else
BuildRequires: PolicyKit-devel >= 0.6
        %endif
    %endif
%endif
%if %{with_storage_fs}
# For mount/umount in FS driver
BuildRequires: util-linux
%endif
%if %{with_qemu}
# From QEMU RPMs
BuildRequires: /usr/bin/qemu-img
%else
    %if %{with_xen}
    %ifnarch aarch64
# From Xen RPMs
BuildRequires: /usr/sbin/qcow-create
    %endif
    %endif
%endif
%if %{with_storage_lvm}
# For LVM drivers
BuildRequires: lvm2
%endif
%if %{with_storage_iscsi}
# For ISCSI driver
BuildRequires: iscsi-initiator-utils
%endif
%if %{with_storage_disk}
# For disk driver
BuildRequires: parted-devel
    %if 0%{?rhel} == 5
# Broken RHEL-5 parted RPM is missing a dep
BuildRequires: e2fsprogs-devel
    %endif
%endif
%if %{with_storage_mpath} || %{with_storage_disk}
# For Multipath support
    %if 0%{?rhel} == 5
# Broken RHEL-5 packaging has header files in main RPM :-(
BuildRequires: device-mapper
    %else
BuildRequires: device-mapper-devel
    %endif
%endif
%if %{with_storage_rbd}
    %if 0%{?rhel} >= 7
BuildRequires: librados2-devel
BuildRequires: librbd1-devel
    %else
BuildRequires: ceph-devel
    %endif
%endif
%if %{with_storage_gluster}
    %if 0%{?rhel} >= 6
BuildRequires: glusterfs-api-devel >= 3.4.0
BuildRequires: glusterfs-devel >= 3.4.0
    %else
BuildRequires: glusterfs-api-devel >= 3.4.1
BuildRequires: glusterfs-devel >= 3.4.1
    %endif
%endif
%if %{with_numactl}
# For QEMU/LXC numa info
BuildRequires: numactl-devel
%endif
%if %{with_capng}
BuildRequires: libcap-ng-devel >= 0.5.0
%endif
%if %{with_fuse}
BuildRequires: fuse-devel >= 2.8.6
%endif
%if %{with_phyp} || %{with_libssh2}
BuildRequires: libssh2-devel >= 1.3.0
%endif

%if %{with_netcf}
    %if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
BuildRequires: netcf-devel >= 0.2.2
    %else
        %if 0%{?fedora} >= 16 || 0%{?rhel} >= 6
BuildRequires: netcf-devel >= 0.1.8
        %else
BuildRequires: netcf-devel >= 0.1.4
        %endif
    %endif
%endif
%if %{with_esx}
    %if 0%{?fedora} || 0%{?rhel} >= 6
BuildRequires: libcurl-devel
    %else
BuildRequires: curl-devel
    %endif
%endif
%if %{with_hyperv}
BuildRequires: libwsman-devel >= 2.2.3
%endif
%if %{with_audit}
BuildRequires: audit-libs-devel
%endif
%if %{with_dtrace}
# we need /usr/sbin/dtrace
BuildRequires: systemtap-sdt-devel
%endif

%if %{with_storage_fs}
# For mount/umount in FS driver
BuildRequires: util-linux
# For showmount in FS driver (netfs discovery)
BuildRequires: nfs-utils
%endif

%if %{with_firewalld} || %{with_polkit}
# Communication with the firewall and polkit daemons use DBus
BuildRequires: dbus-devel
%endif

# Fedora build root suckage
BuildRequires: gawk

# For storage wiping with different algorithms
BuildRequires: scrub

%if %{with_numad}
BuildRequires: numad
%endif

%if %{with_wireshark}
BuildRequires: wireshark-devel
%endif

Provides: bundled(gnulib)

%description
Libvirt is a C toolkit to interact with the virtualization capabilities
of recent versions of Linux (and other OSes). The main package includes
the libvirtd server exporting the virtualization support.

%package docs
Summary: API reference and website documentation
Group: Development/Libraries

%description docs
Includes the API reference for the libvirt C library, and a complete
copy of the libvirt.org website documentation.

%if %{with_libvirtd}
%package daemon
Summary: Server side daemon and supporting files for libvirt library
Group: Development/Libraries

# All runtime requirements for the libvirt package (runtime requrements
# for subpackages are listed later in those subpackages)

# The client side, i.e. shared libs and virsh are in a subpackage
Requires: %{name}-client = %{version}-%{release}

# for modprobe of pci devices
Requires: module-init-tools
# for /sbin/ip & /sbin/tc
Requires: iproute
    %if %{with_avahi}
        %if 0%{?rhel} == 5
Requires: avahi
        %else
Requires: avahi-libs
        %endif
    %endif
    %if %{with_polkit}
        %if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
Requires: polkit >= 0.112
        %else
            %if 0%{?fedora} || 0%{?rhel} >=6
Requires: polkit >= 0.93
            %else
Requires: PolicyKit >= 0.6
            %endif
        %endif
    %endif
    %if %{with_cgconfig}
Requires: libcgroup
    %endif
    %ifarch %{ix86} x86_64 ia64
# For virConnectGetSysinfo
Requires: dmidecode
    %endif
# For service management
    %if %{with_systemd}
Requires(post): systemd-units
Requires(post): systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units
    %endif
    %if %{with_numad}
Requires: numad
    %endif
# libvirtd depends on 'messagebus' service
Requires: dbus
# For uid creation during pre
Requires(pre): shadow-utils

%description daemon
Server side daemon required to manage the virtualization capabilities
of recent versions of Linux. Requires a hypervisor specific sub-RPM
for specific drivers.

    %if %{with_network}
%package daemon-config-network
Summary: Default configuration files for the libvirtd daemon
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
        %endif

%description daemon-config-network
Default configuration files for setting up NAT based networking
    %endif

    %if %{with_nwfilter}
%package daemon-config-nwfilter
Summary: Network filter configuration files for the libvirtd daemon
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
        %endif

%description daemon-config-nwfilter
Network filter configuration files for cleaning guest traffic
    %endif

    %if %{with_driver_modules}
        %if %{with_network}
%package daemon-driver-network
Summary: Network driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}
Requires: dnsmasq >= 2.41
Requires: radvd
Requires: iptables
            %if (0%{?fedora} && 0%{?fedora} < 17) || (0%{?rhel} && 0%{?rhel} < 7)
Requires: iptables-ipv6
            %endif

%description daemon-driver-network
The network driver plugin for the libvirtd daemon, providing
an implementation of the virtual network APIs using the Linux
bridge capabilities.
        %endif


        %if %{with_nwfilter}
%package daemon-driver-nwfilter
Summary: Nwfilter driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}
Requires: iptables
            %if (0%{?fedora} && 0%{?fedora} < 17) || (0%{?rhel} && 0%{?rhel} < 7)
Requires: iptables-ipv6
            %endif
Requires: ebtables

%description daemon-driver-nwfilter
The nwfilter driver plugin for the libvirtd daemon, providing
an implementation of the firewall APIs using the ebtables,
iptables and ip6tables capabilities
        %endif


        %if %{with_nodedev}
%package daemon-driver-nodedev
Summary: Nodedev driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}
# needed for device enumeration
            %if %{with_hal}
Requires: hal
            %endif
            %if %{with_udev}
                %if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
Requires: systemd >= 185
                %else
Requires: udev >= 145
                %endif
            %endif

%description daemon-driver-nodedev
The nodedev driver plugin for the libvirtd daemon, providing
an implementation of the node device APIs using the udev
capabilities.
        %endif


        %if %{with_interface}
%package daemon-driver-interface
Summary: Interface driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}
            %if %{with_netcf} && (0%{?fedora} >= 18 || 0%{?rhel} >= 7)
Requires: netcf-libs >= 0.2.2
            %endif

%description daemon-driver-interface
The interface driver plugin for the libvirtd daemon, providing
an implementation of the network interface APIs using the
netcf library
        %endif


%package daemon-driver-secret
Summary: Secret driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-secret
The secret driver plugin for the libvirtd daemon, providing
an implementation of the secret key APIs.


        %if %{with_storage}
%package daemon-driver-storage
Summary: Storage driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}
            %if %{with_storage_fs}
Requires: nfs-utils
# For mkfs
Requires: util-linux
# For glusterfs
                %if 0%{?fedora}
Requires: glusterfs-client >= 2.0.1
                %endif
            %endif
            %if %{with_storage_lvm}
# For LVM drivers
Requires: lvm2
            %endif
            %if %{with_storage_iscsi}
# For ISCSI driver
Requires: iscsi-initiator-utils
            %endif
            %if %{with_storage_disk}
# For disk driver
Requires: parted
Requires: device-mapper
            %endif
            %if %{with_storage_mpath}
# For multipath support
Requires: device-mapper
            %endif
            %if %{with_storage_sheepdog}
# For Sheepdog support
Requires: sheepdog
            %endif
            %if %{with_qemu}
# From QEMU RPMs
Requires: /usr/bin/qemu-img
            %else
                %if %{with_xen}
# From Xen RPMs
                %ifnarch aarch64
Requires: /usr/sbin/qcow-create
                %endif
                %endif
            %endif

%description daemon-driver-storage
The storage driver plugin for the libvirtd daemon, providing
an implementation of the storage APIs using LVM, iSCSI,
parted and more.
        %endif


        %if %{with_qemu}
%package daemon-driver-qemu
Summary: Qemu driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}
# There really is a hard cross-driver dependency here
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: /usr/bin/qemu-img
# For image compression
Requires: gzip
Requires: bzip2
Requires: lzop
Requires: xz

%description daemon-driver-qemu
The qemu driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
QEMU
        %endif


        %if %{with_lxc}
%package daemon-driver-lxc
Summary: LXC driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}
# There really is a hard cross-driver dependency here
Requires: libvirt-daemon-driver-network = %{version}-%{release}

%description daemon-driver-lxc
The LXC driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
the Linux kernel
        %endif


        %if %{with_uml}
%package daemon-driver-uml
Summary: Uml driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-uml
The UML driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
User Mode Linux
        %endif


        %if %{with_xen}
%package daemon-driver-xen
Summary: Xen driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-xen
The Xen driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
Xen
        %endif


        %if %{with_vbox}
%package daemon-driver-vbox
Summary: VirtualBox driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-vbox
The vbox driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
VirtualBox
        %endif


        %if %{with_libxl}
%package daemon-driver-libxl
Summary: Libxl driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-libxl
The Libxl driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
Libxl
        %endif
    %endif # %{with_driver_modules}



    %if %{with_qemu_tcg}
%package daemon-qemu
Summary: Server side daemon & driver required to run QEMU guests
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
Requires: libvirt-daemon-driver-qemu = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
        %endif
Requires: qemu

%description daemon-qemu
Server side daemon and driver required to manage the virtualization
capabilities of the QEMU TCG emulators
    %endif


    %if %{with_qemu_kvm}
%package daemon-kvm
Summary: Server side daemon & driver required to run KVM guests
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
Requires: libvirt-daemon-driver-qemu = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
        %endif
Requires: qemu-kvm

%description daemon-kvm
Server side daemon and driver required to manage the virtualization
capabilities of the KVM hypervisor
    %endif


    %if %{with_lxc}
%package daemon-lxc
Summary: Server side daemon & driver required to run LXC guests
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
Requires: libvirt-daemon-driver-lxc = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
        %endif

%description daemon-lxc
Server side daemon and driver required to manage the virtualization
capabilities of LXC
    %endif


    %if %{with_uml}
%package daemon-uml
Summary: Server side daemon & driver required to run UML guests
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
Requires: libvirt-daemon-driver-uml = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
        %endif
# There are no UML kernel RPMs in Fedora/RHEL to depend on.

%description daemon-uml
Server side daemon and driver required to manage the virtualization
capabilities of UML
    %endif


    %if %{with_xen} || %{with_libxl}
%package daemon-xen
Summary: Server side daemon & driver required to run XEN guests
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
            %if %{with_xen}
Requires: libvirt-daemon-driver-xen = %{version}-%{release}
            %endif
            %if %{with_libxl}
Requires: libvirt-daemon-driver-libxl = %{version}-%{release}
            %endif
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
        %endif
Requires: xen

%description daemon-xen
Server side daemon and driver required to manage the virtualization
capabilities of XEN
    %endif

    %if %{with_vbox}
%package daemon-vbox
Summary: Server side daemon & driver required to run VirtualBox guests
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
Requires: libvirt-daemon-driver-vbox = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
        %endif

%description daemon-vbox
Server side daemon and driver required to manage the virtualization
capabilities of VirtualBox
    %endif
%endif # %{with_libvirtd}

%package client
Summary: Client side library and utilities of the libvirt library
Group: Development/Libraries
Requires: readline
Requires: ncurses
# So remote clients can access libvirt over SSH tunnel
# (client invokes 'nc' against the UNIX socket on the server)
Requires: nc
# Needed by /usr/libexec/libvirt-guests.sh script.
Requires: gettext
# Needed by virt-pki-validate script.
Requires: gnutls-utils
%if %{with_pm_utils}
# Needed for probing the power management features of the host.
Requires: pm-utils
%endif
%if %{with_sasl}
Requires: cyrus-sasl
# Not technically required, but makes 'out-of-box' config
# work correctly & doesn't have onerous dependencies
Requires: cyrus-sasl-md5
%endif

%description client
Shared libraries and client binaries needed to access to the
virtualization capabilities of recent versions of Linux (and other OSes).

%if %{with_wireshark}
%package wireshark
Summary: Wireshark dissector plugin for libvirt RPC transactions
Group: Development/Libraries
Requires: wireshark
Requires: %{name}-client = %{version}-%{release}

%description wireshark
Wireshark dissector plugin for better analysis of libvirt RPC traffic.
%endif

%if %{with_lxc}
%package login-shell
Summary: Login shell for connecting users to an LXC container
Group: Development/Libraries
Requires: %{name}-client = %{version}-%{release}

%description login-shell
Provides the set-uid virt-login-shell binary that is used to
connect a user to an LXC container when they login, by switching
namespaces.
%endif

%package devel
Summary: Libraries, includes, etc. to compile with the libvirt library
Group: Development/Libraries
Requires: %{name}-client = %{version}-%{release}
Requires: %{name}-docs = %{version}-%{release}
Requires: pkgconfig

%description devel
Include header files & development libraries for the libvirt C library.

%if %{with_sanlock}
%package lock-sanlock
Summary: Sanlock lock manager plugin for QEMU driver
Group: Development/Libraries
    %if 0%{?fedora} >= 17 || 0%{?rhel} >= 6
Requires: sanlock >= 2.4
    %else
Requires: sanlock >= 1.8
    %endif
#for virt-sanlock-cleanup require augeas
Requires: augeas
Requires: %{name}-daemon = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}

%description lock-sanlock
Includes the Sanlock lock manager plugin for the QEMU
driver
%endif

%prep
%setup -q

# Patches have to be stored in a temporary file because RPM has
# a limit on the length of the result of any macro expansion;
# if the string is longer, it's silently cropped
%{lua:
    tmp = os.tmpname();
    f = io.open(tmp, "w+");
    count = 0;
    for i, p in ipairs(patches) do
        f:write(p.."\n");
        count = count + 1;
    end;
    f:close();
    print("PATCHCOUNT="..count.."\n")
    print("PATCHLIST="..tmp.."\n")
}

git init -q
git config user.name rpm-build
git config user.email rpm-build
git config gc.auto 0
git add .
git commit -q -a --author 'rpm-build <rpm-build>' \
           -m '%{name}-%{version} base'

COUNT=$(grep '\.patch$' $PATCHLIST | wc -l)
if [ $COUNT -ne $PATCHCOUNT ]; then
    echo "Found $COUNT patches in $PATCHLIST, expected $PATCHCOUNT"
    exit 1
fi
if [ $COUNT -gt 0 ]; then
    xargs git am <$PATCHLIST || exit 1
fi
echo "Applied $COUNT patches"
rm -f $PATCHLIST

%build
%if ! %{with_xen}
    %define _without_xen --without-xen
%endif

%if ! %{with_qemu}
    %define _without_qemu --without-qemu
%endif

%if ! %{with_openvz}
    %define _without_openvz --without-openvz
%endif

%if ! %{with_lxc}
    %define _without_lxc --without-lxc
%endif

%if ! %{with_vbox}
    %define _without_vbox --without-vbox
%endif

%if ! %{with_xenapi}
    %define _without_xenapi --without-xenapi
%endif

%if ! %{with_libxl}
    %define _without_libxl --without-libxl
%endif

%if ! %{with_sasl}
    %define _without_sasl --without-sasl
%endif

%if ! %{with_avahi}
    %define _without_avahi --without-avahi
%endif

%if ! %{with_phyp}
    %define _without_phyp --without-phyp
%endif

%if ! %{with_esx}
    %define _without_esx --without-esx
%endif

%if ! %{with_hyperv}
    %define _without_hyperv --without-hyperv
%endif

%if ! %{with_vmware}
    %define _without_vmware --without-vmware
%endif

%if ! %{with_parallels}
    %define _without_parallels --without-parallels
%endif

%if ! %{with_polkit}
    %define _without_polkit --without-polkit
%endif

%if ! %{with_libvirtd}
    %define _without_libvirtd --without-libvirtd
%endif

%if ! %{with_uml}
    %define _without_uml --without-uml
%endif

%if %{with_rhel5}
    %define _with_rhel5_api --with-rhel5-api
%endif

%if ! %{with_interface}
    %define _without_interface --without-interface
%endif

%if ! %{with_network}
    %define _without_network --without-network
%endif

%if ! %{with_storage_fs}
    %define _without_storage_fs --without-storage-fs
%endif

%if ! %{with_storage_lvm}
    %define _without_storage_lvm --without-storage-lvm
%endif

%if ! %{with_storage_iscsi}
    %define _without_storage_iscsi --without-storage-iscsi
%endif

%if ! %{with_storage_disk}
    %define _without_storage_disk --without-storage-disk
%endif

%if ! %{with_storage_mpath}
    %define _without_storage_mpath --without-storage-mpath
%endif

%if ! %{with_storage_rbd}
    %define _without_storage_rbd --without-storage-rbd
%endif

%if ! %{with_storage_sheepdog}
    %define _without_storage_sheepdog --without-storage-sheepdog
%endif

%if ! %{with_storage_gluster}
    %define _without_storage_gluster --without-storage-gluster
%endif

%if ! %{with_numactl}
    %define _without_numactl --without-numactl
%endif

%if ! %{with_numad}
    %define _without_numad --without-numad
%endif

%if ! %{with_capng}
    %define _without_capng --without-capng
%endif

%if ! %{with_fuse}
    %define _without_fuse --without-fuse
%endif

%if ! %{with_netcf}
    %define _without_netcf --without-netcf
%endif

%if ! %{with_selinux}
    %define _without_selinux --without-selinux
%endif

%if ! %{with_apparmor}
    %define _without_apparmor --without-apparmor
%endif

%if ! %{with_hal}
    %define _without_hal --without-hal
%endif

%if ! %{with_udev}
    %define _without_udev --without-udev
%endif

%if ! %{with_yajl}
    %define _without_yajl --without-yajl
%endif

%if ! %{with_sanlock}
    %define _without_sanlock --without-sanlock
%endif

%if ! %{with_libpcap}
    %define _without_libpcap --without-libpcap
%endif

%if ! %{with_macvtap}
    %define _without_macvtap --without-macvtap
%endif

%if ! %{with_audit}
    %define _without_audit --without-audit
%endif

%if ! %{with_dtrace}
    %define _without_dtrace --without-dtrace
%endif

%if ! %{with_driver_modules}
    %define _without_driver_modules --without-driver-modules
%endif

%if %{with_firewalld}
    %define _with_firewalld --with-firewalld
%endif

%if ! %{with_wireshark}
    %define _without_wireshark --without-wireshark-dissector
%endif

%if ! %{with_systemd_daemon}
    %define _without_systemd_daemon --without-systemd-daemon
%endif

%if ! %{with_pm_utils}
    %define _without_pm_utils --without-pm-utils
%endif

%define when  %(date +"%%F-%%T")
%define where %(hostname)
%define who   %{?packager}%{!?packager:Unknown}
%define with_packager --with-packager="%{who}, %{when}, %{where}"
%define with_packager_version --with-packager-version="%{release}"

%if %{with_systemd}
    %define init_scripts --with-init_script=systemd
%else
    %define init_scripts --with-init_script=redhat
%endif

%if %{with_selinux}
    %if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
        %define with_selinux_mount --with-selinux-mount="/sys/fs/selinux"
    %else
        %define with_selinux_mount --with-selinux-mount="/selinux"
    %endif
%endif

# place macros above and build commands below this comment

%if 0%{?enable_autotools}
 autoreconf -if
%endif

rm -f po/stamp-po
%configure %{?_without_xen} \
           %{?_without_qemu} \
           %{?_without_openvz} \
           %{?_without_lxc} \
           %{?_without_vbox} \
           %{?_without_libxl} \
           %{?_without_xenapi} \
           %{?_without_sasl} \
           %{?_without_avahi} \
           %{?_without_polkit} \
           %{?_without_libvirtd} \
           %{?_without_uml} \
           %{?_without_phyp} \
           %{?_without_esx} \
           %{?_without_hyperv} \
           %{?_without_vmware} \
           %{?_without_parallels} \
           --without-bhyve \
           %{?_without_interface} \
           %{?_without_network} \
           %{?_with_rhel5_api} \
           %{?_without_storage_fs} \
           %{?_without_storage_lvm} \
           %{?_without_storage_iscsi} \
           %{?_without_storage_disk} \
           %{?_without_storage_mpath} \
           %{?_without_storage_rbd} \
           %{?_without_storage_sheepdog} \
           %{?_without_storage_gluster} \
           %{?_without_numactl} \
           %{?_without_numad} \
           %{?_without_capng} \
           %{?_without_fuse} \
           %{?_without_netcf} \
           %{?_without_selinux} \
           %{?_with_selinux_mount} \
           %{?_without_apparmor} \
           %{?_without_hal} \
           %{?_without_udev} \
           %{?_without_yajl} \
           %{?_without_sanlock} \
           %{?_without_libpcap} \
           %{?_without_macvtap} \
           %{?_without_audit} \
           %{?_without_dtrace} \
           %{?_without_driver_modules} \
           %{?_with_firewalld} \
           %{?_without_wireshark} \
           %{?_without_systemd_daemon} \
           %{?_without_pm_utils} \
           %{with_packager} \
           %{with_packager_version} \
           --with-qemu-user=%{qemu_user} \
           --with-qemu-group=%{qemu_group} \
           %{?with_loader_nvram} \
           %{?enable_werror} \
           --enable-expensive-tests \
           %{init_scripts}
make %{?_smp_mflags}
gzip -9 ChangeLog

%install
rm -fr %{buildroot}

# Avoid using makeinstall macro as it changes prefixes rather than setting
# DESTDIR. Newer make_install macro would be better but it's not available
# on RHEL 5, thus we need to expand it here.
make install DESTDIR=%{?buildroot} SYSTEMD_UNIT_DIR=%{_unitdir}

for i in object-events dominfo domsuspend hellolibvirt openauth xml/nwfilter systemtap dommigrate domtop
do
  (cd examples/$i ; make clean ; rm -rf .deps .libs Makefile Makefile.in)
done
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt/lock-driver/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt/lock-driver/*.a
%if %{with_driver_modules}
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt/connection-driver/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt/connection-driver/*.a
%endif
%if %{with_wireshark}
rm -f $RPM_BUILD_ROOT%{_libdir}/wireshark/plugins/*/libvirt.la
%endif

%if %{with_network}
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/lib/libvirt/dnsmasq/
# We don't want to install /etc/libvirt/qemu/networks in the main %files list
# because if the admin wants to delete the default network completely, we don't
# want to end up re-incarnating it on every RPM upgrade.
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/libvirt/networks/
cp $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/default.xml \
   $RPM_BUILD_ROOT%{_datadir}/libvirt/networks/default.xml
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/default.xml
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
# Strip auto-generated UUID - we need it generated per-install
sed -i -e "/<uuid>/d" $RPM_BUILD_ROOT%{_datadir}/libvirt/networks/default.xml
%else
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/default.xml
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
%endif
%if ! %{with_qemu}
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirtd_qemu.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
%endif
%find_lang %{name}

%if ! %{with_sanlock}
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirt_sanlock.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirt_sanlock.aug
%endif

%if ! %{with_lxc}
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirtd_lxc.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirtd_lxc.aug
%endif

%if ! %{with_qemu}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu.conf
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/libvirtd.qemu
%endif
%if ! %{with_lxc}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/lxc.conf
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/libvirtd.lxc
%endif
%if ! %{with_libxl}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/libxl.conf
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirtd_libxl.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirtd_libxl.aug
%endif
%if ! %{with_uml}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/libvirtd.uml
%endif

# Copied into libvirt-docs subpackage eventually
mv $RPM_BUILD_ROOT%{_datadir}/doc/libvirt-%{version} libvirt-docs

%if %{with_dtrace}
    %ifarch %{power64} s390x x86_64 ia64 alpha sparc64
mv $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_probes.stp \
   $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_probes-64.stp
mv $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_qemu_probes.stp \
   $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_qemu_probes-64.stp
    %endif
%endif

%if 0%{?rhel} == 5
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/sysctl.d/60-libvirtd.conf
%endif

%clean
rm -fr %{buildroot}

%check
cd tests
make
# These tests don't current work in a mock build root
for i in nodeinfotest seclabeltest
do
  rm -f $i
  printf 'int main(void) { return 0; }' > $i.c
  printf '#!/bin/sh\nexit 0\n' > $i
  chmod +x $i
done
if ! make check VIR_TEST_DEBUG=1
then
  cat test-suite.log || true
  exit 1
fi

%if %{with_libvirtd}
    %if ! %{with_driver_modules}
        %if %{with_qemu}
%pre daemon
            %if 0%{?fedora} || 0%{?rhel} >= 6
# We want soft static allocation of well-known ids, as disk images
# are commonly shared across NFS mounts by id rather than name; see
# https://fedoraproject.org/wiki/Packaging:UsersAndGroups
getent group kvm >/dev/null || groupadd -f -g 36 -r kvm
getent group qemu >/dev/null || groupadd -f -g 107 -r qemu
if ! getent passwd qemu >/dev/null; then
  if ! getent passwd 107 >/dev/null; then
    useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin -c "qemu user" qemu
  else
    useradd -r -g qemu -G kvm -d / -s /sbin/nologin -c "qemu user" qemu
  fi
fi
exit 0
            %endif
        %endif
    %endif

%post daemon

    %if %{with_systemd}
        %if %{with_systemd_macros}
            %systemd_post virtlockd.socket libvirtd.service libvirtd.socket
        %else
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl enable \
        virtlockd.socket \
        libvirtd.service >/dev/null 2>&1 || :
fi
        %endif
    %else
        %if %{with_cgconfig}
# Starting with Fedora 16/RHEL-7, systemd automounts all cgroups,
# and cgconfig is no longer a necessary service.
            %if (0%{?rhel} && 0%{?rhel} < 7) || (0%{?fedora} && 0%{?fedora} < 16)
if [ "$1" -eq "1" ]; then
/sbin/chkconfig cgconfig on
fi
            %endif
        %endif

/sbin/chkconfig --add libvirtd
/sbin/chkconfig --add virtlockd
    %endif

%preun daemon
    %if %{with_systemd}
        %if %{with_systemd_macros}
            %systemd_preun libvirtd.socket libvirtd.service virtlockd.socket virtlockd.service
        %else
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable \
        libvirtd.socket \
        libvirtd.service \
        virtlockd.socket \
        virtlockd.service > /dev/null 2>&1 || :
    /bin/systemctl stop \
        libvirtd.socket \
        libvirtd.service \
        virtlockd.socket \
        virtlockd.service > /dev/null 2>&1 || :
fi
        %endif
    %else
if [ $1 = 0 ]; then
    /sbin/service libvirtd stop 1>/dev/null 2>&1
    /sbin/chkconfig --del libvirtd
    /sbin/service virtlockd stop 1>/dev/null 2>&1
    /sbin/chkconfig --del virtlockd
fi
    %endif

%postun daemon
    %if %{with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    /bin/systemctl reload-or-try-restart virtlockd.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart libvirtd.service >/dev/null 2>&1 || :
fi
    %else
if [ $1 -ge 1 ]; then
    /sbin/service virtlockd reload > /dev/null 2>&1 || :
    /sbin/service libvirtd condrestart > /dev/null 2>&1
fi
    %endif

    %if %{with_systemd}
    %else
%triggerpostun daemon -- libvirt-daemon < 1.2.1
if [ "$1" -ge "1" ]; then
    /sbin/service virtlockd reload > /dev/null 2>&1 || :
    /sbin/service libvirtd condrestart > /dev/null 2>&1
fi
    %endif

    %if %{with_network}
%post daemon-config-network
if test $1 -eq 1 && test ! -f %{_sysconfdir}/libvirt/qemu/networks/default.xml ; then
    # see if the network used by default network creates a conflict,
    # and try to resolve it
    # NB: 192.168.122.0/24 is used in the default.xml template file;
    # do not modify any of those values here without also modifying
    # them in the template.
    orig_sub=122
    sub=${orig_sub}
    nl='
'
    routes="${nl}$(ip route show | cut -d' ' -f1)${nl}"
    case ${routes} in
      *"${nl}192.168.${orig_sub}.0/24${nl}"*)
        # there was a match, so we need to look for an unused subnet
        for new_sub in $(seq 124 254); do
          case ${routes} in
          *"${nl}192.168.${new_sub}.0/24${nl}"*)
            ;;
          *)
            sub=$new_sub
            break;
            ;;
          esac
        done
        ;;
      *)
        ;;
    esac

    UUID=`/usr/bin/uuidgen`
    sed -e "s/${orig_sub}/${sub}/g" \
        -e "s,</name>,</name>\n  <uuid>$UUID</uuid>," \
         < %{_datadir}/libvirt/networks/default.xml \
         > %{_sysconfdir}/libvirt/qemu/networks/default.xml
    ln -s ../default.xml %{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
fi
    %endif

    %if %{with_systemd}
%triggerun -- libvirt < 0.9.4
%{_bindir}/systemd-sysv-convert --save libvirtd >/dev/null 2>&1 ||:

# If the package is allowed to autostart:
/bin/systemctl --no-reload enable libvirtd.service >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del libvirtd >/dev/null 2>&1 || :
/bin/systemctl try-restart libvirtd.service >/dev/null 2>&1 || :
    %endif

    %if %{with_driver_modules}
        %if %{with_qemu}
%pre daemon-driver-qemu
            %if 0%{?fedora} || 0%{?rhel} >= 6
# We want soft static allocation of well-known ids, as disk images
# are commonly shared across NFS mounts by id rather than name; see
# https://fedoraproject.org/wiki/Packaging:UsersAndGroups
getent group kvm >/dev/null || groupadd -f -g 36 -r kvm
getent group qemu >/dev/null || groupadd -f -g 107 -r qemu
if ! getent passwd qemu >/dev/null; then
  if ! getent passwd 107 >/dev/null; then
    useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin -c "qemu user" qemu
  else
    useradd -r -g qemu -G kvm -d / -s /sbin/nologin -c "qemu user" qemu
  fi
fi
exit 0
            %endif
        %endif
    %endif
%endif # %{with_libvirtd}

%preun client

%if %{with_systemd}
    %if %{with_systemd_macros}
        %systemd_preun libvirt-guests.service
    %endif
%else
if [ $1 = 0 ]; then
    /sbin/chkconfig --del libvirt-guests
    rm -f /var/lib/libvirt/libvirt-guests
fi
%endif

%post client

/sbin/ldconfig
%if %{with_systemd}
    %if %{with_systemd_macros}
        %systemd_post libvirt-guests.service
    %endif
%else
/sbin/chkconfig --add libvirt-guests
%endif

%postun client

/sbin/ldconfig
%if %{with_systemd}
    %if %{with_systemd_macros}
        %systemd_postun libvirt-guests.service
    %endif
%triggerun client -- libvirt < 0.9.4
%{_bindir}/systemd-sysv-convert --save libvirt-guests >/dev/null 2>&1 ||:

# If the package is allowed to autostart:
/bin/systemctl --no-reload enable libvirt-guests.service >/dev/null 2>&1 ||:

# Run this because the SysV package being removed won't do them
/sbin/chkconfig --del libvirt-guests >/dev/null 2>&1 || :
%endif

%if %{with_sanlock}
%post lock-sanlock
if getent group sanlock > /dev/null ; then
    chmod 0770 %{_localstatedir}/lib/libvirt/sanlock
    chown root:sanlock %{_localstatedir}/lib/libvirt/sanlock
fi
%endif

%if %{with_lxc}
%pre login-shell
getent group virtlogin >/dev/null || groupadd -r virtlogin
exit 0
%endif

%files
%defattr(-, root, root)

%files docs
%defattr(-, root, root)
%doc AUTHORS ChangeLog.gz NEWS README TODO libvirt-docs/*

# API docs
%dir %{_datadir}/gtk-doc/html/libvirt/
%doc %{_datadir}/gtk-doc/html/libvirt/*.devhelp
%doc %{_datadir}/gtk-doc/html/libvirt/*.html
%doc %{_datadir}/gtk-doc/html/libvirt/*.png
%doc %{_datadir}/gtk-doc/html/libvirt/*.css

%if %{with_libvirtd}
%files daemon
%defattr(-, root, root)

%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/

    %if %{with_systemd}
%{_unitdir}/libvirtd.service
%{_unitdir}/libvirtd.socket
%{_unitdir}/virtlockd.service
%{_unitdir}/virtlockd.socket
    %else
%{_sysconfdir}/rc.d/init.d/libvirtd
%{_sysconfdir}/rc.d/init.d/virtlockd
    %endif
%doc daemon/libvirtd.upstart
%config(noreplace) %{_sysconfdir}/sysconfig/libvirtd
%config(noreplace) %{_sysconfdir}/sysconfig/virtlockd
%config(noreplace) %{_sysconfdir}/libvirt/libvirtd.conf
%config(noreplace) %{_sysconfdir}/libvirt/virtlockd.conf
    %if 0%{?fedora} || 0%{?rhel} >= 6
%config(noreplace) %{_prefix}/lib/sysctl.d/60-libvirtd.conf
    %endif

%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd
%dir %{_datadir}/libvirt/

%ghost %dir %{_localstatedir}/run/libvirt/

%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/images/
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/filesystems/
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/boot/
%dir %attr(0711, root, root) %{_localstatedir}/cache/libvirt/


%dir %attr(0755, root, root) %{_libdir}/libvirt/lock-driver
%attr(0755, root, root) %{_libdir}/libvirt/lock-driver/lockd.so

%{_datadir}/augeas/lenses/libvirtd.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd.aug
%{_datadir}/augeas/lenses/virtlockd.aug
%{_datadir}/augeas/lenses/tests/test_virtlockd.aug
%{_datadir}/augeas/lenses/libvirt_lockd.aug
    %if %{with_qemu}
%{_datadir}/augeas/lenses/tests/test_libvirt_lockd.aug
    %endif

    %if %{with_polkit}
        %if 0%{?fedora} || 0%{?rhel} >= 6
%{_datadir}/polkit-1/actions/org.libvirt.unix.policy
%{_datadir}/polkit-1/actions/org.libvirt.api.policy
        %else
%{_datadir}/PolicyKit/policy/org.libvirt.unix.policy
        %endif
    %endif

%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/

%attr(0755, root, root) %{_libexecdir}/libvirt_iohelper

    %if %{with_apparmor}
%attr(0755, root, root) %{_libexecdir}/virt-aa-helper
    %endif

%attr(0755, root, root) %{_sbindir}/libvirtd
%attr(0755, root, root) %{_sbindir}/virtlockd

%{_mandir}/man8/libvirtd.8*
%{_mandir}/man8/virtlockd.8*

    %if ! %{with_driver_modules}
        %if %{with_network} || %{with_qemu}
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/
        %endif
        %if %{with_network} || %{with_nwfilter}
%ghost %dir %{_localstatedir}/run/libvirt/network/
        %endif
        %if %{with_network}
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/autostart
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/network/
%dir %attr(0755, root, root) %{_localstatedir}/lib/libvirt/dnsmasq/
%attr(0755, root, root) %{_libexecdir}/libvirt_leaseshelper
        %endif
        %if %{with_nwfilter}
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/nwfilter/
        %endif
        %if %{with_storage_disk}
%attr(0755, root, root) %{_libexecdir}/libvirt_parthelper
        %endif
        %if %{with_qemu}
%config(noreplace) %{_sysconfdir}/libvirt/qemu.conf
%config(noreplace) %{_sysconfdir}/libvirt/qemu-lockd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.qemu
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%ghost %dir %attr(0700, root, root) %{_localstatedir}/run/libvirt/qemu/
%dir %attr(0750, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/
%dir %attr(0750, %{qemu_user}, %{qemu_group}) %{_localstatedir}/cache/libvirt/qemu/
%{_datadir}/augeas/lenses/libvirtd_qemu.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
        %endif
        %if %{with_lxc}
%config(noreplace) %{_sysconfdir}/libvirt/lxc.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.lxc
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/lxc/
%ghost %dir %{_localstatedir}/run/libvirt/lxc/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/lxc/
%{_datadir}/augeas/lenses/libvirtd_lxc.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_lxc.aug
%attr(0755, root, root) %{_libexecdir}/libvirt_lxc
        %endif
        %if %{with_uml}
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.uml
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/uml/
%ghost %dir %{_localstatedir}/run/libvirt/uml/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/uml/
        %endif
        %if %{with_libxl}
%config(noreplace) %{_sysconfdir}/libvirt/libxl.conf
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/libxl/
%ghost %dir %{_localstatedir}/run/libvirt/libxl/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/libxl/
%{_datadir}/augeas/lenses/libvirtd_libxl.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_libxl.aug
        %endif
        %if %{with_xen}
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/xen/
        %endif
    %endif # ! %{with_driver_modules}

    %if %{with_network}
%files daemon-config-network
%defattr(-, root, root)
%dir %{_datadir}/libvirt/networks/
%{_datadir}/libvirt/networks/default.xml
    %endif

    %if %{with_nwfilter}
%files daemon-config-nwfilter
%defattr(-, root, root)
%{_sysconfdir}/libvirt/nwfilter/*.xml
    %endif

    %if %{with_driver_modules}
        %if %{with_interface}
%files daemon-driver-interface
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_interface.so
        %endif

        %if %{with_network}
%files daemon-driver-network
%defattr(-, root, root)
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/autostart
%ghost %dir %{_localstatedir}/run/libvirt/network/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/network/
%dir %attr(0755, root, root) %{_localstatedir}/lib/libvirt/dnsmasq/
%attr(0755, root, root) %{_libexecdir}/libvirt_leaseshelper
%{_libdir}/%{name}/connection-driver/libvirt_driver_network.so
        %endif

        %if %{with_nodedev}
%files daemon-driver-nodedev
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_nodedev.so
        %endif

        %if %{with_nwfilter}
%files daemon-driver-nwfilter
%defattr(-, root, root)
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/nwfilter/
%ghost %dir %{_localstatedir}/run/libvirt/network/
%{_libdir}/%{name}/connection-driver/libvirt_driver_nwfilter.so
        %endif

%files daemon-driver-secret
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_secret.so

        %if %{with_storage}
%files daemon-driver-storage
%defattr(-, root, root)
            %if %{with_storage_disk}
%attr(0755, root, root) %{_libexecdir}/libvirt_parthelper
            %endif
%{_libdir}/%{name}/connection-driver/libvirt_driver_storage.so
        %endif

        %if %{with_qemu}
%files daemon-driver-qemu
%defattr(-, root, root)
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%config(noreplace) %{_sysconfdir}/libvirt/qemu.conf
%config(noreplace) %{_sysconfdir}/libvirt/qemu-lockd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.qemu
%ghost %dir %attr(0700, root, root) %{_localstatedir}/run/libvirt/qemu/
%dir %attr(0750, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/
%dir %attr(0750, %{qemu_user}, %{qemu_group}) %{_localstatedir}/cache/libvirt/qemu/
%{_datadir}/augeas/lenses/libvirtd_qemu.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
%{_libdir}/%{name}/connection-driver/libvirt_driver_qemu.so
        %endif

        %if %{with_lxc}
%files daemon-driver-lxc
%defattr(-, root, root)
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/lxc/
%config(noreplace) %{_sysconfdir}/libvirt/lxc.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.lxc
%ghost %dir %{_localstatedir}/run/libvirt/lxc/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/lxc/
%{_datadir}/augeas/lenses/libvirtd_lxc.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_lxc.aug
%attr(0755, root, root) %{_libexecdir}/libvirt_lxc
%{_libdir}/%{name}/connection-driver/libvirt_driver_lxc.so
        %endif

        %if %{with_uml}
%files daemon-driver-uml
%defattr(-, root, root)
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/uml/
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.uml
%ghost %dir %{_localstatedir}/run/libvirt/uml/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/uml/
%{_libdir}/%{name}/connection-driver/libvirt_driver_uml.so
        %endif

        %if %{with_xen}
%files daemon-driver-xen
%defattr(-, root, root)
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/xen/
%{_libdir}/%{name}/connection-driver/libvirt_driver_xen.so
        %endif

        %if %{with_libxl}
%files daemon-driver-libxl
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/libvirt/libxl.conf
%config(noreplace) %{_sysconfdir}/libvirt/libxl-lockd.conf
%if %{with_sanlock}
%config(noreplace) %{_sysconfdir}/libvirt/libxl-sanlock.conf
%endif
%{_datadir}/augeas/lenses/libvirtd_libxl.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_libxl.aug
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/libxl/
%ghost %dir %{_localstatedir}/run/libvirt/libxl/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/libxl/
%{_libdir}/%{name}/connection-driver/libvirt_driver_libxl.so
        %endif

        %if %{with_vbox}
%files daemon-driver-vbox
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_vbox.so
        %endif
    %endif # %{with_driver_modules}

    %if %{with_qemu_tcg}
%files daemon-qemu
%defattr(-, root, root)
    %endif

    %if %{with_qemu_kvm}
%files daemon-kvm
%defattr(-, root, root)
    %endif

    %if %{with_lxc}
%files daemon-lxc
%defattr(-, root, root)
    %endif

    %if %{with_uml}
%files daemon-uml
%defattr(-, root, root)
    %endif

    %if %{with_xen} || %{with_libxl}
%files daemon-xen
%defattr(-, root, root)
    %endif

    %if %{with_vbox}
%files daemon-vbox
%defattr(-, root, root)
    %endif
%endif # %{with_libvirtd}

%if %{with_sanlock}
%files lock-sanlock
%defattr(-, root, root)
    %if %{with_qemu}
%config(noreplace) %{_sysconfdir}/libvirt/qemu-sanlock.conf
    %endif
%attr(0755, root, root) %{_libdir}/libvirt/lock-driver/sanlock.so
%{_datadir}/augeas/lenses/libvirt_sanlock.aug
%{_datadir}/augeas/lenses/tests/test_libvirt_sanlock.aug
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/sanlock
%{_sbindir}/virt-sanlock-cleanup
%{_mandir}/man8/virt-sanlock-cleanup.8*
%attr(0755, root, root) %{_libexecdir}/libvirt_sanlock_helper
%endif

%files client -f %{name}.lang
%defattr(-, root, root)
%doc COPYING COPYING.LESSER

%config(noreplace) %{_sysconfdir}/libvirt/libvirt.conf
%{_mandir}/man1/virsh.1*
%{_mandir}/man1/virt-xml-validate.1*
%{_mandir}/man1/virt-pki-validate.1*
%{_mandir}/man1/virt-host-validate.1*
%{_bindir}/virsh
%{_bindir}/virt-xml-validate
%{_bindir}/virt-pki-validate
%{_bindir}/virt-host-validate
%{_libdir}/libvirt.so.*
%{_libdir}/libvirt-qemu.so.*
%{_libdir}/libvirt-lxc.so.*

%if %{with_dtrace}
%{_datadir}/systemtap/tapset/libvirt_probes*.stp
%{_datadir}/systemtap/tapset/libvirt_qemu_probes*.stp
%{_datadir}/systemtap/tapset/libvirt_functions.stp
%endif

%dir %{_datadir}/libvirt/
%dir %{_datadir}/libvirt/schemas/

%{_datadir}/libvirt/schemas/basictypes.rng
%{_datadir}/libvirt/schemas/capability.rng
%{_datadir}/libvirt/schemas/domain.rng
%{_datadir}/libvirt/schemas/domaincaps.rng
%{_datadir}/libvirt/schemas/domaincommon.rng
%{_datadir}/libvirt/schemas/domainsnapshot.rng
%{_datadir}/libvirt/schemas/interface.rng
%{_datadir}/libvirt/schemas/network.rng
%{_datadir}/libvirt/schemas/networkcommon.rng
%{_datadir}/libvirt/schemas/nodedev.rng
%{_datadir}/libvirt/schemas/nwfilter.rng
%{_datadir}/libvirt/schemas/secret.rng
%{_datadir}/libvirt/schemas/storagecommon.rng
%{_datadir}/libvirt/schemas/storagepool.rng
%{_datadir}/libvirt/schemas/storagevol.rng

%{_datadir}/libvirt/cpu_map.xml
%{_datadir}/libvirt/libvirtLogo.png

%if %{with_systemd}
%{_unitdir}/libvirt-guests.service
%else
%{_sysconfdir}/rc.d/init.d/libvirt-guests
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/libvirt-guests
%attr(0755, root, root) %{_libexecdir}/libvirt-guests.sh
%dir %attr(0755, root, root) %{_localstatedir}/lib/libvirt/

%if %{with_sasl}
%config(noreplace) %{_sysconfdir}/sasl2/libvirt.conf
%endif

%if %{with_wireshark}
%files wireshark
%{_libdir}/wireshark/plugins/*/libvirt.so
%endif

%if %{with_lxc}
%files login-shell
%attr(4750, root, virtlogin) %{_bindir}/virt-login-shell
%config(noreplace) %{_sysconfdir}/libvirt/virt-login-shell.conf
%{_mandir}/man1/virt-login-shell.1*
%endif

%files devel
%defattr(-, root, root)

%{_libdir}/libvirt.so
%{_libdir}/libvirt-qemu.so
%{_libdir}/libvirt-lxc.so
%dir %{_includedir}/libvirt
%{_includedir}/libvirt/virterror.h
%{_includedir}/libvirt/libvirt.h
%{_includedir}/libvirt/libvirt-domain.h
%{_includedir}/libvirt/libvirt-domain-snapshot.h
%{_includedir}/libvirt/libvirt-event.h
%{_includedir}/libvirt/libvirt-host.h
%{_includedir}/libvirt/libvirt-interface.h
%{_includedir}/libvirt/libvirt-network.h
%{_includedir}/libvirt/libvirt-nodedev.h
%{_includedir}/libvirt/libvirt-nwfilter.h
%{_includedir}/libvirt/libvirt-secret.h
%{_includedir}/libvirt/libvirt-storage.h
%{_includedir}/libvirt/libvirt-stream.h
%{_includedir}/libvirt/libvirt-qemu.h
%{_includedir}/libvirt/libvirt-lxc.h
%{_libdir}/pkgconfig/libvirt.pc
%{_libdir}/pkgconfig/libvirt-qemu.pc
%{_libdir}/pkgconfig/libvirt-lxc.pc

%dir %{_datadir}/libvirt/api/
%{_datadir}/libvirt/api/libvirt-api.xml
%{_datadir}/libvirt/api/libvirt-qemu-api.xml
%{_datadir}/libvirt/api/libvirt-lxc-api.xml

%doc docs/*.html docs/html docs/*.gif
%doc docs/libvirt-api.xml
%doc examples/hellolibvirt
%doc examples/object-events
%doc examples/dominfo
%doc examples/domsuspend
%doc examples/dommigrate
%doc examples/openauth
%doc examples/xml
%doc examples/systemtap

%changelog
* Thu Sep 10 2015 George Dunlap <george.dunlap@eu.citrix.com> - 1.2.15-4
- Port to aarch64

* Thu May 18 2015 George Dunlap <george.dunlap@eu.citrix.com> - 1.2.15-3
- Turn on with_xen and with_libxl for RHEL (CentOS)

* Thu May 07 2015 Richard W.M. Jones <rjones@redhat.com> - 1.2.15-2
- Add Cole Robinson's patch to fix arch selection (bz# 1219198, bz#1219191)

* Mon May 04 2015 Cole Robinson <crobinso@redhat.com> - 1.2.15-1
- Rebased to version 1.2.15

* Wed Apr 15 2015 Cole Robinson <crobinso@redhat.com> - 1.2.14-2
- Fix LXC domain startup (bz #1210397)
- Fix race starting multiple session daemons (bz #1200149)
- Fix change-media success messages
- Strip invalid control codes from XML (bz #1066564, bz #1184131)

* Thu Apr 02 2015 Cole Robinson <crobinso@redhat.com> - 1.2.14-1
- Rebased to version 1.2.14

* Tue Mar 10 2015 Cole Robinson <crobinso@redhat.com> - 1.2.13-2
- Fix connecting to qemu:///session (bz #1198244)

* Mon Mar 02 2015 Cole Robinson <crobinso@redhat.com> - 1.2.13-1
- Rebased to version 1.2.13
- lot of improvements around NUMA code
- a lot of improvement and bug fixes

* Tue Feb  3 2015 Daniel P. Berrange <berrange@redhat.com> - 1.2.12-2
- Rebuild for changed xen soname

* Tue Jan 27 2015 Daniel P. Berrange <berrange@redhat.com> - 1.2.12-1
- Update to 1.2.12 release

* Mon Dec 15 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.11-1
- Update to 1.2.11 release
- Use git to apply patches

* Fri Nov 21 2014 Cole Robinson <crobinso@redhat.com> - 1.2.10-3
- Allow arm/aarch64 with UEFI

* Sat Nov 15 2014 Cole Robinson <crobinso@redhat.com> - 1.2.10-2
- Fix caps probing when KVM is disabled (bz #1160318)
- ppc64le fixes (bz #1163439)

* Mon Nov  3 2014 Daniel Veillard <veillard@redhat.com> - 1.2.10
- upstream release

* Thu Oct 30 2014 Cole Robinson <crobinso@redhat.com> - 1.2.9-4
- Fix creating i686 guest with x86_64 emulator (bz #1153797)
- Fix tests with latest libxml2

* Thu Oct 09 2014 Cole Robinson <crobinso@redhat.com> - 1.2.9-3
- Fix selinux errors with /dev/net/tun (bz #1147057)

* Fri Oct 03 2014 Cole Robinson <crobinso@redhat.com> - 1.2.9-2
- Fix specifying CPU for qemu aarch64

* Wed Sep 24 2014 Cole Robinson <crobinso@redhat.com> - 1.2.8-6
- Fix labelling host devices (bz #1145968)

* Tue Sep 23 2014 Cole Robinson <crobinso@redhat.com> - 1.2.8-5
- Fix specifying CPU for qemu aarch64

* Thu Sep 18 2014 Cole Robinson <crobinso@redhat.com> - 1.2.8-4
- Don't mess up labelling of /dev/net/tun (bz #1141879)
- pflash/nvram support for UEFI/OVMF

* Wed Sep 17 2014 Cole Robinson <crobinso@redhat.com> - 1.2.8-3
- Fix preun script (bz #1142367)

* Mon Sep 15 2014 Cole Robinson <crobinso@redhat.com> - 1.2.8-2
- Generate non-colliding network IP range at RPM install time (bz #811967)
- Fix directory creation at session daemon startup (bz #1139672)
- Disable wireshark building, currently broken on f21/rawhide

* Fri Sep  5 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.8-1
- Update to 1.2.8 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Cole Robinson <crobinso@redhat.com> - 1.2.7-1
- Rebased to version 1.2.7

* Tue Jul 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.6-2
- Enable kvm on aarch64
- Cleanup F-16/18 conditionals

* Wed Jul  2 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.6-1
- Update to 1.2.6 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun  2 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.5-1
- Update to 1.2.5 release

* Tue May  6 2014 Cole Robinson <berrange@redhat.com> - 1.2.4-1
- Update to 1.2.4 release

* Fri Apr 11 2014 Cole Robinson <crobinso@redhat.com> - 1.2.3-2
- Fix LXC from throwing error System lacks NETNS support (bz #1084902)

* Tue Apr 01 2014 Cole Robinson <crobinso@redhat.com> - 1.2.3-1
- Rebased to version 1.2.3

* Mon Mar 24 2014 Cole Robinson <crobinso@redhat.com> - 1.2.2-2
- Rebuild for xen 4.4

* Mon Mar  3 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.2-1
- Update to 1.2.2 release
- Add wireshark plugin sub-RPM
- Add missing sub-RPMs deps for config packages

* Mon Jan 27 2014 Cole Robinson <crobinso@redhat.com> - 1.2.1-2
- Rebuild for openwsman soname bump

* Tue Jan 21 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.1-1
- Update to 1.2.1 release

* Mon Dec  2 2013 Daniel P. Berrange <berrange@redhat.com> - 1.2.0-1
- Update to 1.2.0 release with python in a separate srpm

* Tue Nov 12 2013 Cole Robinson <crobinso@redhat.com> - 1.1.4-2
- virsh nodedev-detach fails if device has no driver (bz #1028629)

* Mon Nov  4 2013 Daniel Veillard <veillard@redhat.com> - 1.1.4-1
- upstream release of 1.1.4
- Add support for AArch64 architecture
- Various improvements on test code and test driver
- a lot of bug fixes and various improvements

* Sun Oct 06 2013 Cole Robinson <crobinso@redhat.com> - 1.1.3-2
- Allow QoS change with update-device (bz #1014200)
- Fix nwfilter crash during firewalld install (bz #1014762)
- Fix crash with nographics (bz #1014088)

* Tue Oct  1 2013 Daniel Veillard <veillard@redhat.com> - 1.1.3-1
- VMware: Initial VMware Fusion support and various improvements
- libvirt: add new public API virConnectGetCPUModelNames
- various libxl driver improvements
- LXC many container driver improvement
- ARM cpu improvements
- a lot of bug and leak fixes and various improvements

* Tue Sep 24 2013 Cole Robinson <crobinso@redhat.com> - 1.1.2-4
- Fix snapshot restore when VM has disabled usb support (bz #1011520)

* Mon Sep 23 2013 Cole Robinson <crobinso@redhat.com> - 1.1.2-3
- Sync with v1.1.2-maint
- Rebuild for libswan soname bump (bz #1009701)
- CVE-2013-4311: Insecure polkit usage (bz #1009539, bz #1005332)
- CVE-2013-4296: Invalid free memory stats (bz #1006173, bz #1009667)
- CVE-2013-4297: Invalid free in NBDDeviceAssociate (bz #1006505, bz #1006511)
- Fix virsh block-commit abort (bz #1010056)

* Wed Sep 18 2013 Daniel P. Berrange <berrange@redhat.com> - 1.1.2-2
- Rebuild for soname break in openswman package

* Mon Sep  2 2013 Daniel P. Berrange <berrange@redhat.com> - 1.1.2-1
- Update to 1.1.2 release

* Tue Aug 20 2013 Cole Robinson <crobinso@redhat.com> - 1.1.1-3
- Fix launching ARM guests on x86 (patches posted upstream, F20 feature)

* Wed Aug 14 2013 Cole Robinson <crobinso@redhat.com> - 1.1.1-2
- CVE-2013-4239: xen: memory corruption in legacy driver (bz #996241, bz
  #996244)

* Tue Jul 30 2013 Daniel P. Berrange <berrange@redhat.com> - 1.1.1-1
- Update to 1.1.1 release

* Sun Jul 28 2013 Dennis Gilmore <dennis@ausil.us> - 1.1.0-5
- fix doc path in libvirt-python

* Thu Jul 25 2013 Cole Robinson <crobinso@redhat.com> - 1.1.0-4
- CVE-2013-4153: Fix double free of returned JSON (bz #986408, bz #986383)
- CVE-2013-4154: Crash of libvirtd if guest agent not configured (bz #986386,
  bz #986406)

* Wed Jul 17 2013 Daniel P. Berrange <berrange@redhat.com> - 1.1.0-3
- Rebuild for change in Xen library ABI/soname

* Thu Jul 11 2013 Cole Robinson <crobinso@redhat.com> - 1.1.0-2
- CVE-2013-2230 libvirt: multiple registered events crash

* Mon Jul  1 2013 Daniel Veillard <veillard@redhat.com> - 1.1.0-1
- CVE-2013-2218: Fix crash listing network interfaces with filters
- Fine grained ACL support for the API
- Extensible migration APIs
- various improvements in the Xen driver
- agent based vCPU hotplug support
- various bug fixes and improvements including localizations

* Fri Jun 14 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.6-3
- Enable KVM support on ARM

* Sat Jun 08 2013 Cole Robinson <crobinso@redhat.com> - 1.0.6-2
- Drop bogus dep on vbox

* Mon Jun  3 2013 Daniel P. Berrange <berrange@redhat.com> - 1.0.6-1
- Update to 1.0.6 release

* Sun May 19 2013 Cole Robinson <crobinso@redhat.com> - 1.0.5.1-1
- Rebased to version 1.0.5.1
- Follow updated packaging guidelines for user alloc (bz #924501)
- CVE-2013-1962 Open files DoS (bz #963789, bz #953107)

* Tue May 14 2013 Cole Robinson <crobinso@redhat.com> - 1.0.5-3
- Fix stream operations like screenshot (bz #960879)

* Fri May  3 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.5-2
- Fix network driver when using qemu:///session (bz #958907).

* Thu May  2 2013 Daniel Veillard <veillard@redhat.com> - 1.0.5-1
- Update to 1.0.5 release
- add support for NVRAM device
- Add XML config for resource partitions
- Add support for TPM
- NPIV storage migration support
- various bug fixes and improvements including localizations

* Mon Apr  1 2013 Daniel Veillard <veillard@redhat.com> - 1.0.4-1
- Update to 1.0.4 release

* Tue Mar  5 2013 Daniel P. Berrange <berrange@redhat.com> - 1.0.3-1
- Update to 1.0.3 release

* Thu Feb 28 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-4
- Backport "qemu: check backing chains even when cgroup is omitted"
  (RHBZ#896685).
- Disable virnettlscontexttest which apparently fails because of
  a broken gnutls3.  Note since this patch touches Makefile.am, I
  have enabled autoreconf (enable_autotools).

* Tue Feb  5 2013 Daniel P. Berrange <berrange@redhat.com> - 1.0.2-2
- Fix missing python binding constants

* Fri Feb  1 2013 Daniel P. Berrange <berrange@redhat.com> - 1.0.2-1
- Update to 1.0.2 release

* Tue Jan 29 2013 Cole Robinson <crobinso@redhat.com> - 1.0.1-6
- Fix network persistence after define (bz #890492)

* Mon Jan 28 2013 Cole Robinson <crobinso@redhat.com> - 1.0.1-5
- CVE-2013-0170 libvirt: use-after-free in virNetMessageFree() (bz #893450, bz
  #905173)

* Sun Jan 20 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-4
- Rebuild for libnl soname breakage (RHBZ#901569).

* Fri Jan 18 2013 Daniel P. Berrange <berrange@redhat.com> - 1.0.1-3
- Rebuild for libnl3 soname change
- Deal with broken kernel headers

* Mon Dec 17 2012 Cole Robinson <crobinso@redhat.com> - 1.0.1-2
- Fix scriplet warning when uninstalling libvirt-client (bz #888071)

* Mon Dec 17 2012 Daniel Veillard <veillard@redhat.com> - 1.0.1-1
- Update to 1.0.1 release

* Thu Nov  8 2012 Daniel P. Berrange <berrange@redhat.com> - 1.0.0-1
- Update to 1.0.0 release

* Tue Oct 30 2012 Cole Robinson <crobinso@redhat.com> - 0.10.2.1-2
- Disable libxl on F18 too

* Sat Oct 27 2012 Cole Robinson <crobinso@redhat.com> - 0.10.2.1-1
- Rebased to version 0.10.2.1
- Fix lvm volume creation when alloc=0 (bz #866481)
- Clarify virsh send-keys man page example (bz #860004)
- Fix occasional deadlock via virDomainDestroy (bz #859009)
- Fix LXC deadlock from ctrl-c (bz #848119)
- Fix occasional selinux denials with macvtap (bz #798605)
- Fix multilib conflict with systemtap files (bz #831425)
- Don't trigger keytab warning in system logs (bz #745203)
- Fix qemu domxml-2-native NIC model out (bz #636832)
- Fix error message if not enough space for lvm vol (bz #609104)

* Thu Oct 25 2012 Cole Robinson <crobinso@redhat.com> - 0.10.2-4
- Disable libxl driver, since it doesn't build with xen 4.2 in rawhide

* Mon Sep 24 2012 Richard W.M. Jones <rjones@redhat.com> - 0.10.2-3
- Re-add Use-qemu-system-i386-as-binary-instead-of-qemu.patch
  NB: This patch is Fedora-specific and not upstream.
- Add upstream patches: don't duplicate environment variables (RHBZ#859596).

* Mon Sep 24 2012 Daniel Veillard <veillard@redhat.com> - 0.10.2-1
- Upstream release 0.10.2
- network: define new API virNetworkUpdate
- add support for QEmu sandbox support
- blockjob: add virDomainBlockCommit
- New APIs to get/set Node memory parameters
- new API virConnectListAllSecrets
- new API virConnectListAllNWFilters
- new API virConnectListAllNodeDevices
- parallels: add support of containers to the driver
- new API virConnectListAllInterfaces
- new API virConnectListAllNetworks
- new API virStoragePoolListAllVolumes
- Add PMSUSPENDED life cycle event
- new API virStorageListAllStoragePools
- Add per-guest S3/S4 state configuration
- qemu: Support for Block Device IO Limits
- a lot of bug fixes, improvements and portability work

* Fri Sep 21 2012 Richard W.M. Jones <rjones@redhat.com> - 0.10.1-5
- Add (upstream) patches to label sockets for SELinux (RHBZ#853393).

* Thu Sep 13 2012 Richard W.M. Jones <rjones@redhat.com> - 0.10.1-4
- Fix for 32 bit qemu renamed to qemu-system-i386 (RHBZ#857026).

* Wed Sep 12 2012 Cole Robinson <crobinso@redhat.com> - 0.10.1-3
- Fix libvirtd segfault with old netcf-libs (bz 853381)
- Drop unneeded dnsmasq --filterwin2k
- Fix unwanted connection closing, needed for boxes

* Wed Sep  5 2012 Daniel P. Berrange <berrange@redhat.com> - 0.10.1-2
- Remove dep on ceph RPM (rhbz #854360)

* Fri Aug 31 2012 Daniel Veillard <veillard@redhat.com> - 0.10.1-1
- upstream release of 0.10.1
- many fixes from 0.10.0

* Wed Aug 29 2012 Daniel Veillard <veillard@redhat.com> - 0.10.0-1
- upstream release of 0.10.0
- agent: add qemuAgentArbitraryCommand() for general qemu agent command
- Introduce virDomainPinEmulator and virDomainGetEmulatorPinInfo functions
- network: use firewalld instead of iptables, when available
- network: make network driver vlan-aware
- esx: Implement network driver
- driver for parallels hypervisor
- Various LXC improvements
- Add virDomainGetHostname
- a lot of bug fixes, improvements and portability work

* Thu Aug 23 2012 Daniel Veillard <veillard@redhat.com> - 0.10.0-0rc1
- release candidate 1 of 0.10.0

* Tue Aug 14 2012 Daniel P. Berrange <berrange@redhat.com> - 0.10.0-0rc0.2
- Enable autotools to make previous patch work

* Tue Aug 14 2012 Daniel Veillard <veillard@redhat.com> - 0.10.0-0rc0.1
- fix security driver missing from the daemon

* Wed Aug  8 2012 Daniel Veillard <veillard@redhat.com> - 0.10.0-0rc0
- snapshot before 0.10.0 in a few weeks
- adds the parallel driver support

* Mon Jul 23 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.13-3
- Add upstream patch to fix RHBZ#842114.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Daniel Veillard <veillard@redhat.com> - 0.9.13-1
- S390: support for s390(x)
- snapshot: implement new APIs for esx and vbox
- snapshot: new query APIs and many improvements
- virsh: Allow users to reedit rejected XML
- nwfilter: add DHCP snooping
- Enable driver modules in libvirt RPM
- Default to enable driver modules for libvirtd
- storage backend: Add RBD (RADOS Block Device) support
- sVirt support for LXC domains inprovement
- a lot of bug fixes, improvements and portability work

* Mon May 14 2012 Daniel Veillard <veillard@redhat.com> - 0.9.12-1
- qemu: allow snapshotting of sheepdog and rbd disks
- blockjob: add new APIs
- a lot of bug fixes, improvements and portability work

* Thu Apr 26 2012 Cole Robinson <crobinso@redhat.com> - 0.9.11.3-1
- Rebased to version 0.9.11.3
- Abide URI username when connecting to hypervisor (bz 811397)
- Fix managed USB mode (bz 814866)
- Fix crash connecting to ESX host (bz 811891)

* Wed Apr  4 2012 Daniel P. Berrange <berrange@redhat.com> - 0.9.11-1
- Update to 0.9.11 release

* Tue Apr  3 2012 Daniel P. Berrange <berrange@redhat.com> - 0.9.10-4
- Revert previous change

* Sat Mar 31 2012 Daniel P. Berrange <berrange@redhat.com> - 0.9.10-3
- Refactor RPM spec to allow install without default configs

* Thu Mar 15 2012 Daniel P. Berrange <berrange@redhat.com> - 0.9.10-2
- Rebuild for libparted soname break

* Mon Feb 13 2012 Daniel P. Berrange <berrange@redhat.com> - 0.9.10-1
- Update to 0.9.10

* Thu Jan 12 2012 Daniel P. Berrange <berrange@redhat.com> - 0.9.9-2
- Fix LXC I/O handling

* Sat Jan  7 2012 Daniel Veillard <veillard@redhat.com> - 0.9.9-1
- Add API virDomain{S,G}etInterfaceParameters
- Add API virDomain{G, S}etNumaParameters
- Add support for ppc64 qemu
- Support Xen domctl v8
- many improvements and bug fixes

* Thu Dec  8 2011 Daniel P. Berrange <berrange@redhat.com> - 0.9.8-2
- Fix install of libvirt-guests.service & libvirtd.service

* Thu Dec  8 2011 Daniel Veillard <veillard@redhat.com> - 0.9.8-1
- Add support for QEMU 1.0
- Add preliminary PPC cpu driver
- Add new API virDomain{Set, Get}BlockIoTune
- block_resize: Define the new API
- Add a public API to invoke suspend/resume on the host
- various improvements for LXC containers
- Define keepalive protocol and add virConnectIsAlive API
- Add support for STP and VLAN filtering
- many improvements and bug fixes

* Mon Nov 14 2011 Justin M. Forbes <jforbes@redhat.com> - 0.9.7-3
- Remove versioned buildreq for yajl as 2.0.x features are not required.

* Thu Nov 10 2011 Daniel P. Berrange <berrange@redhat.com> - 0.9.7-2
- Rebuild for yajl 2.0.1

* Tue Nov  8 2011 Daniel P. Berrange <berrange@redhat.com> - 0.9.7-1
- Update to 0.9.7 release

* Tue Oct 11 2011 Dan Horák <dan[at]danny.cz> - 0.9.6-3
- xenlight available only on Xen arches (#745020)

* Mon Oct  3 2011 Laine Stump <laine@redhat.com> - 0.9.6-2
- Make PCI multifunction support more manual - Bug 742836
- F15 build still uses cgconfig - Bug 738725

* Thu Sep 22 2011 Daniel Veillard <veillard@redhat.com> - 0.9.6-1
- Fix the qemu reboot bug and a few others bug fixes

* Tue Sep 20 2011 Daniel Veillard <veillard@redhat.com> - 0.9.5-1
- many snapshot improvements (Eric Blake)
- latency: Define new public API and structure (Osier Yang)
- USB2 and various USB improvements (Marc-André Lureau)
- storage: Add fs pool formatting (Osier Yang)
- Add public API for getting migration speed (Jim Fehlig)
- Add basic driver for Microsoft Hyper-V (Matthias Bolte)
- many improvements and bug fixes

* Wed Aug  3 2011 Daniel Veillard <veillard@redhat.com> - 0.9.4-1
- network bandwidth QoS control
- Add new API virDomainBlockPull*
- save: new API to manipulate save file images
- CPU bandwidth limits support
- allow to send NMI and key event to guests
- new API virDomainUndefineFlags
- Implement code to attach to external QEMU instances
- bios: Add support for SGA
- various missing python binding
- many improvements and bug fixes

* Sat Jul 30 2011 Dan Hor?k <dan[at]danny.cz> - 0.9.3-3
- xenlight available only on Xen arches

* Wed Jul  6 2011 Peter Robinson <pbrobinson@gmail.com> - 0.9.3-2
- Add ARM to NUMA platform excludes

* Mon Jul  4 2011 Daniel Veillard <veillard@redhat.com> - 0.9.3-1
- new API virDomainGetVcpupinInfo
- Add TXT record support for virtual DNS service
- Support reboots with the QEMU driver
- New API virDomainGetControlInfo API
- New API virNodeGetMemoryStats
- New API virNodeGetCPUTime
- New API for send-key
- New API virDomainPinVcpuFlags
- support multifunction PCI device
- lxc: various improvements
- many improvements and bug fixes

* Wed Jun 29 2011 Richard W.M. Jones <rjones@redhat.com> - 0.9.2-3
- Rebuild because of libparted soname bump (libparted.so.0 -> libparted.so.1).

* Tue Jun 21 2011 Laine Stump <laine@redhat.com> - 0.9.2-2
- add rule to require netcf-0.1.8 during build so that new transactional
  network change APIs are included.
- document that CVE-2011-2178 has been fixed (by virtue of rebase
  to 0.9.2 - see https://bugzilla.redhat.com/show_bug.cgi?id=709777)

* Mon Jun  6 2011 Daniel Veillard <veillard@redhat.com> - 0.9.2-1
- Framework for lock manager plugins
- API for network config change transactions
- flags for setting memory parameters
- virDomainGetState public API
- qemu: allow blkstat/blkinfo calls during migration
- Introduce migration v3 API
- Defining the Screenshot public API
- public API for NMI injection
- Various improvements and bug fixes

* Wed May 25 2011 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-3
- Add upstream patches:
    0001-json-Avoid-passing-large-positive-64-bit-integers-to.patch
    0001-qemudDomainMemoryPeek-change-ownership-selinux-label.patch
    0002-remote-remove-bogus-virDomainFree.patch
  so that users can try out virt-dmesg.
- Change /var/cache mode to 0711.

* Thu May  5 2011 Daniel Veillard <veillard@redhat.com> - 0.9.1-1
- support various persistent domain updates
- improvements on memory APIs
- Add virDomainEventRebootNew
- various improvements to libxl driver
- Spice: support audio, images and stream compression
- Various improvements and bug fixes

* Thu Apr  7 2011 Daniel Veillard <veillard@redhat.com> - 0.9.0-1
- Support cputune cpu usage tuning
- Add public APIs for storage volume upload/download
- Add public API for setting migration speed on the fly
- Add libxenlight driver
- qemu: support migration to fd
- libvirt: add virDomain{Get,Set}BlkioParameters
- setmem: introduce a new libvirt API (virDomainSetMemoryFlags)
- Expose event loop implementation as a public API
- Dump the debug buffer to libvirtd.log on fatal signal
- Audit support
- Various improvements and bug fixes

* Mon Mar 14 2011 Daniel Veillard <veillard@redhat.com> - 0.8.8-3
- fix a lack of API check on read-only connections
- CVE-2011-1146

* Mon Feb 21 2011 Daniel P. Berrange <berrange@redhat.com> - 0.8.8-2
- Fix kernel boot with latest QEMU

* Thu Feb 17 2011 Daniel Veillard <veillard@redhat.com> - 0.8.8-1
- expose new API for sysinfo extraction
- cgroup blkio weight support
- smartcard device support
- qemu: Support per-device boot ordering
- Various improvements and bug fixes

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Daniel Veillard <veillard@redhat.com> - 0.8.7-1
- Preliminary support for VirtualBox 4.0
- IPv6 support
- Add VMware Workstation and Player driver driver
- Add network disk support
- Various improvements and bug fixes
- from 0.8.6:
- Add support for iSCSI target auto-discovery
- QED: Basic support for QED images
- remote console support
- support for SPICE graphics
- sysinfo and VMBIOS support
- virsh qemu-monitor-command
- various improvements and bug fixes

* Fri Oct 29 2010 Daniel Veillard <veillard@redhat.com> - 0.8.5-1
- Enable JSON and netdev features in QEMU >= 0.13
- framework for auditing integration
- framework DTrace/SystemTap integration
- Setting the number of vcpu at boot
- Enable support for nested SVM
- Virtio plan9fs filesystem QEMU
- Memory parameter controls
- various improvements and bug fixes

* Wed Sep 29 2010 jkeating - 0.8.4-3
- Rebuilt for gcc bug 634757

* Thu Sep 16 2010 Dan Horák <dan[at]danny.cz> - 0.8.4-2
- disable the nwfilterxml2xmltest also on s390(x)

* Mon Sep 13 2010 Daniel Veillard <veillard@redhat.com> - 0.8.4-1
- Upstream release 0.8.4

* Mon Aug 23 2010 Daniel P. Berrange <berrange@redhat.com> - 0.8.3-2
- Fix potential overflow in boot menu code

* Mon Aug 23 2010 Daniel P. Berrange <berrange@redhat.com> - 0.8.3-1
- Upstream release 0.8.3

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 12 2010 Daniel P. Berrange <berrange@redhat.com> - 0.8.2-2
- CVE-2010-2237 ignoring defined main disk format when looking up disk backing stores
- CVE-2010-2238 ignoring defined disk backing store format when recursing into disk
  image backing stores
- CVE-2010-2239 not setting user defined backing store format when creating new image
- CVE-2010-2242 libvirt: improperly mapped source privileged ports may allow for
  obtaining privileged resources on the host

* Mon Jul  5 2010 Daniel Veillard <veillard@redhat.com> - 0.8.2-1
- Upstream release 0.8.2
- phyp: adding support for IVM
- libvirt: introduce domainCreateWithFlags API
- add 802.1Qbh and 802.1Qbg switches handling
- Support for VirtualBox version 3.2
- Init script for handling guests on shutdown/boot
- qemu: live migration with non-shared storage for kvm

* Fri Apr 30 2010 Daniel Veillard <veillard@redhat.com> - 0.8.1-1
- Upstream release 0.8.1
- Starts dnsmasq from libvirtd with --dhcp-hostsfile
- Add virDomainGetBlockInfo API to query disk sizing
- a lot of bug fixes and cleanups

* Mon Apr 12 2010 Daniel Veillard <veillard@redhat.com> - 0.8.0-1
- Upstream release 0.8.0
- Snapshotting support (QEmu/VBox/ESX)
- Network filtering API
- XenAPI driver
- new APIs for domain events
- Libvirt managed save API
- timer subselection for domain clock
- synchronous hooks
- API to update guest CPU to host CPU
- virDomainUpdateDeviceFlags new API
- migrate max downtime API
- volume wiping API
- and many bug fixes

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 0.7.7-3.fc14
- No change, just rebuild against new libparted with bumped soname.

* Mon Mar 22 2010 Cole Robinson <crobinso@redhat.com> - 0.7.7-2.fc14
- Fix USB devices by product with security enabled (bz 574136)
- Set kernel/initrd in security driver, fixes some URL installs (bz 566425)

* Fri Mar  5 2010 Daniel Veillard <veillard@redhat.com> - 0.7.7-1
- macvtap support
- async job handling
- virtio channel
- computing baseline CPU
- virDomain{Attach,Detach}DeviceFlags
- assorted bug fixes and lots of cleanups

* Tue Feb 16 2010 Adam Jackson <ajax@redhat.com> 0.7.6-2
- libvirt-0.7.6-add-needed.patch: Fix FTBFS from --no-add-needed
- Add BuildRequires: xmlrpc-c-client for libxmlrpc_client.so

* Wed Feb  3 2010 Daniel Veillard <veillard@redhat.com> - 0.7.6-1
- upstream release of 0.7.6
- Use QEmu new device adressing when possible
- Implement CPU topology support for QEMU driver
- Implement SCSI controller hotplug/unplug for QEMU
- Implement support for multi IQN
- a lot of fixes and improvements

* Thu Jan 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.7.5-3
- bump for libssh2 rebuild

* Tue Jan 12 2010 Daniel P. Berrange <berrange@redhat.com> - 0.7.5-2
- Rebuild for libparted soname change

* Wed Dec 23 2009 Daniel Veillard <veillard@redhat.com> - 0.7.5-1
- Add new API virDomainMemoryStats
- Public API and domain extension for CPU flags
- vbox: Add support for version 3.1
- Support QEMU's virtual FAT block device driver
- a lot of fixes

* Fri Nov 20 2009 Daniel Veillard <veillard@redhat.com> - 0.7.4-1
- upstream release of 0.7.4
- udev node device backend
- API to check object properties
- better QEmu monitor processing
- MAC address based port filtering for qemu
- support IPv6 and multiple addresses per interfaces
- a lot of fixes

* Thu Nov 19 2009 Daniel P. Berrange <berrange@redhat.com> - 0.7.2-6
- Really fix restore file labelling this time

* Wed Nov 11 2009 Daniel P. Berrange <berrange@redhat.com> - 0.7.2-5
- Disable numactl on s390[x]. Again.

* Wed Nov 11 2009 Daniel P. Berrange <berrange@redhat.com> - 0.7.2-4
- Fix QEMU save/restore permissions / labelling

* Thu Oct 29 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.2-3
- Avoid compressing small log files (#531030)

* Thu Oct 29 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.2-2
- Make libvirt-devel require libvirt-client, not libvirt
- Fix qemu machine types handling

* Wed Oct 14 2009 Daniel Veillard <veillard@redhat.com> - 0.7.2-1
- Upstream release of 0.7.2
- Allow to define ESX domains
- Allows suspend and resulme of LXC domains
- API for data streams
- many bug fixes

* Tue Oct 13 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-12
- Fix restore of qemu guest using raw save format (#523158)

* Fri Oct  9 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-11
- Fix libvirtd memory leak during error reply sending (#528162)
- Add several PCI hot-unplug typo fixes from upstream

* Tue Oct  6 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-10
- Create /var/log/libvirt/{lxc,uml} dirs for logrotate
- Make libvirt-python dependon on libvirt-client
- Sync misc minor changes from upstream spec

* Tue Oct  6 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-9
- Change logrotate config to weekly (#526769)

* Thu Oct  1 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-8
- Disable sound backend, even when selinux is disabled (#524499)
- Re-label qcow2 backing files (#497131)

* Wed Sep 30 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-7
- Fix USB device passthrough (#522683)

* Mon Sep 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.7.1-6
- rebuild for libssh2 1.2

* Mon Sep 21 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-5
- Don't set a bogus error in virDrvSupportsFeature()
- Fix raw save format

* Thu Sep 17 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-4
- A couple of hot-unplug memory handling fixes (#523953)

* Thu Sep 17 2009 Daniel Veillard <veillard@redhat.com> - 0.7.1-3
- disable numactl on s390[x]

* Thu Sep 17 2009 Daniel Veillard <veillard@redhat.com> - 0.7.1-2
- revamp of spec file for modularity and RHELs

* Tue Sep 15 2009 Daniel Veillard <veillard@redhat.com> - 0.7.1-1
- Upstream release of 0.7.1
- ESX, VBox driver updates
- mutipath support
- support for encrypted (qcow) volume
- compressed save image format for Qemu/KVM
- QEmu host PCI device hotplug support
- configuration of huge pages in guests
- a lot of fixes

* Mon Sep 14 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-0.2.gitfac3f4c
- Update to newer snapshot of 0.7.1
- Stop libvirt using untrusted 'info vcpus' PID data (#520864)
- Support relabelling of USB and PCI devices
- Enable multipath storage support
- Restart libvirtd upon RPM upgrade

* Sun Sep  6 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-0.1.gitg3ef2e05
- Update to pre-release git snapshot of 0.7.1
- Drop upstreamed patches

* Wed Aug 19 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.0-6
- Fix migration completion with newer versions of qemu (#516187)

* Wed Aug 19 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.0-5
- Add PCI host device hotplug support
- Allow PCI bus reset to reset other devices (#499678)
- Fix stupid PCI reset error message (bug #499678)
- Allow PM reset on multi-function PCI devices (bug #515689)
- Re-attach PCI host devices after guest shuts down (bug #499561)
- Fix list corruption after disk hot-unplug
- Fix minor 'virsh nodedev-list --tree' annoyance

* Thu Aug 13 2009 Daniel P. Berrange <berrange@redhat.com> - 0.7.0-4
- Rewrite policykit support (rhbz #499970)
- Log and ignore NUMA topology problems (rhbz #506590)

* Mon Aug 10 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.0-3
- Don't fail to start network if ipv6 modules is not loaded (#516497)

* Thu Aug  6 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.0-2
- Make sure qemu can access kernel/initrd (bug #516034)
- Set perms on /var/lib/libvirt/boot to 0711 (bug #516034)

* Wed Aug  5 2009 Daniel Veillard <veillard@redhat.com> - 0.7.0-1
- ESX, VBox3, Power Hypervisor drivers
- new net filesystem glusterfs
- Storage cloning for LVM and Disk backends
- interface implementation based on netcf
- Support cgroups in QEMU driver
- QEmu hotplug NIC support
- a lot of fixes

* Fri Jul  3 2009 Daniel Veillard <veillard@redhat.com> - 0.6.5-1
- release of 0.6.5

* Fri May 29 2009 Daniel Veillard <veillard@redhat.com> - 0.6.4-1
- release of 0.6.4
- various new APIs

* Fri Apr 24 2009 Daniel Veillard <veillard@redhat.com> - 0.6.3-1
- release of 0.6.3
- VirtualBox driver

* Fri Apr  3 2009 Daniel Veillard <veillard@redhat.com> - 0.6.2-1
- release of 0.6.2

* Wed Mar  4 2009 Daniel Veillard <veillard@redhat.com> - 0.6.1-1
- release of 0.6.1

* Sat Jan 31 2009 Daniel Veillard <veillard@redhat.com> - 0.6.0-1
- release of 0.6.0

* Tue Nov 25 2008 Daniel Veillard <veillard@redhat.com> - 0.5.0-1
- release of 0.5.0

* Tue Sep 23 2008 Daniel Veillard <veillard@redhat.com> - 0.4.6-1
- release of 0.4.6

* Mon Sep  8 2008 Daniel Veillard <veillard@redhat.com> - 0.4.5-1
- release of 0.4.5

* Wed Jun 25 2008 Daniel Veillard <veillard@redhat.com> - 0.4.4-1
- release of 0.4.4
- mostly a few bug fixes from 0.4.3

* Thu Jun 12 2008 Daniel Veillard <veillard@redhat.com> - 0.4.3-1
- release of 0.4.3
- lots of bug fixes and small improvements

* Tue Apr  8 2008 Daniel Veillard <veillard@redhat.com> - 0.4.2-1
- release of 0.4.2
- lots of bug fixes and small improvements

* Mon Mar  3 2008 Daniel Veillard <veillard@redhat.com> - 0.4.1-1
- Release of 0.4.1
- Storage APIs
- xenner support
- lots of assorted improvements, bugfixes and cleanups
- documentation and localization improvements

* Tue Dec 18 2007 Daniel Veillard <veillard@redhat.com> - 0.4.0-1
- Release of 0.4.0
- SASL based authentication
- PolicyKit authentication
- improved NUMA and statistics support
- lots of assorted improvements, bugfixes and cleanups
- documentation and localization improvements

* Sun Sep 30 2007 Daniel Veillard <veillard@redhat.com> - 0.3.3-1
- Release of 0.3.3
- Avahi support
- NUMA support
- lots of assorted improvements, bugfixes and cleanups
- documentation and localization improvements

* Tue Aug 21 2007 Daniel Veillard <veillard@redhat.com> - 0.3.2-1
- Release of 0.3.2
- API for domains migration
- APIs for collecting statistics on disks and interfaces
- lots of assorted bugfixes and cleanups
- documentation and localization improvements

* Tue Jul 24 2007 Daniel Veillard <veillard@redhat.com> - 0.3.1-1
- Release of 0.3.1
- localtime clock support
- PS/2 and USB input devices
- lots of assorted bugfixes and cleanups
- documentation and localization improvements

* Mon Jul  9 2007 Daniel Veillard <veillard@redhat.com> - 0.3.0-1
- Release of 0.3.0
- Secure remote access support
- unification of daemons
- lots of assorted bugfixes and cleanups
- documentation and localization improvements

* Fri Jun  8 2007 Daniel Veillard <veillard@redhat.com> - 0.2.3-1
- Release of 0.2.3
- lot of assorted bugfixes and cleanups
- support for Xen-3.1
- new scheduler API

* Tue Apr 17 2007 Daniel Veillard <veillard@redhat.com> - 0.2.2-1
- Release of 0.2.2
- lot of assorted bugfixes and cleanups
- preparing for Xen-3.0.5

* Thu Mar 22 2007 Jeremy Katz <katzj@redhat.com> - 0.2.1-2.fc7
- don't require xen; we don't need the daemon and can control non-xen now
- fix scriptlet error (need to own more directories)
- update description text

* Fri Mar 16 2007 Daniel Veillard <veillard@redhat.com> - 0.2.1-1
- Release of 0.2.1
- lot of bug and portability fixes
- Add support for network autostart and init scripts
- New API to detect the virtualization capabilities of a host
- Documentation updates

* Fri Feb 23 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-4.fc7
- Fix loading of guest & network configs

* Fri Feb 16 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-3.fc7
- Disable kqemu support since its not in Fedora qemu binary
- Fix for -vnc arg syntax change in 0.9.0  QEMU

* Thu Feb 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-2.fc7
- Fixed path to qemu daemon for autostart
- Fixed generation of <features> block in XML
- Pre-create config directory at startup

* Wed Feb 14 2007 Daniel Veillard <veillard@redhat.com> 0.2.0-1.fc7
- support for KVM and QEmu
- support for network configuration
- assorted fixes

* Mon Jan 22 2007 Daniel Veillard <veillard@redhat.com> 0.1.11-1.fc7
- finish inactive Xen domains support
- memory leak fix
- RelaxNG schemas for XML configs

* Wed Dec 20 2006 Daniel Veillard <veillard@redhat.com> 0.1.10-1.fc7
- support for inactive Xen domains
- improved support for Xen display and vnc
- a few bug fixes
- localization updates

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.1.9-2
- rebuild against python 2.5

* Wed Nov 29 2006 Daniel Veillard <veillard@redhat.com> 0.1.9-1
- better error reporting
- python bindings fixes and extensions
- add support for shareable drives
- add support for non-bridge style networking
- hot plug device support
- added support for inactive domains
- API to dump core of domains
- various bug fixes, cleanups and improvements
- updated the localization

* Tue Nov  7 2006 Daniel Veillard <veillard@redhat.com> 0.1.8-3
- it's pkgconfig not pgkconfig !

* Mon Nov  6 2006 Daniel Veillard <veillard@redhat.com> 0.1.8-2
- fixing spec file, added %dist, -devel requires pkgconfig and xen-devel
- Resolves: rhbz#202320

* Mon Oct 16 2006 Daniel Veillard <veillard@redhat.com> 0.1.8-1
- fix missing page size detection code for ia64
- fix mlock size when getting domain info list from hypervisor
- vcpu number initialization
- don't label crashed domains as shut off
- fix virsh man page
- blktapdd support for alternate drivers like blktap
- memory leak fixes (xend interface and XML parsing)
- compile fix
- mlock/munlock size fixes

* Fri Sep 22 2006 Daniel Veillard <veillard@redhat.com> 0.1.7-1
- Fix bug when running against xen-3.0.3 hypercalls
- Fix memory bug when getting vcpus info from xend

* Fri Sep 22 2006 Daniel Veillard <veillard@redhat.com> 0.1.6-1
- Support for localization
- Support for new Xen-3.0.3 cdrom and disk configuration
- Support for setting VNC port
- Fix bug when running against xen-3.0.2 hypercalls
- Fix reconnection problem when talking directly to http xend

* Tue Sep  5 2006 Jeremy Katz <katzj@redhat.com> - 0.1.5-3
- patch from danpb to support new-format cd devices for HVM guests

* Tue Sep  5 2006 Daniel Veillard <veillard@redhat.com> 0.1.5-2
- reactivating ia64 support

* Tue Sep  5 2006 Daniel Veillard <veillard@redhat.com> 0.1.5-1
- new release
- bug fixes
- support for new hypervisor calls
- early code for config files and defined domains

* Mon Sep  4 2006 Daniel Berrange <berrange@redhat.com> - 0.1.4-5
- add patch to address dom0_ops API breakage in Xen 3.0.3 tree

* Mon Aug 28 2006 Jeremy Katz <katzj@redhat.com> - 0.1.4-4
- add patch to support paravirt framebuffer in Xen

* Mon Aug 21 2006 Daniel Veillard <veillard@redhat.com> 0.1.4-3
- another patch to fix network handling in non-HVM guests

* Thu Aug 17 2006 Daniel Veillard <veillard@redhat.com> 0.1.4-2
- patch to fix virParseUUID()

* Wed Aug 16 2006 Daniel Veillard <veillard@redhat.com> 0.1.4-1
- vCPUs and affinity support
- more complete XML, console and boot options
- specific features support
- enforced read-only connections
- various improvements, bug fixes

* Wed Aug  2 2006 Jeremy Katz <katzj@redhat.com> - 0.1.3-6
- add patch from pvetere to allow getting uuid from libvirt

* Wed Aug  2 2006 Jeremy Katz <katzj@redhat.com> - 0.1.3-5
- build on ia64 now

* Thu Jul 27 2006 Jeremy Katz <katzj@redhat.com> - 0.1.3-4
- don't BR xen, we just need xen-devel

* Thu Jul 27 2006 Daniel Veillard <veillard@redhat.com> 0.1.3-3
- need rebuild since libxenstore is now versionned

* Mon Jul 24 2006 Mark McLoughlin <markmc@redhat.com> - 0.1.3-2
- Add BuildRequires: xen-devel

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.1.3-1.1
- rebuild

* Tue Jul 11 2006 Daniel Veillard <veillard@redhat.com> 0.1.3-1
- support for HVM Xen guests
- various bugfixes

* Mon Jul  3 2006 Daniel Veillard <veillard@redhat.com> 0.1.2-1
- added a proxy mechanism for read only access using httpu
- fixed header includes paths

* Wed Jun 21 2006 Daniel Veillard <veillard@redhat.com> 0.1.1-1
- extend and cleanup the driver infrastructure and code
- python examples
- extend uuid support
- bug fixes, buffer handling cleanups
- support for new Xen hypervisor API
- test driver for unit testing
- virsh --conect argument

* Mon Apr 10 2006 Daniel Veillard <veillard@redhat.com> 0.1.0-1
- various fixes
- new APIs: for Node information and Reboot
- virsh improvements and extensions
- documentation updates and man page
- enhancement and fixes of the XML description format

* Tue Feb 28 2006 Daniel Veillard <veillard@redhat.com> 0.0.6-1
- added error handling APIs
- small bug fixes
- improve python bindings
- augment documentation and regression tests

* Thu Feb 23 2006 Daniel Veillard <veillard@redhat.com> 0.0.5-1
- new domain creation API
- new UUID based APIs
- more tests, documentation, devhelp
- bug fixes

* Fri Feb 10 2006 Daniel Veillard <veillard@redhat.com> 0.0.4-1
- fixes some problems in 0.0.3 due to the change of names

* Wed Feb  8 2006 Daniel Veillard <veillard@redhat.com> 0.0.3-1
- changed library name to libvirt from libvir, complete and test the python
  bindings

* Sun Jan 29 2006 Daniel Veillard <veillard@redhat.com> 0.0.2-1
- upstream release of 0.0.2, use xend, save and restore added, python bindings
  fixed

* Wed Nov  2 2005 Daniel Veillard <veillard@redhat.com> 0.0.1-1
- created

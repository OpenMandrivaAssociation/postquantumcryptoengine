%define major 1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

%bcond_with	static
%bcond_without	strict
%bcond_without	tests

# NOTE: use commit if the last release is still in beta
%global commit 8bdb9c1d3988a389af462c793189d11165733d2a

Summary:	Post Quantum algorithm integration to bctoolbox
Name:		postquantumcryptoengine
Version:	5.2.0
Release:	1
License:	GPLv3
Group:		System/Libraries
URL:		https://linphone.org/
#Source0:	https://gitlab.linphone.org/BC/public/Postquantumcryptoengine/-/archive/%{version}-beta/Postquantumcryptoengine-%{version}-beta.tar.bz2
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{?commit:%{commit}}%{!?commit:%{version}}/%{name}-%{?commit:%{commit}}%{!?commit:%{version}}.tar.bz2
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(liboqs)

%description
postquantumcryptoengine is an extension to the bctoolbox lib providing Post
Quantum Cryptography.

 *  Kyber 512, 768 and 1024
 *  HQC 128, 192 and 256 (NIST round 3 version)
 *  X25519 and X448 in KEM version and a way to combine two or more of
    theses.

#---------------------------------------------------------------------------

%package -n	%{libname}
Summary:	Post Quantum algorithm integration to bctoolbox
Group:		System/Libraries

%description -n	%{libname}
postquantumcryptoengine is an extension to the bctoolbox lib providing Post
Quantum Cryptography.

 *  Kyber 512, 768 and 1024
 *  HQC 128, 192 and 256 (NIST round 3 version)
 *  X25519 and X448 in KEM version and a way to combine two or more of
    theses.

%files -n %{libname}
%{_libdir}/lib%{name}.so.*

#---------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{devname}
This package contains development files for %{name}

%files -n %{devname}
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}

#---------------------------------------------------------------------------

%prep
#%%autosetup -p1 -n %{name}-%{version}-beta-%{commit}
%autosetup -p1 -n %{name}-%{?commit:%{commit}}%{!?commit:%{version}}

%build
%cmake \
	-DENABLE_STRICT:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_TESTS:BOOL=%{?with_tests:ON}%{?!with_tests:OFF} \
	-DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/%{name} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# fix cmake stuff path
install -dm 0755 %{buildroot}%{_libdir}/cmake
mv %{buildroot}%{_datadir}/%{name}/cmake %{buildroot}%{_libdir}/cmake/%{name}
rmdir %{buildroot}%{_datadir}/%{name}


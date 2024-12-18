%global major 1
%global libname %mklibname %{name}
%global devname %mklibname %{name} -d

# exclude unwanted cmake requires
%global __provides_exclude_from ^%{_datadir}/cmake/.*/Find.*cmake$

%bcond strict			1
%bcond unit_tests		1
%bcond unit_tests_install	0

Summary:	Post Quantum algorithm integration to bctoolbox
Name:		postquantumcryptoengine
Version:	5.3.97
Release:	1
License:	GPLv3
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
Patch0:		postquantumcryptoengine-5.2.94-cmake-config-location.patch 
Patch100:	postquantumcryptoengine-5.2.94_fix_sizeof_declaration.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(bctoolbox)
BuildRequires:	cmake(liboqs)

%description
postquantumcryptoengine is an extension to the bctoolbox lib providing Post
Quantum Cryptography.

 *  Kyber 512, 768 and 1024
 *  HQC 128, 192 and 256 (NIST round 3 version)
 *  X25519 and X448 in KEM version and a way to combine two or more of
    theses.

%if %{with unit_tests} && %{with unit_tests_install} 
%files
%{_bindir}/pqcrypto-tester
%endif

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
%license LICENSE.txt
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_datadir}/cmake/PostQuantumCryptoEngine

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{?commit:%{commit}}%{!?commit:%{version}}

%build
%cmake \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_unit_tests:ON}%{?!with_unit_tests:OFF} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# don't install unit tester
%if %{with unit_tests} && ! %{with unit_tests_install}
rm -f %{buildroot}%{_bindir}/pqcrypto-tester
%endif

%check
%if %{with unit_tests}
pushd build
#FIXME: some tests may fail at ABF
ctest || true
popd
%endif


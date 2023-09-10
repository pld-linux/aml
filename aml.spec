#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Andri's Main Loop library
Summary(pl.UTF-8):	Biblioteka pętli głównej Andri's Main Loop
Name:		aml
Version:	0.3.0
Release:	1
License:	ISC
Group:		Libraries
#https://github.com/any1/aml/releases
Source0:	https://github.com/any1/aml/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	72fad42e1b5efc3055055df6a7b5f1d8
URL:		https://github.com/any1/aml
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Another Main Loop library - Andri's Main Loop.

Goals:
- Portability
- Utility
- Simplicity

Non-goals:
- MS Windows (TM) support
- Solving the C10K problem

Features:
- File descriptor event handlers
- Timers
- Tickers
- Signal handlers
- Idle dispatch callbacks
- Thread pool
- Interoperability with other event loops

%description -l pl.UTF-8
Jeszcze jedna biblioteka pętli głównej - Andri's Main Loop.

Cele:
- przenośność
- użyteczność
- prostota

Celami nie są:
- obsługa MS Windows (TM)
- rozwiązanie problemu C10K

Funkcjonalność:
- obsługa zdarzeń związanych z deskryptorami plików
- stopery
- zegary
- obsługa sygnałów
- wywołania zwrotne w czasie bezczynności
- pula wątków
- współpraca z innymi pętlami zdarzeń

%package devel
Summary:	Header files for libaml library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libaml
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libaml library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libaml.

%package static
Summary:	Static libaml library
Summary(pl.UTF-8):	Statyczna biblioteka libaml
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libaml library.

%description static -l pl.UTF-8
Statyczna biblioteka libaml.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_libdir}/libaml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaml.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaml.so
%{_includedir}/aml.h
%{_pkgconfigdir}/aml.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libaml.a
%endif

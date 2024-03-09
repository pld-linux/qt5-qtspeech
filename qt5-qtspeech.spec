#
# Conditional build:
%bcond_without	doc			# documentation
%bcond_without	flite			# Flite plugin
%bcond_without	speech_dispatcher	# Speech Dispatcher plugin

%define		orgname		qtspeech
%define		qtbase_ver		%{version}
%define		qttools_ver		%{version}
%define		qtxmlpatterns_ver	%{version}
Summary:	The Qt5 Speech library
Summary(pl.UTF-8):	Biblioteka Qt5 Speech
Name:		qt5-%{orgname}
Version:	5.15.13
Release:	1
License:	LGPL v3 or GPL v2+ or commercial
Group:		Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	a8eff80706ba3fc12c6f70d198c78736
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Multimedia-devel >= %{qtbase_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
BuildRequires:	Qt5XmlPatterns-devel >= %{qtxmlpatterns_ver}
BuildRequires:	qt5-doc-common >= %{qtbase_ver}
%if %{with flite}
BuildRequires:	flite-devel >= 2.1
%endif
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
%if %{with speech_dispatcher}
BuildRequires:	speech-dispatcher-devel
%endif
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Speech library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Speech.

%package -n Qt5Speech
Summary:	The Qt5 Speech library
Summary(pl.UTF-8):	Biblioteka Qt5 Speech
Group:		Libraries
%requires_eq_to	Qt5Core Qt5Core-devel

%description -n Qt5Speech
Qt5 Speech library.

%description -n Qt5Speech -l pl.UTF-8
Biblioteka Qt5 Speech.

%package -n Qt5Speech-devel
Summary:	Qt5 Speech library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Speech - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Speech = %{version}-%{release}

%description -n Qt5Speech-devel
Qt5 Speech library - development files.

%description -n Qt5Speech-devel -l pl.UTF-8
Biblioteka Qt5 Speech - pliki programistyczne.

%package -n Qt5Speech-plugin-speechd
Summary:	Speech Dispatcher plugin for Qt5 Speech library
Summary(pl.UTF-8):	Wtyczka Speech Dispatcher do biblioteki Qt5 Speech
Group:		Libraries
Requires:	Qt5Speech = %{version}-%{release}

%description -n Qt5Speech-plugin-speechd
Speech Dispatcher plugin for Qt5 Speech library.

%description -n Qt5Speech-plugin-speechd -l pl.UTF-8
Wtyczka Speech Dispatcher do biblioteki Qt5 Speech

%package -n Qt5Speech-plugin-flite
Summary:	flite plugin for Qt5 Speech library
Summary(pl.UTF-8):	Wtyczka flite do biblioteki Qt5 Speech
Group:		Libraries
Requires:	Qt5Speech = %{version}-%{release}
Requires:	flite >= 2.1

%description -n Qt5Speech-plugin-flite
flite plugin for Qt5 Speech library.

%description -n Qt5Speech-plugin-flite -l pl.UTF-8
Wtyczka flite do biblioteki Qt5 Speech

%package doc
Summary:	Qt5 Speech documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Speech w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 Speech documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Speech w formacie HTML.

%package doc-qch
Summary:	Qt5 Speech documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Speech w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 Speech documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Speech w formacie QCH.

%package examples
Summary:	Qt5 Speech examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Speech
License:	BSD or commercial
Group:		Development/Libraries
BuildArch:	noarch

%description examples
Qt5 Speech examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Speech.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
%{qmake_qt5} -- \
	-%{!?with_flite:no-}flite \
	-%{!?with_speech_dispatcher:no-}speechd
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/speech

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Speech -p /sbin/ldconfig
%postun	-n Qt5Speech -p /sbin/ldconfig

%files -n Qt5Speech
%defattr(644,root,root,755)
%doc dist/changes-*
# R: Core
%attr(755,root,root) %{_libdir}/libQt5TextToSpeech.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5TextToSpeech.so.5
%dir %{_libdir}/qt5/plugins/texttospeech
%dir %{_libdir}/cmake/Qt5TextToSpeech

%files -n Qt5Speech-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5TextToSpeech.so
%{_libdir}/libQt5TextToSpeech.prl
%{_includedir}/qt5/QtTextToSpeech
%{_pkgconfigdir}/Qt5TextToSpeech.pc
%{_libdir}/cmake/Qt5TextToSpeech/Qt5TextToSpeechConfig*.cmake
%{qt5dir}/mkspecs/modules/qt_lib_texttospeech.pri
%{qt5dir}/mkspecs/modules/qt_lib_texttospeech_private.pri

%files -n Qt5Speech-plugin-speechd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt5/plugins/texttospeech/libqtexttospeech_speechd.so
%{_libdir}/cmake/Qt5TextToSpeech/Qt5TextToSpeech_QTextToSpeechPluginSpeechd.cmake

%if %{with flite}
%files -n Qt5Speech-plugin-flite
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt5/plugins/texttospeech/libqttexttospeech_flite.so
%{_libdir}/cmake/Qt5TextToSpeech/Qt5TextToSpeech_QTextToSpeechEngineFlite.cmake
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtspeech

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtspeech.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5

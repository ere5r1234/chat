[app]

# (str) Title of your application
title = CrossPlatformChat

# (str) Package name
package.name = crossplatformchat

# (str) Package domain (needed for android/ios packaging)
package.domain = com.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy>=2.2.0,pyyaml

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
#requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services =

#
# OSX Specific
#
# (str) Path to a custom kivy_launcher.ini file
#osx.kivy_launcher.ini = %(source.dir)s/data/kivy_launcher.ini

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names: 
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray, darkgray, grey,
# lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy, olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format. 
# see https://lottiefiles.com/ for examples and https://airbnb.design/lottie/ 
# for general documentation. 
#android.presplash_lottie = %(source.dir)s/data/presplash.json

# (str) Adaptive icon of the application (used if Android API level is 26+ at runtime)
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (list) features (adds uses-feature -tags to manifest)
#android.features = android.hardware.usb.host

# (int) Target Android API, should be as high as possible.
#android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 26

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 23b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 21

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer. If set to True, it will be accepted automatically.
# android.accept_sdk_license = False

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = '@android:style/Theme.NoTitleBar'

# (list) Pattern to whitelist for the whole project
#android.whitelist = 

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process.
#android.add_jars = name.jar,path/to/jar.jar

# (list) List of Java files to add to the android project (can be java or a directory containing
# java files)
#android.add_src =

# (list) Android AAR archives to add
#android.add_aars = path/to/aar.aar

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (list) Copy these files to src/main/res/xml/ (used for example with intent-filters)
#android.res_xml = PATH_TO_FILE, 

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (str) screenOrientation to set for the main activity. 
# Valid values can be found at https://developer.android.com/guide/topics/manifest/activity-element.html#screen
#android.manifest.orientation = fullSensor

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data = 

# (list) Android library project to add (will be added in the 
# project.properties automatically.)
#android.library_references =

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
#android.uses_library =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
#android.arch = armeabi-v7a

# (int) overrides automatic versionCode computation (used in build.gradle)
# this is not the same as app version and should only be edited if you know what you're doing
# android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
# android.allow_backup = True

# (str) XML file for backup rules (see official auto backup documentation)
# android.backup_rules = 

# (str) For debugging purpose, if you leave this field empty, the application will
# be listed in the debug apps of the device.
#android.debuggable = 1

#
# iOS specific
#

# (str) Path to a custom kivy-ios directory
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git repository to clone
#ios.kivy_ios_url = https://github.com/kivy/kivy-ios.git
#ios.kivy_ios_branch = master

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa)
# bin_dir = ./bin

# (list) The build commands to be executed in order
# You can add your own commands here
#build.commands =

# (str) The URL of the buildserver.
# This is the server used to build the application. 
# Valid options are:
# - http://buildozer.io:8090
# - https://buildozer.io:8090
#buildserver = http://buildozer.io:8090

# (list) A list of whitelisted signing keys.
# These signing keys will be accepted when verifying signatures from the buildserver.
#buildserver_whitelist_keys =

# (str) The certificate file to use for SSL connections with the buildserver.
#buildserver_certificate =

# (str) The domain to check for buildserver certificates.
#buildserver_domain = buildozer.io

# #########
# WARNINGS
# #########

# (int) If this is set to 1, Buildozer will check for updates each time it is run.
# This is a good idea to keep up to date with new features, but can cause problems if
# Buildozer makes a breaking change and the user's code depends on old behavior.
#check_for_updates = 1

# #########
# INTERNET
# #########

# (bool) Use the internet connection to download dependencies
# Need to be set to True if you want to download any dependencies
# that aren't already installed on your system.
# Without this, Buildozer will fail if any dependencies are missing.
# However, setting this to False can be useful if you're working in an
# environment with no internet, and have already downloaded all dependencies.
#offline = 0

# (bool) Skip the verification of downloaded files
#verify_downloads = 1

# (str) The default pypi server to use for downloading Python packages.
#pypi_server = https://pypi.org/simple

# (str) A custom index URL for pip.
#pip_index_url =

# (str) A custom trusted host for pip.
#pip_trusted_host =

# #########
# ANDROID STUFF
# #########

# (bool) Whether to skip cleaning, useful for debugging
#android.skip_clean = False

# (str) Path to android SDK tools, if not set, Buildozer will try to find it automatically
#android.sdk_path =

# (str) Path to android NDK, if not set, Buildozer will try to find it automatically
#android.ndk_path =

# (str) Path to android SDK tools, if not set, Buildozer will try to find it automatically
#android.sdk_tools_path =

# (str) Path to android SDK platform tools, if not set, Buildozer will try to find it automatically
#android.platform_tools_path =

# (str) Path to android build tools, if not set, Buildozer will try to find it automatically
#android.build_tools_path =

# (str) Path to android build tools version, if not set, Buildozer will try to find it automatically
#android.build_tools_version =

# (str) Path to android SDK platform, if not set, Buildozer will try to find it automatically
#android.platform = android-%(android.api)s

# (bool) If True, then Android builds will be done using the gradle build system
#android.gradle = True

# (str) Gradle version to use
#android.gradle_version = 7.0.2

# (str) Android Gradle Plugin version to use
#android.gradle_plugin_version = 7.0.0

# (str) Android NDK path
#android.ndk_path =

# (str) Android NDK version
#android.ndk_version = 21.4.7075529

# (str) Android API version to use
#android.api = 31

# (str) Android min API version to use
#android.minapi = 26

# (str) Android target API version to use
#android.targetapi = 31

# (str) Android SDK tools version
#android.sdk_tools = 26.1.1

# (str) Android SDK platform tools version
#android.platform_tools = 33.0.1

# (str) Android build tools version
#android.build_tools = 33.0.1

# (str) Path to the android sdk tools
#android.sdk_tools_path =

# (str) Path to the android platform tools
#android.platform_tools_path =

# (str) Path to the android build tools
#android.build_tools_path =

# (str) Path to the android SDK platform
#android.platform_path =

# (str) Path to the android SDK
#android.sdk_path =

# (str) Path to the android NDK
#android.ndk_path =

# (str) Path to the android NDK version
#android.ndk_version =

# (str) Path to the android API
#android.api_path =

# (str) Path to the android min API
#android.minapi_path =

# (str) Path to the android target API
#android.targetapi_path =

# (str) Path to the android SDK tools
#android.sdk_tools_path =

# (str) Path to the android platform tools
#android.platform_tools_path =

# (str) Path to the android build tools
#android.build_tools_path =

# (str) Path to the android SDK platform
#android.platform_path =

# (str) Path to the android SDK
#android.sdk_path =

# (str) Path to the android NDK
#android.ndk_path =

# (str) Path to the android NDK version
#android.ndk_version =

# (str) Path to the android API
#android.api_path =

# (str) Path to the android min API
#android.minapi_path =

# (str) Path to the android target API
#android.targetapi_path =
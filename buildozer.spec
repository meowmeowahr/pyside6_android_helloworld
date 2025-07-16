; The application build settings for Buildozer
; iOS is not supported

[app]
; Application settings
title = PySide6 Hello World
package.name = pyside_hello
package.domain = com.meowmeowahr
source.dir = .
version = 0.1
requirements = python3,shiboken6,PySide6

; App orientation
; Must be landscape or portrait
; Auto-rotate isn't supported
; Multi-window and floating window support will work
orientation = portrait
fullscreen = 1

; Indlude additional file extensions here
source.include_exts = py,png,jpg,kv,atlas,qml,js,xml

; Set your Android permissions here
android.permissions = android.permission.INTERNET, android.permission.WRITE_EXTERNAL_STORAGE

; Add your Qt modules here
; Core,Widgets,Gui are required
p4a.extra_args = --qt-libs=Core,Widgets,Gui --load-local-libs=plugins_platforms_qtforandroid --init-classes=

; Set your non-adaptive icon here
; Adaptive icon support is broken in Buildozer==1.5.0
icon.filename = ./assets/icon.png

; SDK and NDK
; The SDK will be automatically downloaded
; The NDK must be installed with the download.sh script
android.ndk_path = .ndk/android-ndk
android.sdk_path = .sdk/android-sdk

; Internal
android.archs = arm64-v8a
android.allow_backup = True
p4a.bootstrap = qt
p4a.local_recipes = deployment/recipes
p4a.branch = develop
android.add_jars = deployment/jar/PySide6/jar/Qt6Android.jar,./deployment/jar/PySide6/jar/Qt6AndroidBindings.jar

[buildozer]
log_level = 2
warn_on_root = 1

; APK output directory
; ./dist is standard in many Python build tools
bin_dir = ./dist


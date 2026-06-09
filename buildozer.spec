[app]

# (string) Title of your application
title = GPS Tracker

# (string) Package name
package.name = gpstracker

# (string) Package domain (needed for android package naming)
package.domain = org.daulat

# (string) Source code directory
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (string) Application version
version = 0.1

# (list) Application requirements
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, plyer

# (str) Supported orientations
orientation = portrait

# (bool) Use fullscreen mode or not
fullscreen = 0

# ==============================================================================
# Android specific settings
# ==============================================================================

# (list) Android permissions
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android NDK API to use
android.ndk_api = 21

# ------ यहाँ हमने नया Nipro NDK फिक्स जोड़ा है ------
# (str) Android NDK version to use
android.ndk = 26b
# ------------------------------------------------

# (bool) Use private storage or external
android.private_storage = True

# (bool) Accept SDK license without prompting
android.accept_sdk_license = True

# (list) The Android architectures to build for.
android.archs = armeabi-v7a, arm64-v8a

# ==============================================================================
# Buildozer settings
# ==============================================================================

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug and big outputs)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

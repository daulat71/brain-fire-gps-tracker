[app]

# (str) Title of your application
title = GPS Tracker

# (str) Package name
package.name = gpstracker

# (str) Package domain (needed for android packaging)
package.domain = org.daulat

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
# KivyMD 1.2.0 और आधुनिक टूल्स के लिए ये वर्जन एकदम स्टेबल हैं
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, plyer, requests, urllib3, openssl, certifi

# (str) Supported orientations (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# GPS लोकेशन ट्रैकिंग और एंड्रॉइड 13+ नोटिफिकेशन्स के लिए आवश्यक अनुमतियां
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE, FOREGROUND_SERVICE_LOCATION, POST_NOTIFICATIONS

# (int) Target Android API, should be as high as possible.
# JDK 17 के साथ API 34 सबसे परफेक्ट काम करता है
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android NDK API to use
android.ndk_api = 21

# (str) Android NDK version to use
android.ndk = 25c

# (bool) Use private storage for data (True or False)
android.private_storage = True

# (bool) Accept SDK license without prompting
android.accept_sdk_license = True

# (list) The Android architectures to build for.
# arm64-v8a (नए फोन) और armeabi-v7a (पुराने फोन) दोनों को जोड़ा है ताकि ऐप सब जगह चले
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug and big outputs)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

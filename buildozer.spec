[app]
title = GPS Tracker
package.name = gpstracker
package.domain = org.daulat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 🛠️ सुधार 1: यहाँ cython का सटीक वर्जन डालना अनिवार्य है
requirements = python3, cython==0.29.36, kivy==2.3.0, kivymd==1.2.0, plyer, requests

orientation = portrait
fullscreen = 0

# जीपीएस और इंटरनेट के लिए परमिशन्स
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# 🛠️ सुधार 2: API 33 के लिए सबसे स्थिर (Stable) NDK और API सेटिंग्स
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b

# बिल्ड को सुचारू रूप से चलाने के लिए कुछ अतिरिक्त सेटिंग्स
android.private_storage = True
android.accept_sdk_license = True

android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
